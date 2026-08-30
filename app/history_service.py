import threading
from pathlib import Path

from app.database import get_connection
from app.image_service import (
    get_image_batch_status,
)
from app.job_store import get_job, BASE_DIR
from app.normalizer_service import (
    get_prompt_packages,
)
from app.request_context import (
    get_current_owner_id,
)
from app.platform.storage_backend import (
    get_storage_backend,
)


_SCHEMA_READY = False
_SCHEMA_LOCK = threading.RLock()

STORAGE = get_storage_backend(
    BASE_DIR
)


# ============================================================
# SCHEMA
# ============================================================

def _column_names(
    connection,
    table_name: str,
):
    return {
        row["name"]
        for row in connection.execute(
            f"PRAGMA table_info({table_name})"
        ).fetchall()
    }


def ensure_history_schema(force: bool = False):
    global _SCHEMA_READY

    if _SCHEMA_READY and not force:
        return

    with _SCHEMA_LOCK:
        if _SCHEMA_READY and not force:
            return

        connection = get_connection()

        try:
            job_columns = _column_names(
                connection,
                "generation_jobs",
            )

            if "is_favorite" not in job_columns:
                connection.execute(
                    """
                    ALTER TABLE generation_jobs
                    ADD COLUMN is_favorite INTEGER
                    NOT NULL DEFAULT 0
                    """
                )

            image_columns = _column_names(
                connection,
                "generated_images",
            )

            if "is_favorite" not in image_columns:
                connection.execute(
                    """
                    ALTER TABLE generated_images
                    ADD COLUMN is_favorite INTEGER
                    NOT NULL DEFAULT 0
                    """
                )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_generation_jobs_favorite
                ON generation_jobs(is_favorite)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_generated_images_favorite
                ON generated_images(is_favorite)
                """
            )

            connection.commit()

        finally:
            connection.close()

        _SCHEMA_READY = True



# ============================================================
# HELPERS
# ============================================================

def _provider_parts(
    value: str | None,
):
    pieces = [
        piece
        for piece in str(
            value or ""
        ).split(":")
        if piece
    ]

    return {
        "provider":
            pieces[0]
            if len(pieces) > 0
            else None,

        "model":
            pieces[1]
            if len(pieces) > 1
            else None,

        "quality":
            pieces[2]
            if len(pieces) > 2
            else None,

        "size":
            pieces[3]
            if len(pieces) > 3
            else None,
    }


def _display_status(
    job_status: str,
    prompt_count: int,
    complete_count: int,
    failed_count: int,
):
    if (
        prompt_count > 0
        and
        complete_count >= prompt_count
    ):
        return "complete"

    if (
        complete_count > 0
        and
        failed_count > 0
    ):
        return "partial"

    if complete_count > 0:
        return "partial"

    if (
        job_status
        in {
            "planning_failed",
            "normalization_failed",
        }
    ):
        return "failed"

    if job_status == "structured":
        return "prompts_ready"

    if job_status == "planned_raw":
        return "planned"

    return (
        job_status
        or
        "draft"
    )


def _history_media_url(
    storage_ref: str | None,
    fallback_url: str,
):
    ref = str(storage_ref or "")

    if ref.startswith("r2://"):
        try:
            # Presigning is local; it does not perform an R2 network request.
            # This lets History thumbnails load directly from private R2
            # instead of FastAPI -> Turso -> redirect for every image.
            return STORAGE.signed_get_url(
                ref
            )
        except Exception:
            return None

    # Once R2 is the active storage backend, legacy local file references are
    # intentionally not requested as History thumbnails. Hyperex may still
    # keep their job metadata in Turso, but the files themselves were not
    # migrated to R2. Returning None lets the UI render NO PREVIEW instead of
    # generating repeated /api/images/.../file 404 requests on every History
    # load. Local-storage mode keeps the original fallback behavior.
    if getattr(STORAGE, "name", "local") == "r2":
        return None

    return fallback_url


def _thumbnail_map(
    connection,
    job_ids: list[int],
    limit: int = 4,
):
    result = {
        int(job_id): []
        for job_id in job_ids
    }

    if not job_ids:
        return result

    placeholders = ",".join(
        "?"
        for _ in job_ids
    )

    # One query for generated thumbnails across every visible job. The old
    # implementation opened a new Turso connection/query for every history
    # card, which became an N+1 network-latency problem after cloud migration.
    generated_rows = connection.execute(
        f"""
        SELECT
            gi.id,
            gi.job_id,
            gi.prompt_id,
            gi.file_path,
            COALESCE(
                gp.position,
                gi.id
            ) AS display_position

        FROM generated_images gi

        LEFT JOIN generated_prompts gp
            ON gp.id = gi.prompt_id

        WHERE
            gi.job_id IN ({placeholders})
            AND gi.status = 'complete'

        ORDER BY
            gi.job_id DESC,
            display_position ASC,
            gi.id DESC
        """,
        tuple(job_ids),
    ).fetchall()

    seen_prompts = {
        int(job_id): set()
        for job_id in job_ids
    }

    for row in generated_rows:
        job_id = int(
            row["job_id"]
        )

        if len(result[job_id]) >= limit:
            continue

        prompt_id = row[
            "prompt_id"
        ]

        prompt_key = (
            f"prompt:{prompt_id}"
            if prompt_id is not None
            else f"image:{row['id']}"
        )

        if prompt_key in seen_prompts[job_id]:
            continue

        seen_prompts[job_id].add(
            prompt_key
        )

        image_id = int(
            row["id"]
        )

        media_url = _history_media_url(
            row["file_path"],
            f"/api/images/{image_id}/file",
        )

        if not media_url:
            continue

        result[job_id].append({
            "type": "generated",
            "url": media_url,
        })

    missing_job_ids = [
        job_id
        for job_id, items in result.items()
        if not items
    ]

    if not missing_job_ids:
        return result

    placeholders = ",".join(
        "?"
        for _ in missing_job_ids
    )

    reference_rows = connection.execute(
        f"""
        SELECT
            id,
            job_id,
            position,
            file_path

        FROM reference_images

        WHERE job_id IN ({placeholders})

        ORDER BY
            job_id DESC,
            position ASC
        """,
        tuple(missing_job_ids),
    ).fetchall()

    for row in reference_rows:
        job_id = int(
            row["job_id"]
        )

        if len(result[job_id]) >= limit:
            continue

        reference_id = int(
            row["id"]
        )

        media_url = _history_media_url(
            row["file_path"],
            (
                f"/api/jobs/{job_id}"
                f"/references/{reference_id}/file"
            ),
        )

        if not media_url:
            continue

        result[job_id].append({
            "type": "reference",
            "url": media_url,
        })

    return result


# ============================================================
# LIST / SEARCH
# ============================================================

def list_history_jobs(
    q: str = "",
    profile_id: int | None = None,
    planner_provider: str | None = None,
    image_provider: str | None = None,
    status: str | None = None,
    favorites_only: bool = False,
    limit: int = 100,
    offset: int = 0,
):
    ensure_history_schema()

    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        clauses = [
            "gj.owner_id = ?"
        ]

        params = [
            owner_id
        ]

        clean_query = (
            q
            .strip()
            .lower()
        )

        if clean_query:
            clauses.append(
                """
                (
                    LOWER(gp.name) LIKE ?
                    OR LOWER(
                        COALESCE(
                            gj.description,
                            ''
                        )
                    ) LIKE ?
                    OR CAST(
                        gj.id
                        AS TEXT
                    ) LIKE ?
                )
                """
            )

            pattern = (
                f"%{clean_query}%"
            )

            params.extend(
                [
                    pattern,
                    pattern,
                    pattern,
                ]
            )

        if profile_id is not None:
            clauses.append(
                "gj.profile_id = ?"
            )

            params.append(
                profile_id
            )

        if planner_provider:
            clean_planner_provider = (
                planner_provider
                .strip()
                .lower()
            )

            if (
                clean_planner_provider
                ==
                "gemini"
            ):
                clauses.append(
                    """
                    (
                        LOWER(
                            COALESCE(
                                gj.planner_provider,
                                ''
                            )
                        ) = 'gemini'

                        OR (
                            gj.planner_provider IS NULL
                            AND LOWER(
                                COALESCE(
                                    gj.planner_model,
                                    ''
                                )
                            ) LIKE 'gemini%'
                        )
                    )
                    """
                )

            elif (
                clean_planner_provider
                ==
                "openai"
            ):
                clauses.append(
                    """
                    (
                        LOWER(
                            COALESCE(
                                gj.planner_provider,
                                ''
                            )
                        ) = 'openai'

                        OR (
                            gj.planner_provider IS NULL
                            AND LOWER(
                                COALESCE(
                                    gj.planner_model,
                                    ''
                                )
                            ) LIKE 'gpt%'
                        )
                    )
                    """
                )

            else:
                clauses.append(
                    """
                    LOWER(
                        COALESCE(
                            gj.planner_provider,
                            ''
                        )
                    ) = ?
                    """
                )

                params.append(
                    clean_planner_provider
                )

        if image_provider:
            clauses.append(
                """
                EXISTS (
                    SELECT 1

                    FROM generated_images gi_filter

                    WHERE
                        gi_filter.job_id = gj.id
                        AND LOWER(
                            COALESCE(
                                gi_filter.provider,
                                ''
                            )
                        ) LIKE ?
                )
                """
            )

            params.append(
                (
                    image_provider
                    .strip()
                    .lower()
                    +
                    ":%"
                )
            )

        if favorites_only:
            clauses.append(
                """
                (
                    COALESCE(
                        gj.is_favorite,
                        0
                    ) = 1

                    OR EXISTS (
                        SELECT 1

                        FROM generated_images gi_fav

                        WHERE
                            gi_fav.job_id = gj.id
                            AND COALESCE(
                                gi_fav.is_favorite,
                                0
                            ) = 1
                    )
                )
                """
            )

        where_sql = (
            "WHERE "
            +
            " AND ".join(
                clauses
            )
            if clauses
            else
            ""
        )

        # Pull extra rows before applying derived-status filtering.
        raw_limit = min(
            max(
                limit + offset,
                100,
            ),
            500,
        )

        rows = connection.execute(
            f"""
            SELECT
                gj.id,
                gj.profile_id,
                gj.profile_version_id,
                gj.description,
                gj.requested_count,
                gj.status,
                gj.planner_provider,
                gj.planner_model,
                gj.created_at,
                gj.updated_at,
                COALESCE(
                    gj.is_favorite,
                    0
                ) AS is_favorite,

                gp.name
                    AS profile_name,

                (
                    SELECT COUNT(*)

                    FROM reference_images ri

                    WHERE ri.job_id = gj.id
                )
                    AS reference_count,

                (
                    SELECT COUNT(*)

                    FROM generated_prompts prm

                    WHERE prm.job_id = gj.id
                )
                    AS prompt_count,

                (
                    SELECT COUNT(
                        DISTINCT gi_complete.prompt_id
                    )

                    FROM generated_images gi_complete

                    WHERE
                        gi_complete.job_id = gj.id
                        AND gi_complete.status = 'complete'
                )
                    AS complete_count,

                (
                    SELECT COUNT(
                        DISTINCT gi_failed.prompt_id
                    )

                    FROM generated_images gi_failed

                    WHERE
                        gi_failed.job_id = gj.id
                        AND gi_failed.status = 'failed'
                        AND NOT EXISTS (
                            SELECT 1

                            FROM generated_images gi_success

                            WHERE
                                gi_success.job_id = gj.id
                                AND gi_success.prompt_id =
                                    gi_failed.prompt_id
                                AND gi_success.status =
                                    'complete'
                        )
                )
                    AS failed_count,

                (
                    SELECT provider

                    FROM generated_images gi_provider

                    WHERE
                        gi_provider.job_id = gj.id
                        AND gi_provider.status = 'complete'

                    ORDER BY gi_provider.id DESC

                    LIMIT 1
                )
                    AS image_provider_label,

                (
                    SELECT COUNT(*)

                    FROM generated_images gi_fav_count

                    WHERE
                        gi_fav_count.job_id = gj.id
                        AND COALESCE(
                            gi_fav_count.is_favorite,
                            0
                        ) = 1
                )
                    AS favorite_image_count

            FROM generation_jobs gj

            JOIN generation_profiles gp
                ON gp.id = gj.profile_id

            {where_sql}

            ORDER BY
                gj.id DESC

            LIMIT ?
            """,
            (
                *params,
                raw_limit,
            ),
        ).fetchall()

        thumbnail_map = _thumbnail_map(
            connection,
            [
                int(row["id"])
                for row in rows
            ],
        )

        items = []

        for row in rows:
            item = dict(
                row
            )

            item_status = _display_status(
                item["status"],
                int(
                    item["prompt_count"]
                    or
                    0
                ),
                int(
                    item["complete_count"]
                    or
                    0
                ),
                int(
                    item["failed_count"]
                    or
                    0
                ),
            )

            if (
                status
                and
                item_status
                !=
                status
            ):
                continue

            provider = _provider_parts(
                item.get(
                    "image_provider_label"
                )
            )

            if not item.get(
                "planner_provider"
            ):
                planner_model = str(
                    item.get(
                        "planner_model"
                    )
                    or
                    ""
                ).lower()

                if planner_model.startswith(
                    "gemini"
                ):
                    item[
                        "planner_provider"
                    ] = "gemini"

                elif planner_model.startswith(
                    "gpt"
                ):
                    item[
                        "planner_provider"
                    ] = "openai"

            item["display_status"] = (
                item_status
            )

            item["image_provider"] = (
                provider[
                    "provider"
                ]
            )

            item["image_model"] = (
                provider[
                    "model"
                ]
            )

            item["image_quality"] = (
                provider[
                    "quality"
                ]
            )

            item["image_size"] = (
                provider[
                    "size"
                ]
            )

            item["thumbnails"] = (
                thumbnail_map.get(
                    int(item["id"]),
                    [],
                )
            )

            item["has_favorite_output"] = (
                int(
                    item[
                        "favorite_image_count"
                    ]
                    or
                    0
                )
                >
                0
            )

            items.append(
                item
            )

        total_filtered = len(
            items
        )

        paged = items[
            offset:
            offset + limit
        ]

        return {
            "items":
                paged,
            "count":
                len(
                    paged
                ),
            "total":
                total_filtered,
            "offset":
                offset,
            "limit":
                limit,
        }

    finally:
        connection.close()


# ============================================================
# OPTIONS
# ============================================================

def get_history_options():
    ensure_history_schema()

    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        profiles = connection.execute(
            """
            SELECT
                gp.id,
                gp.name

            FROM generation_profiles gp

            LEFT JOIN managed_workflows mw
                ON mw.profile_id = gp.id

            WHERE
                gp.owner_id = ?
                OR (
                    gp.owner_id IS NULL
                    AND mw.status = 'published'
                )

            ORDER BY gp.name ASC
            """,
            (
                owner_id,
            ),
        ).fetchall()

        return {
            "profiles": [
                dict(
                    row
                )
                for row in profiles
            ],

            "planner_providers": [
                "openai",
                "gemini",
            ],

            "image_providers": [
                "openai",
                "gemini",
            ],

            "statuses": [
                "complete",
                "partial",
                "prompts_ready",
                "planned",
                "failed",
                "prepared",
            ],
        }

    finally:
        connection.close()


# ============================================================
# DETAIL
# ============================================================

def get_history_detail(
    job_id: int,
):
    ensure_history_schema()

    job = get_job(
        job_id
    )

    if job is None:
        return None

    connection = get_connection()

    try:
        favorite = connection.execute(
            """
            SELECT
                COALESCE(
                    is_favorite,
                    0
                ) AS is_favorite

            FROM generation_jobs

            WHERE id = ?
            """,
            (job_id,),
        ).fetchone()

    finally:
        connection.close()

    packages = (
        get_prompt_packages(
            job_id
        )
        or
        {
            "packages":
                [],
            "source_verified":
                False,
        }
    )

    batch = (
        get_image_batch_status(
            job_id
        )
        or
        {
            "status":
                "no_prompts",
            "items":
                [],
            "complete_count":
                0,
            "failed_count":
                0,
            "total_prompts":
                0,
        }
    )

    job["is_favorite"] = (
        bool(
            favorite[
                "is_favorite"
            ]
        )
        if favorite
        else
        False
    )

    if not job.get(
        "planner_provider"
    ):
        planner_model = str(
            job.get(
                "planner_model"
            )
            or
            ""
        ).lower()

        if planner_model.startswith(
            "gemini"
        ):
            job[
                "planner_provider"
            ] = "gemini"

        elif planner_model.startswith(
            "gpt"
        ):
            job[
                "planner_provider"
            ] = "openai"

    job["packages"] = packages
    job["batch"] = batch

    return job


# ============================================================
# FAVORITES
# ============================================================

def set_job_favorite(
    job_id: int,
    favorite: bool,
):
    ensure_history_schema()

    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        cursor = connection.execute(
            """
            UPDATE generation_jobs

            SET is_favorite = ?

            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                1
                if favorite
                else
                0,
                job_id,
                owner_id,
            ),
        )

        connection.commit()

        if cursor.rowcount < 1:
            return None

        return {
            "job_id":
                job_id,
            "is_favorite":
                bool(
                    favorite
                ),
        }

    finally:
        connection.close()


def set_image_favorite(
    image_id: int,
    favorite: bool,
):
    ensure_history_schema()

    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        cursor = connection.execute(
            """
            UPDATE generated_images

            SET is_favorite = ?

            WHERE
                id = ?
                AND EXISTS (
                    SELECT 1
                    FROM generation_jobs gj
                    WHERE
                        gj.id =
                            generated_images.job_id
                        AND gj.owner_id = ?
                )
            """,
            (
                1
                if favorite
                else
                0,
                image_id,
                owner_id,
            ),
        )

        connection.commit()

        if cursor.rowcount < 1:
            return None

        row = connection.execute(
            """
            SELECT
                job_id

            FROM generated_images

            WHERE id = ?
            """,
            (image_id,),
        ).fetchone()

        return {
            "image_id":
                image_id,
            "job_id":
                (
                    row[
                        "job_id"
                    ]
                    if row
                    else
                    None
                ),
            "is_favorite":
                bool(
                    favorite
                ),
        }

    finally:
        connection.close()

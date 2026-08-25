from app.database import get_connection
from app.image_service import (
    get_image_batch_status,
)
from app.job_store import get_job
from app.normalizer_service import (
    get_prompt_packages,
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


def ensure_history_schema():
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


def _thumbnail_urls(
    job_id: int,
    limit: int = 4,
):
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                gi.id,
                gp.position

            FROM generated_images gi

            LEFT JOIN generated_prompts gp
                ON gp.id = gi.prompt_id

            WHERE
                gi.job_id = ?
                AND gi.status = 'complete'
                AND gi.id IN (
                    SELECT MAX(id)

                    FROM generated_images

                    WHERE
                        job_id = ?
                        AND status = 'complete'

                    GROUP BY prompt_id
                )

            ORDER BY
                COALESCE(
                    gp.position,
                    gi.id
                ) ASC

            LIMIT ?
            """,
            (
                job_id,
                job_id,
                limit,
            ),
        ).fetchall()

        if rows:
            return [
                {
                    "type":
                        "generated",
                    "url":
                        f"/api/images/{row['id']}/file",
                }
                for row in rows
            ]

        rows = connection.execute(
            """
            SELECT
                id,
                position

            FROM reference_images

            WHERE job_id = ?

            ORDER BY position ASC

            LIMIT ?
            """,
            (
                job_id,
                limit,
            ),
        ).fetchall()

        return [
            {
                "type":
                    "reference",
                "url":
                    (
                        f"/api/jobs/{job_id}"
                        f"/references/{row['id']}/file"
                    ),
            }
            for row in rows
        ]

    finally:
        connection.close()


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
                _thumbnail_urls(
                    int(
                        item["id"]
                    )
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
                id,
                name

            FROM generation_profiles

            WHERE
                owner_id = ?
                OR (
                    owner_id IS NULL
                    AND name IN (
                        'Hero Images',
                        'UGC Images'
                    )
                )

            ORDER BY name ASC
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

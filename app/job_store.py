from pathlib import Path
import threading
import uuid

from app.database import get_connection
from app.builtin_workflows import (
    is_builtin_workflow_name,
    load_builtin_instruction,
)
from app.managed_workflow_service import (
    get_managed_workflow_instruction,
)
from app.request_context import (
    get_current_owner_id,
    LOCAL_OWNER_ID,
)
from app.platform.storage_backend import (
    get_storage_backend,
    media_type_for_filename,
)


BASE_DIR = Path(__file__).resolve().parent.parent

STORAGE = get_storage_backend(
    BASE_DIR
)

DATA_DIR = STORAGE.data_dir
UPLOADS_DIR = STORAGE.uploads_dir

MAX_IMAGE_BYTES = 20 * 1024 * 1024

SUPPORTED_JOB_ASPECT_RATIOS = {
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
}


_SCHEMA_READY = False
_SCHEMA_LOCK = threading.RLock()


def detect_image_type(data: bytes):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return {
            "extension": ".png",
            "media_type": "image/png",
        }

    if data.startswith(b"\xff\xd8\xff"):
        return {
            "extension": ".jpg",
            "media_type": "image/jpeg",
        }

    if (
        len(data) >= 12
        and data[0:4] == b"RIFF"
        and data[8:12] == b"WEBP"
    ):
        return {
            "extension": ".webp",
            "media_type": "image/webp",
        }

    return None


def media_type_for_storage(
    storage_ref: str,
    original_filename: str = "",
):
    name = original_filename or storage_ref
    return media_type_for_filename(name)


def normalize_job_aspect_ratio(
    value: str | None,
):
    normalized = (
        value
        or
        "1:1"
    ).strip()

    if (
        normalized
        not in
        SUPPORTED_JOB_ASPECT_RATIOS
    ):
        return "1:1"

    return normalized


def resolve_openai_size_for_ratio(
    aspect_ratio: str,
):
    portrait = {
        "2:3",
        "3:4",
        "4:5",
        "9:16",
    }

    landscape = {
        "3:2",
        "4:3",
        "5:4",
        "16:9",
    }

    if aspect_ratio in portrait:
        return "1024x1536"

    if aspect_ratio in landscape:
        return "1536x1024"

    return "1024x1024"


def build_generation_snapshot(
    runtime_settings: dict,
    aspect_ratio: str,
):
    aspect_ratio = (
        normalize_job_aspect_ratio(
            aspect_ratio
        )
    )

    planner_provider = (
        runtime_settings.get(
            "planner_provider",
            "gemini",
        )
    )

    image_provider = (
        runtime_settings.get(
            "image_provider",
            "openai",
        )
    )

    if planner_provider == "openai":
        planner_model = (
            runtime_settings.get(
                "openai_planner_model",
                "gpt-5.6-luna",
            )
        )

        planner_reasoning = (
            runtime_settings.get(
                "openai_planner_reasoning",
                "low",
            )
        )

    else:
        planner_model = (
            runtime_settings.get(
                "gemini_planner_model",
                "gemini-3.6-flash",
            )
        )

        planner_reasoning = None

    if image_provider == "openai":
        image_model = (
            runtime_settings.get(
                "openai_image_model",
                "gpt-image-2",
            )
        )

        image_quality = (
            runtime_settings.get(
                "openai_image_quality",
                "low",
            )
        )

        image_size = (
            resolve_openai_size_for_ratio(
                aspect_ratio
            )
        )

        image_output_format = (
            runtime_settings.get(
                "openai_image_output_format",
                "jpeg",
            )
        )

    else:
        image_model = (
            runtime_settings.get(
                "gemini_image_model",
                "gemini-3.1-flash-image",
            )
        )

        image_quality = None

        image_size = (
            runtime_settings.get(
                "gemini_image_size",
                "1K",
            )
        )

        image_output_format = None

    try:
        batch_concurrency = int(
            runtime_settings.get(
                "batch_concurrency",
                2,
            )
        )
    except (
        TypeError,
        ValueError,
    ):
        batch_concurrency = 2

    batch_concurrency = max(
        1,
        min(
            batch_concurrency,
            4,
        ),
    )

    return {
        "aspect_ratio":
            aspect_ratio,
        "planner_tier_snapshot":
            runtime_settings.get(
                "planner_tier",
                "economy",
            ),
        "planner_provider_snapshot":
            planner_provider,
        "planner_model_snapshot":
            planner_model,
        "planner_reasoning_snapshot":
            planner_reasoning,
        "image_tier_snapshot":
            runtime_settings.get(
                "image_tier",
                "economy",
            ),
        "image_provider_snapshot":
            image_provider,
        "image_model_snapshot":
            image_model,
        "image_quality_snapshot":
            image_quality,
        "image_size_snapshot":
            image_size,
        "image_output_format_snapshot":
            image_output_format,
        "batch_concurrency_snapshot":
            batch_concurrency,
    }


def ensure_job_schema(force: bool = False):
    global _SCHEMA_READY

    if _SCHEMA_READY and not force:
        return

    with _SCHEMA_LOCK:
        if _SCHEMA_READY and not force:
            return

        connection = get_connection()

        try:
            columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(generation_jobs)"
                ).fetchall()
            }

            additions = {
                "owner_id":
                    "TEXT",
                "aspect_ratio":
                    "TEXT",
                "planner_tier_snapshot":
                    "TEXT",
                "planner_provider_snapshot":
                    "TEXT",
                "planner_model_snapshot":
                    "TEXT",
                "planner_reasoning_snapshot":
                    "TEXT",
                "image_tier_snapshot":
                    "TEXT",
                "image_provider_snapshot":
                    "TEXT",
                "image_model_snapshot":
                    "TEXT",
                "image_quality_snapshot":
                    "TEXT",
                "image_size_snapshot":
                    "TEXT",
                "image_output_format_snapshot":
                    "TEXT",
                "batch_concurrency_snapshot":
                    "INTEGER",
            }

            for name, type_name in (
                additions.items()
            ):
                if name in columns:
                    continue

                connection.execute(
                    f"""
                    ALTER TABLE generation_jobs
                    ADD COLUMN {name} {type_name}
                    """
                )

            connection.execute(
                """
                UPDATE generation_jobs
                SET owner_id = ?
                WHERE owner_id IS NULL
                """,
                (
                    LOCAL_OWNER_ID,
                ),
            )

            connection.commit()

        finally:
            connection.close()

        _SCHEMA_READY = True


def create_prepared_job(
    profile_id: int,
    description: str,
    requested_count: str,
    uploads: list[dict],
    aspect_ratio: str = "1:1",
    runtime_settings: dict | None = None,
):
    ensure_job_schema()

    connection = get_connection()

    owner_id = (
        get_current_owner_id()
    )

    try:
        profile = connection.execute(
            """
            SELECT
                gp.id,
                gp.name,
                gp.active_version_id,
                pv.version_number,
                pv.system_instruction,
                mw.workflow_type
                    AS managed_workflow_type,
                mw.status
                    AS managed_status
            FROM generation_profiles gp

            JOIN profile_versions pv
                ON pv.id = gp.active_version_id

            LEFT JOIN managed_workflows mw
                ON mw.profile_id = gp.id

            WHERE
                gp.id = ?
                AND gp.is_active = 1
                AND (
                    gp.owner_id = ?
                    OR (
                        gp.owner_id IS NULL
                        AND mw.status = 'published'
                    )
                )
            """,
            (
                profile_id,
                owner_id,
            ),
        ).fetchone()

        if profile is None:
            return {
                "status":
                    "profile_unavailable"
            }

        if profile[
            "managed_workflow_type"
        ]:
            system_instruction = (
                get_managed_workflow_instruction(
                    profile[
                        "id"
                    ],
                    profile[
                        "active_version_id"
                    ],
                )
            )

            if not system_instruction:
                return {
                    "status":
                        "managed_instruction_missing",
                    "profile_name":
                        profile["name"],
                }

        elif is_builtin_workflow_name(
            profile["name"]
        ):
            # Compatibility fallback for pre-managed Hero / UGC records.
            system_instruction = (
                load_builtin_instruction(
                    profile["name"]
                )
            )

            if not system_instruction:
                return {
                    "status":
                        "builtin_instruction_missing",
                    "profile_name":
                        profile["name"],
                }

        else:
            system_instruction = (
                profile[
                    "system_instruction"
                ]
            )

        snapshots = (
            build_generation_snapshot(
                runtime_settings
                or
                {},
                aspect_ratio,
            )
        )

        cursor = connection.execute(
            """
            INSERT INTO generation_jobs (
                owner_id,
                profile_id,
                profile_version_id,
                description,
                requested_count,
                aspect_ratio,
                planner_tier_snapshot,
                planner_provider_snapshot,
                planner_model_snapshot,
                planner_reasoning_snapshot,
                image_tier_snapshot,
                image_provider_snapshot,
                image_model_snapshot,
                image_quality_snapshot,
                image_size_snapshot,
                image_output_format_snapshot,
                batch_concurrency_snapshot,
                status,
                system_instruction_snapshot
            )
            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?
            )
            """,
            (
                owner_id,
                profile_id,
                profile[
                    "active_version_id"
                ],
                description,
                requested_count,
                snapshots[
                    "aspect_ratio"
                ],
                snapshots[
                    "planner_tier_snapshot"
                ],
                snapshots[
                    "planner_provider_snapshot"
                ],
                snapshots[
                    "planner_model_snapshot"
                ],
                snapshots[
                    "planner_reasoning_snapshot"
                ],
                snapshots[
                    "image_tier_snapshot"
                ],
                snapshots[
                    "image_provider_snapshot"
                ],
                snapshots[
                    "image_model_snapshot"
                ],
                snapshots[
                    "image_quality_snapshot"
                ],
                snapshots[
                    "image_size_snapshot"
                ],
                snapshots[
                    "image_output_format_snapshot"
                ],
                snapshots[
                    "batch_concurrency_snapshot"
                ],
                "prepared",
                system_instruction,
            ),
        )

        job_id = cursor.lastrowid

        for position, upload in enumerate(
            uploads,
            start=1,
        ):
            stored_filename = (
                f"{position:02d}_"
                f"{uuid.uuid4().hex[:12]}"
                f"{upload['extension']}"
            )

            storage_ref = STORAGE.write_reference(
                owner_id=owner_id,
                job_id=job_id,
                filename=stored_filename,
                data=upload["data"],
                media_type=upload["media_type"],
            )

            connection.execute(
                """
                INSERT INTO reference_images (
                    job_id,
                    position,
                    original_filename,
                    stored_filename,
                    file_path
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    job_id,
                    position,
                    upload["original_filename"],
                    stored_filename,
                    storage_ref,
                ),
            )

        connection.commit()

    except Exception:
        connection.rollback()

        try:
            if "job_id" in locals():
                STORAGE.delete_job_objects(
                    owner_id,
                    job_id,
                )
        except Exception:
            pass

        raise

    finally:
        connection.close()

    return {
        "status": "created",
        "job": get_job(
            job_id
        ),
    }


def get_job(
    job_id: int,
):
    ensure_job_schema()
    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        job = connection.execute(
            """
            SELECT
                gj.id,
                gj.owner_id,
                gj.profile_id,
                gj.profile_version_id,
                gj.description,
                gj.requested_count,
                gj.aspect_ratio,
                gj.planner_tier_snapshot,
                gj.planner_provider_snapshot,
                gj.planner_model_snapshot,
                gj.planner_reasoning_snapshot,
                gj.image_tier_snapshot,
                gj.image_provider_snapshot,
                gj.image_model_snapshot,
                gj.image_quality_snapshot,
                gj.image_size_snapshot,
                gj.image_output_format_snapshot,
                gj.batch_concurrency_snapshot,
                gj.status,
                gj.planner_provider,
                gj.planner_model,
                gj.planner_raw_output,
                gj.planner_error,
                gj.planned_at,
                gj.created_at,
                gj.updated_at,
                gp.name AS profile_name,
                pv.version_number
                    AS profile_version_number,
                LENGTH(
                    gj.system_instruction_snapshot
                )
                    AS system_instruction_characters
            FROM generation_jobs gj
            JOIN generation_profiles gp
                ON gp.id = gj.profile_id
            JOIN profile_versions pv
                ON pv.id =
                    gj.profile_version_id
            WHERE
                gj.id = ?
                AND gj.owner_id = ?
            """,
            (
                job_id,
                owner_id,
            ),
        ).fetchone()

        if job is None:
            return None

        references = connection.execute(
            """
            SELECT
                id,
                position,
                original_filename,
                stored_filename,
                file_path,
                created_at
            FROM reference_images
            WHERE job_id = ?
            ORDER BY position ASC
            """,
            (job_id,),
        ).fetchall()

        result = dict(
            job
        )

        result[
            "references"
        ] = [
            {
                "id": reference["id"],
                "position": reference["position"],
                "original_filename": reference["original_filename"],
                "stored_filename": reference["stored_filename"],
                "created_at": reference["created_at"],
                "file_url": (
                    f"/api/jobs/{job_id}"
                    f"/references/"
                    f"{reference['id']}/file"
                ),
            }
            for reference in references
        ]

        result[
            "reference_count"
        ] = len(
            result[
                "references"
            ]
        )

        return result

    finally:
        connection.close()


def get_job_for_planning(
    job_id: int,
):
    ensure_job_schema()
    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        job = connection.execute(
            """
            SELECT
                id,
                owner_id,
                profile_id,
                profile_version_id,
                description,
                requested_count,
                aspect_ratio,
                planner_provider_snapshot,
                planner_model_snapshot,
                planner_reasoning_snapshot,
                image_provider_snapshot,
                image_model_snapshot,
                image_quality_snapshot,
                image_size_snapshot,
                image_output_format_snapshot,
                batch_concurrency_snapshot,
                status,
                system_instruction_snapshot
            FROM generation_jobs
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                job_id,
                owner_id,
            ),
        ).fetchone()

        if job is None:
            return None

        references = connection.execute(
            """
            SELECT
                id,
                position,
                original_filename,
                file_path
            FROM reference_images
            WHERE job_id = ?
            ORDER BY position ASC
            """,
            (job_id,),
        ).fetchall()

        result = dict(
            job
        )

        result[
            "references"
        ] = []

        for reference in references:
            storage_ref = reference["file_path"]

            if not STORAGE.exists(storage_ref):
                raise FileNotFoundError(
                    "Reference image is missing: "
                    f"{reference['original_filename']}"
                )

            result["references"].append(
                {
                    **dict(reference),
                    "storage_ref": storage_ref,
                    "data": STORAGE.read_bytes(storage_ref),
                    "media_type": media_type_for_storage(
                        storage_ref,
                        reference["original_filename"],
                    ),
                    "absolute_path": STORAGE.local_path(storage_ref),
                }
            )


        return result

    finally:
        connection.close()


def mark_job_planning(
    job_id: int,
    model: str,
    provider: str = "gemini",
):
    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'planning',
                planner_provider = ?,
                planner_model = ?,
                planner_error = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                provider,
                model,
                job_id,
                owner_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def mark_job_planned(
    job_id: int,
    model: str,
    raw_output: str,
    provider: str = "gemini",
):
    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'planned_raw',
                planner_provider = ?,
                planner_model = ?,
                planner_raw_output = ?,
                planner_error = NULL,
                planned_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                provider,
                model,
                raw_output,
                job_id,
                owner_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def mark_job_planning_failed(
    job_id: int,
    model: str,
    error_message: str,
    provider: str = "gemini",
):
    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'planning_failed',
                planner_provider = ?,
                planner_model = ?,
                planner_error = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                provider,
                model,
                error_message[
                    :2000
                ],
                job_id,
                owner_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_reference_file(
    job_id: int,
    reference_id: int,
):
    connection = get_connection()
    owner_id = get_current_owner_id()

    try:
        row = connection.execute(
            """
            SELECT
                ri.id,
                ri.job_id,
                ri.original_filename,
                ri.stored_filename,
                ri.file_path
            FROM reference_images ri
            JOIN generation_jobs gj
                ON gj.id = ri.job_id
            WHERE
                ri.id = ?
                AND ri.job_id = ?
                AND gj.owner_id = ?
            """,
            (reference_id, job_id, owner_id),
        ).fetchone()

        if row is None:
            return None

        storage_ref = row["file_path"]
        if not STORAGE.exists(storage_ref):
            return None

        return {
            "storage_ref": storage_ref,
            "path": STORAGE.local_path(storage_ref),
            "signed_url": STORAGE.signed_get_url(storage_ref),
            "media_type": media_type_for_storage(
                storage_ref,
                row["original_filename"],
            ),
            "original_filename": row["original_filename"],
        }

    finally:
        connection.close()


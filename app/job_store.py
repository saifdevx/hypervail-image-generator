from pathlib import Path
import shutil
import uuid

from app.database import get_connection
from app.builtin_workflows import (
    is_builtin_workflow_name,
    load_builtin_instruction,
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"

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


def media_type_for_path(path: Path):
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(
        path.suffix.lower(),
        "application/octet-stream",
    )


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
        "planner_provider_snapshot":
            planner_provider,
        "planner_model_snapshot":
            planner_model,
        "planner_reasoning_snapshot":
            planner_reasoning,
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


def ensure_job_schema():
    connection = get_connection()

    try:
        columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(generation_jobs)"
            ).fetchall()
        }

        additions = {
            "aspect_ratio":
                "TEXT",
            "planner_provider_snapshot":
                "TEXT",
            "planner_model_snapshot":
                "TEXT",
            "planner_reasoning_snapshot":
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

        connection.commit()

    finally:
        connection.close()


def create_prepared_job(
    profile_id: int,
    description: str,
    requested_count: str,
    uploads: list[dict],
    aspect_ratio: str = "1:1",
    runtime_settings: dict | None = None,
):
    ensure_job_schema()

    UPLOADS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = get_connection()
    job_directory = None

    try:
        profile = connection.execute(
            """
            SELECT
                gp.id,
                gp.name,
                gp.active_version_id,
                pv.version_number,
                pv.system_instruction
            FROM generation_profiles gp
            JOIN profile_versions pv
                ON pv.id = gp.active_version_id
            WHERE
                gp.id = ?
                AND gp.is_active = 1
            """,
            (profile_id,),
        ).fetchone()

        if profile is None:
            return {
                "status":
                    "profile_unavailable"
            }

        if is_builtin_workflow_name(
            profile["name"]
        ):
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
            )
            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?
            )
            """,
            (
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
                    "planner_provider_snapshot"
                ],
                snapshots[
                    "planner_model_snapshot"
                ],
                snapshots[
                    "planner_reasoning_snapshot"
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

        job_directory = (
            UPLOADS_DIR
            /
            f"job_{job_id:06d}"
        )

        job_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        for position, upload in enumerate(
            uploads,
            start=1,
        ):
            stored_filename = (
                f"{position:02d}_"
                f"{uuid.uuid4().hex[:12]}"
                f"{upload['extension']}"
            )

            stored_path = (
                job_directory
                /
                stored_filename
            )

            stored_path.write_bytes(
                upload["data"]
            )

            relative_path = (
                stored_path
                .relative_to(
                    BASE_DIR
                )
                .as_posix()
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
                    upload[
                        "original_filename"
                    ],
                    stored_filename,
                    relative_path,
                ),
            )

        connection.commit()

    except Exception:
        connection.rollback()

        if (
            job_directory is not None
            and job_directory.exists()
        ):
            shutil.rmtree(
                job_directory,
                ignore_errors=True,
            )

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

    try:
        job = connection.execute(
            """
            SELECT
                gj.id,
                gj.profile_id,
                gj.profile_version_id,
                gj.description,
                gj.requested_count,
                gj.aspect_ratio,
                gj.planner_provider_snapshot,
                gj.planner_model_snapshot,
                gj.planner_reasoning_snapshot,
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
            WHERE gj.id = ?
            """,
            (job_id,),
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
                **dict(
                    reference
                ),
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

    try:
        job = connection.execute(
            """
            SELECT
                id,
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
            WHERE id = ?
            """,
            (job_id,),
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

        uploads_root = (
            UPLOADS_DIR.resolve()
        )

        for reference in references:
            path = (
                BASE_DIR
                /
                reference[
                    "file_path"
                ]
            ).resolve()

            if (
                path != uploads_root
                and
                uploads_root
                not in path.parents
            ):
                raise RuntimeError(
                    "Reference path escaped uploads directory."
                )

            if not path.exists():
                raise FileNotFoundError(
                    "Reference image is missing: "
                    f"{reference['original_filename']}"
                )

            result[
                "references"
            ].append(
                {
                    **dict(
                        reference
                    ),
                    "absolute_path":
                        path,
                    "media_type":
                        media_type_for_path(
                            path
                        ),
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
            WHERE id = ?
            """,
            (
                provider,
                model,
                job_id,
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
            WHERE id = ?
            """,
            (
                provider,
                model,
                raw_output,
                job_id,
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
            WHERE id = ?
            """,
            (
                provider,
                model,
                error_message[
                    :2000
                ],
                job_id,
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
            WHERE
                ri.id = ?
                AND ri.job_id = ?
            """,
            (
                reference_id,
                job_id,
            ),
        ).fetchone()

        if row is None:
            return None

        path = (
            BASE_DIR
            /
            row[
                "file_path"
            ]
        ).resolve()

        uploads_root = (
            UPLOADS_DIR.resolve()
        )

        if (
            path != uploads_root
            and
            uploads_root
            not in path.parents
        ):
            return None

        if not path.exists():
            return None

        return {
            "path":
                path,
            "media_type":
                media_type_for_path(
                    path
                ),
            "original_filename":
                row[
                    "original_filename"
                ],
        }

    finally:
        connection.close()

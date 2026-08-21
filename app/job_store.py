from pathlib import Path
import shutil
import uuid

from app.database import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"

MAX_IMAGE_BYTES = 20 * 1024 * 1024


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


def create_prepared_job(
    profile_id: int,
    description: str,
    requested_count: str,
    uploads: list[dict],
):
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

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
            return {"status": "profile_unavailable"}

        cursor = connection.execute(
            """
            INSERT INTO generation_jobs (
                profile_id,
                profile_version_id,
                description,
                requested_count,
                status,
                system_instruction_snapshot
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                profile_id,
                profile["active_version_id"],
                description,
                requested_count,
                "prepared",
                profile["system_instruction"],
            ),
        )

        job_id = cursor.lastrowid
        job_directory = UPLOADS_DIR / f"job_{job_id:06d}"
        job_directory.mkdir(parents=True, exist_ok=True)

        for position, upload in enumerate(uploads, start=1):
            stored_filename = (
                f"{position:02d}_"
                f"{uuid.uuid4().hex[:12]}"
                f"{upload['extension']}"
            )

            stored_path = job_directory / stored_filename
            stored_path.write_bytes(upload["data"])

            relative_path = (
                stored_path
                .relative_to(BASE_DIR)
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
                    upload["original_filename"],
                    stored_filename,
                    relative_path,
                ),
            )

        connection.commit()

    except Exception:
        connection.rollback()

        if job_directory is not None and job_directory.exists():
            shutil.rmtree(job_directory, ignore_errors=True)

        raise

    finally:
        connection.close()

    return {
        "status": "created",
        "job": get_job(job_id),
    }


def get_job(job_id: int):
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
                gj.status,
                gj.planner_model,
                gj.planner_raw_output,
                gj.planner_error,
                gj.planned_at,
                gj.created_at,
                gj.updated_at,
                gp.name AS profile_name,
                pv.version_number AS profile_version_number,
                LENGTH(gj.system_instruction_snapshot)
                    AS system_instruction_characters
            FROM generation_jobs gj
            JOIN generation_profiles gp
                ON gp.id = gj.profile_id
            JOIN profile_versions pv
                ON pv.id = gj.profile_version_id
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

        result = dict(job)

        result["references"] = [
            {
                **dict(reference),
                "file_url": (
                    f"/api/jobs/{job_id}"
                    f"/references/{reference['id']}/file"
                ),
            }
            for reference in references
        ]

        result["reference_count"] = len(result["references"])
        return result

    finally:
        connection.close()


def get_job_for_planning(job_id: int):
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

        result = dict(job)
        result["references"] = []

        uploads_root = UPLOADS_DIR.resolve()

        for reference in references:
            path = (BASE_DIR / reference["file_path"]).resolve()

            if path != uploads_root and uploads_root not in path.parents:
                raise RuntimeError(
                    "Reference path escaped uploads directory."
                )

            if not path.exists():
                raise FileNotFoundError(
                    "Reference image is missing: "
                    f"{reference['original_filename']}"
                )

            result["references"].append(
                {
                    **dict(reference),
                    "absolute_path": path,
                    "media_type": media_type_for_path(path),
                }
            )

        return result

    finally:
        connection.close()


def mark_job_planning(job_id: int, model: str):
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'planning',
                planner_model = ?,
                planner_error = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (model, job_id),
        )
        connection.commit()

    finally:
        connection.close()


def mark_job_planned(
    job_id: int,
    model: str,
    raw_output: str,
):
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'planned_raw',
                planner_model = ?,
                planner_raw_output = ?,
                planner_error = NULL,
                planned_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
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
):
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'planning_failed',
                planner_model = ?,
                planner_error = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                model,
                error_message[:2000],
                job_id,
            ),
        )
        connection.commit()

    finally:
        connection.close()


def get_reference_file(job_id: int, reference_id: int):
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
            (reference_id, job_id),
        ).fetchone()

        if row is None:
            return None

        path = (BASE_DIR / row["file_path"]).resolve()
        uploads_root = UPLOADS_DIR.resolve()

        if path != uploads_root and uploads_root not in path.parents:
            return None

        if not path.exists():
            return None

        return {
            "path": path,
            "media_type": media_type_for_path(path),
            "original_filename": row["original_filename"],
        }

    finally:
        connection.close()

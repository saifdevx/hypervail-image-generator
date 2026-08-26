import shutil
from pathlib import Path

from app.database import get_connection
from app.job_store import (
    BASE_DIR,
    DATA_DIR,
    UPLOADS_DIR,
)
from app.request_context import (
    get_current_owner_id,
)
from app.platform.storage_backend import (
    get_storage_backend,
)


STORAGE = get_storage_backend(
    BASE_DIR
)

OUTPUTS_DIR = DATA_DIR / "outputs"


def _safe_delete_file(
    path_value: str | None,
    allowed_root: Path,
):
    if not path_value:
        return False

    path = (
        BASE_DIR
        /
        path_value
    ).resolve()

    root = (
        allowed_root
        .resolve()
    )

    if (
        path != root
        and
        root not in path.parents
    ):
        return False

    if not path.exists():
        return False

    if path.is_file():
        path.unlink(
            missing_ok=True
        )

        return True

    return False


def delete_generated_image(
    image_id: int,
):
    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        row = connection.execute(
            """
            SELECT
                gi.id,
                gi.job_id,
                gi.file_path
            FROM generated_images gi

            JOIN generation_jobs gj
                ON gj.id =
                    gi.job_id

            WHERE
                gi.id = ?
                AND gj.owner_id = ?
            """,
            (
                image_id,
                owner_id,
            ),
        ).fetchone()

        if row is None:
            return None

        connection.execute(
            """
            DELETE FROM generated_images
            WHERE id = ?
            """,
            (
                image_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()

    deleted_file = (
        STORAGE.delete(
            row["file_path"]
        )
        if row["file_path"]
        else False
    )

    return {
        "image_id":
            image_id,
        "job_id":
            row[
                "job_id"
            ],
        "deleted":
            True,
        "file_deleted":
            deleted_file,
    }


def delete_job(
    job_id: int,
):
    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        job = connection.execute(
            """
            SELECT id
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

        connection.execute(
            """
            DELETE FROM generated_images
            WHERE job_id = ?
            """,
            (
                job_id,
            ),
        )

        connection.execute(
            """
            DELETE FROM generated_prompts
            WHERE job_id = ?
            """,
            (
                job_id,
            ),
        )

        connection.execute(
            """
            DELETE FROM reference_images
            WHERE job_id = ?
            """,
            (
                job_id,
            ),
        )

        connection.execute(
            """
            DELETE FROM generation_jobs
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                job_id,
                owner_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()

    try:
        STORAGE.delete_job_objects(
            owner_id,
            job_id,
        )
    except Exception:
        pass

    return {
        "job_id":
            job_id,
        "deleted":
            True,
    }


def recover_stale_generations(
    stale_minutes: int = 30,
):
    stale_minutes = max(
        5,
        min(
            int(
                stale_minutes
            ),
            1440,
        ),
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE generated_images
            SET
                status = 'failed',
                error_message = ?
            WHERE
                status IN (
                    'queued',
                    'generating'
                )
                AND datetime(created_at)
                    <
                    datetime(
                        'now',
                        ?
                    )
            """,
            (
                (
                    "Generation was interrupted or stale. "
                    "Retry this image."
                ),
                f"-{stale_minutes} minutes",
            ),
        )

        recovered = (
            cursor.rowcount
        )

        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'images_partial_failed',
                updated_at = CURRENT_TIMESTAMP
            WHERE
                status = 'images_generating'
                AND NOT EXISTS (
                    SELECT 1
                    FROM generated_images gi
                    WHERE
                        gi.job_id =
                            generation_jobs.id
                        AND gi.status IN (
                            'queued',
                            'generating'
                        )
                )
            """
        )

        connection.commit()

    finally:
        connection.close()

    return {
        "stale_images_marked_failed":
            recovered,
    }


def cleanup_orphan_directories():
    if STORAGE.name != "local":
        return {
            "removed_count": 0,
            "removed": [],
            "note": "R2 objects are deleted with their jobs; local orphan scan skipped.",
        }

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT id
            FROM generation_jobs
            """
        ).fetchall()

    finally:
        connection.close()

    known = {
        int(
            row[
                "id"
            ]
        )
        for row in rows
    }

    removed = []

    for root in (
        UPLOADS_DIR,
        OUTPUTS_DIR,
    ):
        if not root.exists():
            continue

        for child in root.iterdir():
            if not child.is_dir():
                continue

            name = child.name

            if not name.startswith(
                "job_"
            ):
                continue

            try:
                job_id = int(
                    name[
                        4:
                    ]
                )
            except ValueError:
                continue

            if job_id in known:
                continue

            shutil.rmtree(
                child,
                ignore_errors=True,
            )

            removed.append(
                child
                .relative_to(
                    BASE_DIR
                )
                .as_posix()
            )

    return {
        "removed_count":
            len(
                removed
            ),
        "removed":
            removed,
    }

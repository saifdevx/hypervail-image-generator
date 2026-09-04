import secrets
import threading

from app.database import get_connection


_SCHEMA_READY = False
_SCHEMA_LOCK = threading.RLock()


VALID_TASK_TYPES = {
    "generate_all",
    "generate_one",
    "regenerate_one",
}


VALID_TASK_STATUSES = {
    "queued",
    "running",
    "completed",
    "failed",
}


def ensure_queue_task_schema(force: bool = False):
    global _SCHEMA_READY

    if _SCHEMA_READY and not force:
        return

    with _SCHEMA_LOCK:
        if _SCHEMA_READY and not force:
            return

        connection = get_connection()

        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS generation_queue_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL UNIQUE,
                    job_id INTEGER NOT NULL,
                    user_id TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    prompt_id INTEGER,
                    status TEXT NOT NULL DEFAULT 'queued',
                    attempts INTEGER NOT NULL DEFAULT 0,
                    error_message TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_generation_queue_tasks_job
                ON generation_queue_tasks(job_id, id DESC)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_generation_queue_tasks_user
                ON generation_queue_tasks(user_id, id DESC)
                """
            )

            connection.commit()
            _SCHEMA_READY = True

        finally:
            connection.close()


def new_queue_task_id():
    return secrets.token_urlsafe(24)


def _clean_task_type(value: str):
    task_type = str(value or "").strip().lower()

    if task_type not in VALID_TASK_TYPES:
        raise ValueError("Unsupported queue task type.")

    return task_type


def create_queue_task(task: dict):
    ensure_queue_task_schema()

    task_id = str(
        task.get("task_id")
        or
        ""
    ).strip()

    user_id = str(
        task.get("user_id")
        or
        ""
    ).strip()

    if not task_id:
        raise ValueError("Queue task_id is required.")

    if not user_id:
        raise ValueError("Queue user_id is required.")

    job_id = int(task.get("job_id"))
    prompt_id = task.get("prompt_id")

    if prompt_id is not None:
        prompt_id = int(prompt_id)

    task_type = _clean_task_type(
        task.get("task")
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO generation_queue_tasks (
                task_id,
                job_id,
                user_id,
                task_type,
                prompt_id,
                status
            )
            VALUES (?, ?, ?, ?, ?, 'queued')
            """,
            (
                task_id,
                job_id,
                user_id,
                task_type,
                prompt_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()

    return get_queue_task(task_id)


def get_queue_task(task_id: str):
    ensure_queue_task_schema()
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT *
            FROM generation_queue_tasks
            WHERE task_id = ?
            """,
            (task_id,),
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def get_latest_job_queue_task(job_id: int):
    ensure_queue_task_schema()
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT *
            FROM generation_queue_tasks
            WHERE job_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (int(job_id),),
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def claim_queue_task(
    task_id: str,
    job_id: int,
    user_id: str,
):
    """
    Atomically claim a queued/retried task.

    Completed tasks are never executed again. A failed task may be claimed
    again because Cloudflare can retry delivery after a transient Render or
    network error.
    """

    ensure_queue_task_schema()
    connection = get_connection()

    try:
        row = connection.execute(
            """
            UPDATE generation_queue_tasks
            SET
                status = 'running',
                attempts = attempts + 1,
                error_message = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                task_id = ?
                AND job_id = ?
                AND user_id = ?
                AND status IN ('queued', 'failed')
            RETURNING *
            """,
            (
                task_id,
                int(job_id),
                str(user_id),
            ),
        ).fetchone()

        connection.commit()

        if row:
            return {
                "status": "claimed",
                "task": dict(row),
            }

        existing = connection.execute(
            """
            SELECT *
            FROM generation_queue_tasks
            WHERE task_id = ?
            """,
            (task_id,),
        ).fetchone()

        if existing is None:
            return {
                "status": "not_found",
                "task": None,
            }

        existing = dict(existing)

        if (
            int(existing.get("job_id") or 0)
            != int(job_id)
            or
            str(existing.get("user_id") or "")
            != str(user_id)
        ):
            return {
                "status": "mismatch",
                "task": existing,
            }

        return {
            "status": str(existing.get("status") or "blocked"),
            "task": existing,
        }

    finally:
        connection.close()


def mark_queue_task_completed(task_id: str):
    ensure_queue_task_schema()
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generation_queue_tasks
            SET
                status = 'completed',
                error_message = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE task_id = ?
            """,
            (task_id,),
        )

        connection.commit()

    finally:
        connection.close()


def mark_queue_task_failed(
    task_id: str,
    error_message: str,
):
    ensure_queue_task_schema()
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generation_queue_tasks
            SET
                status = 'failed',
                error_message = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE task_id = ?
            """,
            (
                str(error_message or "Queue task failed.")[:2000],
                task_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()

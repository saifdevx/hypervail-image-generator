from app.database import get_connection
from app.user_service import list_users
from app.model_registry import list_models
from app.auth_service import get_auth_provider, auth_is_configured
from app.platform.database_backend import (
    get_database_provider,
    database_is_configured,
)
from app.platform.storage_backend import (
    get_storage_provider,
    storage_is_configured,
)
from app.platform.queue_backend import (
    get_queue_provider,
    queue_is_configured,
)


def get_admin_overview():
    connection = get_connection()

    try:
        users = int((connection.execute(
            "SELECT COUNT(*) AS count FROM app_users"
        ).fetchone()["count"] or 0))

        jobs = int((connection.execute(
            "SELECT COUNT(*) AS count FROM generation_jobs"
        ).fetchone()["count"] or 0))

        today_jobs = int((connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM generation_jobs
            WHERE date(created_at) = date('now')
            """
        ).fetchone()["count"] or 0))

        complete_images = int((connection.execute(
            "SELECT COUNT(*) AS count FROM generated_images WHERE status = 'complete'"
        ).fetchone()["count"] or 0))

        failed_images = int((connection.execute(
            "SELECT COUNT(*) AS count FROM generated_images WHERE status = 'failed'"
        ).fetchone()["count"] or 0))

        attempted_images = complete_images + failed_images
        success_rate = (
            round((complete_images / attempted_images) * 100, 1)
            if attempted_images
            else 100.0
        )

        return {
            "users": users,
            "jobs": jobs,
            "jobs_today": today_jobs,
            "complete_images": complete_images,
            "failed_images": failed_images,
            "success_rate": success_rate,
        }

    finally:
        connection.close()


def get_recent_failures(limit: int = 12):
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                gi.id AS image_id,
                gi.job_id,
                gi.provider,
                gi.error_message,
                gi.created_at,
                au.email AS user_email,
                gj.image_model_snapshot AS model
            FROM generated_images gi
            JOIN generation_jobs gj
                ON gj.id = gi.job_id
            LEFT JOIN app_users au
                ON au.user_id = gj.owner_id
            WHERE gi.status = 'failed'
            ORDER BY gi.id DESC
            LIMIT ?
            """,
            (max(1, min(int(limit), 50)),),
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def get_system_status():
    return {
        "auth": {
            "label": "Firebase Auth" if get_auth_provider() == "firebase" else "Local Auth",
            "provider": get_auth_provider(),
            "configured": auth_is_configured(),
        },
        "database": {
            "label": "Turso" if get_database_provider() == "turso" else "SQLite",
            "provider": get_database_provider(),
            "configured": database_is_configured(),
        },
        "storage": {
            "label": "Cloudflare R2" if get_storage_provider() == "r2" else "Local Files",
            "provider": get_storage_provider(),
            "configured": storage_is_configured(),
        },
        "queue": {
            "label": "Cloudflare Queues" if get_queue_provider() == "cloudflare" else "Local Runner",
            "provider": get_queue_provider(),
            "configured": queue_is_configured(),
        },
    }


def get_admin_dashboard():
    return {
        "overview": get_admin_overview(),
        "users": list_users(limit=100),
        "models": list_models(),
        "system": get_system_status(),
        "recent_failures": get_recent_failures(),
    }

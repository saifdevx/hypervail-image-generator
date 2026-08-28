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
from app.managed_workflow_service import (
    get_workflow_summary,
    list_admin_workflows,
)


def get_admin_overview():
    connection = get_connection()

    try:
        # Keep the Admin overview to one Turso round-trip. The previous
        # implementation issued five sequential COUNT queries; that was fine
        # for local SQLite but multiplied network latency in the cloud.
        row = connection.execute(
            """
            SELECT
                (
                    SELECT COUNT(*)
                    FROM app_users
                ) AS users,
                (
                    SELECT COUNT(*)
                    FROM generation_jobs
                ) AS jobs,
                (
                    SELECT COUNT(*)
                    FROM generation_jobs
                    WHERE date(created_at) = date('now')
                ) AS jobs_today,
                (
                    SELECT COUNT(*)
                    FROM generated_images
                    WHERE status = 'complete'
                ) AS complete_images,
                (
                    SELECT COUNT(*)
                    FROM generated_images
                    WHERE status = 'failed'
                ) AS failed_images
            """
        ).fetchone()

        users = int(row["users"] or 0)
        jobs = int(row["jobs"] or 0)
        today_jobs = int(row["jobs_today"] or 0)
        complete_images = int(row["complete_images"] or 0)
        failed_images = int(row["failed_images"] or 0)

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
    workflow_summary = (
        get_workflow_summary()
    )

    return {
        "overview": {
            **get_admin_overview(),
            "workflows":
                workflow_summary[
                    "total"
                ],
            "published_workflows":
                workflow_summary[
                    "published"
                ],
        },
        "users": list_users(limit=100),
        "models": list_models(),
        "workflows":
            list_admin_workflows(),
        "workflow_summary":
            workflow_summary,
        "system": get_system_status(),
        "recent_failures": get_recent_failures(),
    }

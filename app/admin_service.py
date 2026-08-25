from app.database import get_connection
from app.user_service import (
    list_users,
)
from app.model_registry import (
    list_models,
)
from app.feature_flags import (
    list_feature_flags,
)


def get_admin_overview():
    connection = get_connection()

    try:
        users = connection.execute(
            """
            SELECT COUNT(*)
                AS count
            FROM app_users
            """
        ).fetchone()[
            "count"
        ]

        jobs = connection.execute(
            """
            SELECT COUNT(*)
                AS count
            FROM generation_jobs
            """
        ).fetchone()[
            "count"
        ]

        complete_images = connection.execute(
            """
            SELECT COUNT(*)
                AS count
            FROM generated_images
            WHERE status = 'complete'
            """
        ).fetchone()[
            "count"
        ]

        failed_images = connection.execute(
            """
            SELECT COUNT(*)
                AS count
            FROM generated_images
            WHERE status = 'failed'
            """
        ).fetchone()[
            "count"
        ]

        today_jobs = connection.execute(
            """
            SELECT COUNT(*)
                AS count
            FROM generation_jobs
            WHERE
                date(created_at)
                =
                date('now')
            """
        ).fetchone()[
            "count"
        ]

        return {
            "users":
                int(
                    users
                    or
                    0
                ),
            "jobs":
                int(
                    jobs
                    or
                    0
                ),
            "jobs_today":
                int(
                    today_jobs
                    or
                    0
                ),
            "complete_images":
                int(
                    complete_images
                    or
                    0
                ),
            "failed_images":
                int(
                    failed_images
                    or
                    0
                ),
        }

    finally:
        connection.close()


def get_admin_dashboard():
    return {
        "overview":
            get_admin_overview(),
        "users":
            list_users(
                limit=100
            ),
        "models":
            list_models(),
        "feature_flags":
            list_feature_flags(),
    }

import os

from app.database import get_connection
from app.request_context import (
    LOCAL_OWNER_ID,
)


VALID_ROLES = {
    "user",
    "support",
    "admin",
}

VALID_STATUSES = {
    "active",
    "suspended",
}


def ensure_user_schema():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS app_users (
                user_id TEXT PRIMARY KEY,
                email TEXT,
                display_name TEXT,
                role TEXT NOT NULL
                    DEFAULT 'user',
                status TEXT NOT NULL
                    DEFAULT 'active',
                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                last_seen_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_app_users_email
            ON app_users(email)
            """
        )

        connection.commit()

    finally:
        connection.close()


def _bootstrap_admin_uid():
    return (
        os.getenv(
            "HYPEREX_ADMIN_UID"
        )
        or
        ""
    ).strip()


def _bootstrap_admin_email():
    """
    Legacy/local bootstrap fallback only.

    For Firebase mode, Hyperex should use HYPEREX_ADMIN_UID so an
    unverified email string alone can never grant administrator access.
    """
    return (
        os.getenv(
            "HYPEREX_ADMIN_EMAIL"
        )
        or
        ""
    ).strip().lower()


def _allow_email_admin_bootstrap():
    return (
        os.getenv(
            "ALLOW_EMAIL_ADMIN_BOOTSTRAP",
            "false",
        )
        or
        "false"
    ).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def ensure_user(
    user_id: str,
    email: str | None = None,
):
    ensure_user_schema()

    clean_email = (
        email
        or
        ""
    ).strip()

    role = "user"

    if user_id == LOCAL_OWNER_ID:
        role = "admin"

    admin_uid = (
        _bootstrap_admin_uid()
    )

    if (
        admin_uid
        and
        user_id
        ==
        admin_uid
    ):
        role = "admin"

    elif _allow_email_admin_bootstrap():
        admin_email = (
            _bootstrap_admin_email()
        )

        if (
            admin_email
            and
            clean_email.lower()
            ==
            admin_email
        ):
            role = "admin"

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT OR IGNORE INTO app_users (
                user_id,
                email,
                role,
                status
            )
            VALUES (?, ?, ?, 'active')
            """,
            (
                user_id,
                clean_email,
                role,
            ),
        )

        if clean_email:
            connection.execute(
                """
                UPDATE app_users
                SET
                    email = ?,
                    last_seen_at =
                        CURRENT_TIMESTAMP
                WHERE user_id = ?
                """,
                (
                    clean_email,
                    user_id,
                ),
            )

        if role == "admin":
            connection.execute(
                """
                UPDATE app_users
                SET role = 'admin'
                WHERE user_id = ?
                """,
                (
                    user_id,
                ),
            )

        connection.commit()

        row = connection.execute(
            """
            SELECT *
            FROM app_users
            WHERE user_id = ?
            """,
            (
                user_id,
            ),
        ).fetchone()

        return (
            dict(
                row
            )
            if row
            else
            None
        )

    finally:
        connection.close()


def get_user(
    user_id: str,
):
    ensure_user_schema()
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT *
            FROM app_users
            WHERE user_id = ?
            """,
            (
                user_id,
            ),
        ).fetchone()

        return (
            dict(
                row
            )
            if row
            else
            None
        )

    finally:
        connection.close()


def list_users(
    limit: int = 100,
):
    ensure_user_schema()
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                u.user_id,
                u.email,
                u.display_name,
                u.role,
                u.status,
                u.created_at,
                u.last_seen_at,

                (
                    SELECT COUNT(*)
                    FROM generation_jobs gj
                    WHERE
                        gj.owner_id =
                            u.user_id
                )
                    AS job_count,

                (
                    SELECT COUNT(*)
                    FROM generated_images gi
                    JOIN generation_jobs gj
                        ON gj.id =
                            gi.job_id
                    WHERE
                        gj.owner_id =
                            u.user_id
                        AND gi.status =
                            'complete'
                )
                    AS image_count

            FROM app_users u

            ORDER BY
                u.created_at DESC

            LIMIT ?
            """,
            (
                max(
                    1,
                    min(
                        int(
                            limit
                        ),
                        500,
                    ),
                ),
            ),
        ).fetchall()

        return [
            dict(
                row
            )
            for row in rows
        ]

    finally:
        connection.close()


def update_user_access(
    user_id: str,
    role: str | None = None,
    status: str | None = None,
):
    ensure_user_schema()

    if (
        role is not None
        and
        role not in VALID_ROLES
    ):
        raise ValueError(
            "Unsupported role."
        )

    if (
        status is not None
        and
        status not in VALID_STATUSES
    ):
        raise ValueError(
            "Unsupported user status."
        )

    updates = []
    params = []

    if role is not None:
        updates.append(
            "role = ?"
        )
        params.append(
            role
        )

    if status is not None:
        updates.append(
            "status = ?"
        )
        params.append(
            status
        )

    if not updates:
        return get_user(
            user_id
        )

    params.append(
        user_id
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            f"""
            UPDATE app_users
            SET
                {", ".join(updates)}
            WHERE user_id = ?
            """,
            tuple(
                params
            ),
        )

        connection.commit()

        if cursor.rowcount < 1:
            return None

    finally:
        connection.close()

    return get_user(
        user_id
    )


def user_is_admin(
    user_id: str,
):
    user = get_user(
        user_id
    )

    return bool(
        user
        and
        user.get(
            "role"
        )
        ==
        "admin"
        and
        user.get(
            "status"
        )
        ==
        "active"
    )

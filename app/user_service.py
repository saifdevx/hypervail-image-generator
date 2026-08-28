import os
import threading
import time

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


# Schema migrations belong to process startup, not the hot request path.
# SQLite made repeated CREATE/INDEX checks effectively invisible, but every
# statement becomes a network round-trip once DATABASE_PROVIDER=turso.
_SCHEMA_READY = False
_SCHEMA_LOCK = threading.RLock()

# A short per-process cache removes duplicate app_users reads while one page
# loads several API requests. Admin role/status changes invalidate this cache
# immediately in the process that performs the change. A short TTL also keeps
# multi-worker deployments eventually consistent without making auth depend on
# a long-lived cache.
_USER_CACHE = {}
_USER_CACHE_LOCK = threading.RLock()
_USER_CACHE_TTL_SECONDS = 10.0


def _cache_user(user):
    if not user:
        return

    payload = dict(user)
    user_id = str(payload.get("user_id") or "")

    if not user_id:
        return

    with _USER_CACHE_LOCK:
        _USER_CACHE[user_id] = (
            time.monotonic(),
            payload,
        )


def _cached_user(user_id: str):
    clean_id = str(user_id or "")
    if not clean_id:
        return None

    with _USER_CACHE_LOCK:
        entry = _USER_CACHE.get(clean_id)
        if entry is None:
            return None

        cached_at, payload = entry
        if (time.monotonic() - cached_at) > _USER_CACHE_TTL_SECONDS:
            _USER_CACHE.pop(clean_id, None)
            return None

        return dict(payload)


def _invalidate_user_cache(user_id: str):
    with _USER_CACHE_LOCK:
        _USER_CACHE.pop(str(user_id or ""), None)


def ensure_user_schema(force: bool = False):
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
            _SCHEMA_READY = True

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
        # One UPSERT replaces the old INSERT + UPDATE + optional role UPDATE
        # + SELECT sequence. This matters for a remote Turso database because
        # each SQL statement is a network round-trip. Existing suspension state
        # and non-admin roles are preserved; bootstrap admins are only promoted.
        row = connection.execute(
            """
            INSERT INTO app_users (
                user_id,
                email,
                role,
                status
            )
            VALUES (?, ?, ?, 'active')
            ON CONFLICT(user_id)
            DO UPDATE SET
                email = CASE
                    WHEN excluded.email != ''
                        THEN excluded.email
                    ELSE app_users.email
                END,
                last_seen_at = CURRENT_TIMESTAMP,
                role = CASE
                    WHEN excluded.role = 'admin'
                        THEN 'admin'
                    ELSE app_users.role
                END
            RETURNING *
            """,
            (
                user_id,
                clean_email,
                role,
            ),
        ).fetchone()

        connection.commit()

        result = (
            dict(row)
            if row
            else
            None
        )
        _cache_user(result)
        return result

    finally:
        connection.close()


def get_user(
    user_id: str,
):
    ensure_user_schema()

    cached = _cached_user(user_id)
    if cached is not None:
        return cached

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

        result = (
            dict(row)
            if row
            else
            None
        )
        _cache_user(result)
        return result

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
        row = connection.execute(
            f"""
            UPDATE app_users
            SET
                {", ".join(updates)}
            WHERE user_id = ?
            RETURNING *
            """,
            tuple(
                params
            ),
        ).fetchone()

        connection.commit()

        result = (
            dict(row)
            if row
            else
            None
        )

        if result is None:
            _invalidate_user_cache(
                user_id
            )
            return None

        _cache_user(result)
        return result

    finally:
        connection.close()


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

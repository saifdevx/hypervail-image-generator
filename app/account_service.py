from app.database import get_connection
from app.request_context import (
    LOCAL_OWNER_ID,
    get_current_owner_id,
)
from app.user_service import (
    user_is_admin,
)


SYSTEM_OWNER_ID = "__hyperex_system__"
IMPORT_MARKER_KEY = "local_data_import_completed_v1"


def _row_value(
    row,
    key: str,
    default=0,
):
    if row is None:
        return default

    try:
        return row[
            key
        ]
    except Exception:
        return default


def _get_import_marker(
    connection,
):
    return connection.execute(
        """
        SELECT
            value,
            updated_at
        FROM app_settings
        WHERE
            owner_id = ?
            AND key = ?
        LIMIT 1
        """,
        (
            SYSTEM_OWNER_ID,
            IMPORT_MARKER_KEY,
        ),
    ).fetchone()


def _local_data_counts(
    connection,
):
    profiles = int(
        _row_value(
            connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM generation_profiles
                WHERE owner_id = ?
                """,
                (
                    LOCAL_OWNER_ID,
                ),
            ).fetchone(),
            "count",
            0,
        )
        or
        0
    )

    jobs = int(
        _row_value(
            connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM generation_jobs
                WHERE owner_id = ?
                """,
                (
                    LOCAL_OWNER_ID,
                ),
            ).fetchone(),
            "count",
            0,
        )
        or
        0
    )

    references = int(
        _row_value(
            connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM reference_images ri
                JOIN generation_jobs gj
                    ON gj.id = ri.job_id
                WHERE gj.owner_id = ?
                """,
                (
                    LOCAL_OWNER_ID,
                ),
            ).fetchone(),
            "count",
            0,
        )
        or
        0
    )

    images = int(
        _row_value(
            connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM generated_images gi
                JOIN generation_jobs gj
                    ON gj.id = gi.job_id
                WHERE gj.owner_id = ?
                """,
                (
                    LOCAL_OWNER_ID,
                ),
            ).fetchone(),
            "count",
            0,
        )
        or
        0
    )

    settings = int(
        _row_value(
            connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM app_settings
                WHERE owner_id = ?
                """,
                (
                    LOCAL_OWNER_ID,
                ),
            ).fetchone(),
            "count",
            0,
        )
        or
        0
    )

    provider_connections = int(
        _row_value(
            connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM provider_credentials
                WHERE owner_key = ?
                """,
                (
                    LOCAL_OWNER_ID,
                ),
            ).fetchone(),
            "count",
            0,
        )
        or
        0
    )

    return {
        "profiles":
            profiles,
        "jobs":
            jobs,
        "references":
            references,
        "images":
            images,
        "settings":
            settings,
        "provider_connections":
            provider_connections,
    }


def _has_importable_data(
    counts: dict,
):
    return any(
        int(
            counts.get(
                key,
                0,
            )
            or
            0
        )
        >
        0
        for key in (
            "profiles",
            "jobs",
            "settings",
            "provider_connections",
        )
    )


def get_local_data_import_status():
    """
    Preview the old pre-Firebase local data that can be transferred.

    Security rules:
    - Only an active Hyperex admin may import.
    - The migration is permanently marked after a successful transfer.
    - Hero / UGC built-ins are not local-owned records and are not moved.
    """
    owner_id = (
        get_current_owner_id()
    )

    is_admin = (
        owner_id
        !=
        LOCAL_OWNER_ID
        and
        user_is_admin(
            owner_id
        )
    )

    connection = get_connection()

    try:
        marker = (
            _get_import_marker(
                connection
            )
        )

        counts = (
            _local_data_counts(
                connection
            )
        )

        completed = (
            marker is not None
        )

        available = bool(
            is_admin
            and
            not completed
            and
            _has_importable_data(
                counts
            )
        )

        return {
            "admin_only":
                True,
            "is_admin":
                bool(
                    is_admin
                ),
            "available":
                available,
            "completed":
                completed,
            "completed_at":
                (
                    _row_value(
                        marker,
                        "updated_at",
                        None,
                    )
                    if marker
                    else
                    None
                ),
            "counts":
                counts,
        }

    finally:
        connection.close()


def claim_local_data():
    """
    One-time migration of the old single-user owner ('local') into the
    currently signed-in Hyperex administrator.

    Associated references, prompts, generated images and favorites remain
    attached to their jobs/images, so moving generation_jobs ownership moves
    access to those records without rewriting every child row.
    """
    owner_id = (
        get_current_owner_id()
    )

    if (
        owner_id
        ==
        LOCAL_OWNER_ID
        or
        not user_is_admin(
            owner_id
        )
    ):
        raise PermissionError(
            "Administrator access required."
        )

    connection = get_connection()

    try:
        marker = (
            _get_import_marker(
                connection
            )
        )

        if marker is not None:
            return {
                "claimed":
                    False,
                "reason":
                    "already_completed",
                "counts":
                    _local_data_counts(
                        connection
                    ),
            }

        before = (
            _local_data_counts(
                connection
            )
        )

        if not _has_importable_data(
            before
        ):
            return {
                "claimed":
                    False,
                "reason":
                    "no_local_data",
                "counts":
                    before,
            }

        profile_cursor = (
            connection.execute(
                """
                UPDATE generation_profiles
                SET owner_id = ?
                WHERE owner_id = ?
                """,
                (
                    owner_id,
                    LOCAL_OWNER_ID,
                ),
            )
        )

        job_cursor = (
            connection.execute(
                """
                UPDATE generation_jobs
                SET owner_id = ?
                WHERE owner_id = ?
                """,
                (
                    owner_id,
                    LOCAL_OWNER_ID,
                ),
            )
        )

        # Preserve the old single-user runtime settings by copying them
        # into the importing admin account. If the admin already has a
        # value for the same key, the old local value intentionally wins
        # because this tool exists specifically to migrate the old setup.
        connection.execute(
            """
            INSERT INTO app_settings (
                owner_id,
                key,
                value,
                updated_at
            )
            SELECT
                ?,
                key,
                value,
                updated_at
            FROM app_settings
            WHERE owner_id = ?

            ON CONFLICT(
                owner_id,
                key
            )
            DO UPDATE SET
                value =
                    excluded.value,
                updated_at =
                    excluded.updated_at
            """,
            (
                owner_id,
                LOCAL_OWNER_ID,
            ),
        )

        connection.execute(
            """
            DELETE FROM app_settings
            WHERE owner_id = ?
            """,
            (
                LOCAL_OWNER_ID,
            ),
        )

        # Migrate encrypted BYOK connections in the same way.
        connection.execute(
            """
            INSERT INTO provider_credentials (
                owner_key,
                provider,
                encrypted_key,
                key_suffix,
                created_at,
                updated_at
            )
            SELECT
                ?,
                provider,
                encrypted_key,
                key_suffix,
                created_at,
                updated_at
            FROM provider_credentials
            WHERE owner_key = ?

            ON CONFLICT(
                owner_key,
                provider
            )
            DO UPDATE SET
                encrypted_key =
                    excluded.encrypted_key,
                key_suffix =
                    excluded.key_suffix,
                updated_at =
                    excluded.updated_at
            """,
            (
                owner_id,
                LOCAL_OWNER_ID,
            ),
        )

        connection.execute(
            """
            DELETE FROM provider_credentials
            WHERE owner_key = ?
            """,
            (
                LOCAL_OWNER_ID,
            ),
        )

        # Permanent one-time marker. It uses the existing app_settings
        # table so no new database schema/migration is introduced.
        connection.execute(
            """
            INSERT INTO app_settings (
                owner_id,
                key,
                value,
                updated_at
            )
            VALUES (
                ?,
                ?,
                ?,
                CURRENT_TIMESTAMP
            )

            ON CONFLICT(
                owner_id,
                key
            )
            DO NOTHING
            """,
            (
                SYSTEM_OWNER_ID,
                IMPORT_MARKER_KEY,
                owner_id,
            ),
        )

        connection.commit()

        return {
            "claimed":
                True,
            "reason":
                "completed",
            "profiles":
                int(
                    profile_cursor.rowcount
                    or
                    0
                ),
            "jobs":
                int(
                    job_cursor.rowcount
                    or
                    0
                ),
            "counts":
                before,
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

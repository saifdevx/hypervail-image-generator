from app.database import get_connection
from app.request_context import (
    LOCAL_OWNER_ID,
    get_current_owner_id,
)


def claim_local_data():
    owner_id = (
        get_current_owner_id()
    )

    if owner_id == LOCAL_OWNER_ID:
        return {
            "claimed":
                False,
            "reason":
                "already_local",
        }

    connection = get_connection()

    try:
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

        # Move local settings only when that key does not already
        # exist for the signed-in user.
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

        # Same pattern for encrypted provider keys.
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

        connection.commit()

        return {
            "claimed":
                True,
            "profiles":
                profile_cursor.rowcount,
            "jobs":
                job_cursor.rowcount,
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

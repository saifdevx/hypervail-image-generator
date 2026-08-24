import os
from pathlib import Path

from cryptography.fernet import (
    Fernet,
    InvalidToken,
)

from app.database import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOCAL_KEY_FILE = DATA_DIR / ".credential_key"

OWNER_KEY = "local"

SUPPORTED_PROVIDERS = {
    "openai",
    "gemini",
}


def ensure_credential_schema():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS
            provider_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_key TEXT NOT NULL,
                provider TEXT NOT NULL,
                encrypted_key TEXT NOT NULL,
                key_suffix TEXT NOT NULL,
                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(owner_key, provider)
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def _clean_provider(
    provider: str,
):
    value = (
        provider
        .strip()
        .lower()
    )

    if value not in SUPPORTED_PROVIDERS:
        raise ValueError(
            "Unsupported provider."
        )

    return value


def _load_or_create_master_key():
    env_value = (
        os.getenv(
            "APP_ENCRYPTION_KEY"
        )
        or
        ""
    ).strip()

    if env_value:
        key = env_value.encode(
            "utf-8"
        )

        # Raises ValueError if malformed.
        Fernet(
            key
        )

        return key

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if LOCAL_KEY_FILE.exists():
        key = (
            LOCAL_KEY_FILE
            .read_text(
                encoding="utf-8"
            )
            .strip()
            .encode(
                "utf-8"
            )
        )

        Fernet(
            key
        )

        return key

    key = Fernet.generate_key()

    LOCAL_KEY_FILE.write_text(
        key.decode(
            "utf-8"
        ),
        encoding="utf-8",
    )

    try:
        os.chmod(
            LOCAL_KEY_FILE,
            0o600,
        )
    except OSError:
        pass

    return key


def _fernet():
    return Fernet(
        _load_or_create_master_key()
    )


def save_provider_api_key(
    provider: str,
    api_key: str,
):
    ensure_credential_schema()

    provider = _clean_provider(
        provider
    )

    clean_key = (
        api_key
        .strip()
        .strip('"')
        .strip("'")
    )

    if len(clean_key) < 8:
        raise ValueError(
            "API key looks too short."
        )

    encrypted = (
        _fernet()
        .encrypt(
            clean_key.encode(
                "utf-8"
            )
        )
        .decode(
            "utf-8"
        )
    )

    suffix = clean_key[
        -4:
    ]

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO provider_credentials (
                owner_key,
                provider,
                encrypted_key,
                key_suffix,
                updated_at
            )
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)

            ON CONFLICT(owner_key, provider)
            DO UPDATE SET
                encrypted_key = excluded.encrypted_key,
                key_suffix = excluded.key_suffix,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                OWNER_KEY,
                provider,
                encrypted,
                suffix,
            ),
        )

        connection.commit()

    finally:
        connection.close()

    return {
        "provider":
            provider,
        "saved":
            True,
        "key_suffix":
            suffix,
    }


def get_saved_provider_api_key(
    provider: str,
):
    ensure_credential_schema()

    provider = _clean_provider(
        provider
    )

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT encrypted_key
            FROM provider_credentials
            WHERE
                owner_key = ?
                AND provider = ?
            """,
            (
                OWNER_KEY,
                provider,
            ),
        ).fetchone()

    finally:
        connection.close()

    if row is None:
        return None

    try:
        return (
            _fernet()
            .decrypt(
                row[
                    "encrypted_key"
                ].encode(
                    "utf-8"
                )
            )
            .decode(
                "utf-8"
            )
        )

    except InvalidToken:
        return None


def remove_provider_api_key(
    provider: str,
):
    ensure_credential_schema()

    provider = _clean_provider(
        provider
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM provider_credentials
            WHERE
                owner_key = ?
                AND provider = ?
            """,
            (
                OWNER_KEY,
                provider,
            ),
        )

        connection.commit()

        return {
            "provider":
                provider,
            "removed":
                cursor.rowcount > 0,
        }

    finally:
        connection.close()


def get_saved_connection_status():
    ensure_credential_schema()

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                provider,
                key_suffix,
                created_at,
                updated_at
            FROM provider_credentials
            WHERE owner_key = ?
            """,
            (
                OWNER_KEY,
            ),
        ).fetchall()

    finally:
        connection.close()

    by_provider = {
        row[
            "provider"
        ]:
            dict(
                row
            )
        for row in rows
    }

    return {
        provider: {
            "saved":
                provider
                in
                by_provider,
            "key_suffix":
                (
                    by_provider[
                        provider
                    ][
                        "key_suffix"
                    ]
                    if provider
                    in
                    by_provider
                    else
                    None
                ),
            "updated_at":
                (
                    by_provider[
                        provider
                    ][
                        "updated_at"
                    ]
                    if provider
                    in
                    by_provider
                    else
                    None
                ),
        }
        for provider
        in sorted(
            SUPPORTED_PROVIDERS
        )
    }

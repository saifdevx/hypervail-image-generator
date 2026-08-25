from app.database import get_connection


DEFAULT_FLAGS = [
    (
        "admin_panel",
        True,
        "Show the Hyperex admin dashboard to administrators.",
    ),
    (
        "model_tiers",
        True,
        "Expose Economy / Balanced / Best Quality model tiers.",
    ),
    (
        "device_cache",
        False,
        "Future local device image cache / privacy mode.",
    ),
    (
        "cloud_queue",
        False,
        "Future Cloudflare Queues generation runner.",
    ),
    (
        "cloud_storage",
        False,
        "Future Cloudflare R2 image storage.",
    ),
]


def ensure_feature_flag_schema():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS feature_flags (
                key TEXT PRIMARY KEY,
                enabled INTEGER NOT NULL DEFAULT 0,
                description TEXT,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        for (
            key,
            enabled,
            description,
        ) in DEFAULT_FLAGS:
            connection.execute(
                """
                INSERT OR IGNORE INTO feature_flags (
                    key,
                    enabled,
                    description
                )
                VALUES (?, ?, ?)
                """,
                (
                    key,
                    1
                    if enabled
                    else
                    0,
                    description,
                ),
            )

        connection.commit()

    finally:
        connection.close()


def list_feature_flags():
    ensure_feature_flag_schema()
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT *
            FROM feature_flags
            ORDER BY key ASC
            """
        ).fetchall()

        return [
            {
                **dict(
                    row
                ),
                "enabled":
                    bool(
                        row[
                            "enabled"
                        ]
                    ),
            }
            for row in rows
        ]

    finally:
        connection.close()


def get_feature_flag(
    key: str,
    default: bool = False,
):
    ensure_feature_flag_schema()
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT enabled
            FROM feature_flags
            WHERE key = ?
            """,
            (
                key,
            ),
        ).fetchone()

        if row is None:
            return default

        return bool(
            row[
                "enabled"
            ]
        )

    finally:
        connection.close()


def set_feature_flag(
    key: str,
    enabled: bool,
):
    ensure_feature_flag_schema()
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE feature_flags
            SET
                enabled = ?,
                updated_at =
                    CURRENT_TIMESTAMP
            WHERE key = ?
            """,
            (
                1
                if enabled
                else
                0,
                key,
            ),
        )

        connection.commit()

        if cursor.rowcount < 1:
            return None

    finally:
        connection.close()

    return {
        "key":
            key,
        "enabled":
            bool(
                enabled
            ),
    }

import json

from app.database import get_connection
from app.request_context import (
    get_current_owner_id,
)


def ensure_usage_schema():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS usage_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                job_id INTEGER,
                provider TEXT,
                model TEXT,
                quantity INTEGER NOT NULL DEFAULT 1,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_usage_events_user
            ON usage_events(
                user_id,
                created_at
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def record_usage(
    event_type: str,
    job_id: int | None = None,
    provider: str | None = None,
    model: str | None = None,
    quantity: int = 1,
    metadata: dict | None = None,
):
    ensure_usage_schema()

    user_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO usage_events (
                user_id,
                event_type,
                job_id,
                provider,
                model,
                quantity,
                metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                event_type,
                job_id,
                provider,
                model,
                max(
                    1,
                    int(
                        quantity
                    ),
                ),
                json.dumps(
                    metadata
                    or
                    {}
                ),
            ),
        )

        connection.commit()

    finally:
        connection.close()


def user_usage_summary(
    user_id: str | None = None,
):
    ensure_usage_schema()

    user_id = (
        user_id
        or
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                event_type,
                SUM(quantity)
                    AS total
            FROM usage_events
            WHERE user_id = ?
            GROUP BY event_type
            """,
            (
                user_id,
            ),
        ).fetchall()

        return {
            row[
                "event_type"
            ]:
                int(
                    row[
                        "total"
                    ]
                    or
                    0
                )
            for row in rows
        }

    finally:
        connection.close()

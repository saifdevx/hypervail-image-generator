import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "image_agent.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def column_exists(connection, table_name: str, column_name: str):
    rows = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    return any(
        row["name"] == column_name
        for row in rows
    )


def add_column_if_missing(
    connection,
    table_name: str,
    column_name: str,
    column_sql: str,
):
    if not column_exists(
        connection,
        table_name,
        column_name,
    ):
        connection.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name} {column_sql}
            """
        )


def run_migrations(connection):
    # Active profile-version support from Step 4C.1.
    add_column_if_missing(
        connection,
        "generation_profiles",
        "active_version_id",
        "INTEGER",
    )

    connection.execute(
        """
        UPDATE generation_profiles

        SET active_version_id = (
            SELECT pv.id
            FROM profile_versions pv
            WHERE pv.profile_id = generation_profiles.id
            ORDER BY pv.version_number DESC
            LIMIT 1
        )

        WHERE active_version_id IS NULL
        """
    )

    # Step 7: raw Gemini planner state.
    add_column_if_missing(
        connection,
        "generation_jobs",
        "planner_model",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "planner_raw_output",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "planner_error",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "planned_at",
        "TEXT",
    )

    connection.commit()


def init_database():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generation_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                description TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                active_version_id INTEGER,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS profile_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                version_number INTEGER NOT NULL,
                system_instruction TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (profile_id)
                    REFERENCES generation_profiles(id)
                    ON DELETE CASCADE,

                UNIQUE(profile_id, version_number)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generation_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                profile_version_id INTEGER NOT NULL,
                description TEXT,
                requested_count TEXT NOT NULL DEFAULT 'auto',
                status TEXT NOT NULL DEFAULT 'pending',
                system_instruction_snapshot TEXT NOT NULL,
                planner_model TEXT,
                planner_raw_output TEXT,
                planner_error TEXT,
                planned_at TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (profile_id)
                    REFERENCES generation_profiles(id),

                FOREIGN KEY (profile_version_id)
                    REFERENCES profile_versions(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reference_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                position INTEGER NOT NULL,
                original_filename TEXT NOT NULL,
                stored_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (job_id)
                    REFERENCES generation_jobs(id)
                    ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generated_prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                position INTEGER NOT NULL,
                title TEXT,
                prompt_text TEXT NOT NULL,
                metadata_json TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (job_id)
                    REFERENCES generation_jobs(id)
                    ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generated_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                prompt_id INTEGER,
                provider TEXT,
                file_path TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                error_message TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (job_id)
                    REFERENCES generation_jobs(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (prompt_id)
                    REFERENCES generated_prompts(id)
                    ON DELETE SET NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_profile_versions_profile
            ON profile_versions(profile_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_generation_jobs_profile
            ON generation_jobs(profile_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_generation_jobs_version
            ON generation_jobs(profile_version_id)
            """
        )

        connection.commit()
        run_migrations(connection)

        print(f"Database ready: {DATABASE_PATH}")

    finally:
        connection.close()


def get_database_status():
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        tables = [
            row["name"]
            for row in rows
        ]

        return {
            "status": "connected",
            "database": DATABASE_PATH.name,
            "tables": tables,
            "table_count": len(tables),
        }

    finally:
        connection.close()

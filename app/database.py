from pathlib import Path

from app.platform.database_backend import (
    get_database_backend,
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "image_agent.db"

LOCAL_OWNER_ID = "local"


def get_connection():
    backend = (
        get_database_backend(
            DATABASE_PATH
        )
    )

    return backend.connect()


def column_exists(
    connection,
    table_name: str,
    column_name: str,
):
    rows = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    return any(
        row["name"]
        ==
        column_name
        for row in rows
    )


def add_column_if_missing(
    connection,
    table_name: str,
    column_name: str,
    column_sql: str,
):
    if column_exists(
        connection,
        table_name,
        column_name,
    ):
        return

    connection.execute(
        f"""
        ALTER TABLE {table_name}
        ADD COLUMN {column_name} {column_sql}
        """
    )


def _ensure_phase_columns(
    connection,
):
    # Profiles / jobs
    add_column_if_missing(
        connection,
        "generation_profiles",
        "active_version_id",
        "INTEGER",
    )

    add_column_if_missing(
        connection,
        "generation_profiles",
        "owner_id",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "owner_id",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "planner_provider",
        "TEXT",
    )

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

    # Step 8 structured state.
    add_column_if_missing(
        connection,
        "generation_jobs",
        "normalizer_model",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "structured_output_json",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "normalizer_error",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "normalized_at",
        "TEXT",
    )

    # Step 13 snapshots.
    add_column_if_missing(
        connection,
        "generation_jobs",
        "aspect_ratio",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "planner_provider_snapshot",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "planner_model_snapshot",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "planner_reasoning_snapshot",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "image_provider_snapshot",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "image_model_snapshot",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "image_quality_snapshot",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "image_size_snapshot",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "image_output_format_snapshot",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generation_jobs",
        "batch_concurrency_snapshot",
        "INTEGER",
    )

    # Step 12 / 13 image fields.
    add_column_if_missing(
        connection,
        "generation_jobs",
        "is_favorite",
        "INTEGER NOT NULL DEFAULT 0",
    )

    add_column_if_missing(
        connection,
        "generated_images",
        "generation_note",
        "TEXT",
    )

    add_column_if_missing(
        connection,
        "generated_images",
        "is_favorite",
        "INTEGER NOT NULL DEFAULT 0",
    )


def _migrate_existing_ownership(
    connection,
):
    # Existing single-user custom profiles become local-owner data.
    # Built-in and Admin-managed workflows stay global (owner_id NULL).
    managed_workflows_exist = (
        connection.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE
                type = 'table'
                AND name = 'managed_workflows'
            LIMIT 1
            """
        ).fetchone()
        is not None
    )

    if managed_workflows_exist:
        connection.execute(
            """
            UPDATE generation_profiles
            SET owner_id = ?
            WHERE
                owner_id IS NULL
                AND name NOT IN (
                    'Hero Images',
                    'UGC Images'
                )
                AND id NOT IN (
                    SELECT profile_id
                    FROM managed_workflows
                )
            """,
            (
                LOCAL_OWNER_ID,
            ),
        )

        connection.execute(
            """
            UPDATE generation_profiles
            SET owner_id = NULL
            WHERE
                name IN (
                    'Hero Images',
                    'UGC Images'
                )
                OR id IN (
                    SELECT profile_id
                    FROM managed_workflows
                )
            """
        )
    else:
        connection.execute(
            """
            UPDATE generation_profiles
            SET owner_id = ?
            WHERE
                owner_id IS NULL
                AND name NOT IN (
                    'Hero Images',
                    'UGC Images'
                )
            """,
            (
                LOCAL_OWNER_ID,
            ),
        )

        connection.execute(
            """
            UPDATE generation_profiles
            SET owner_id = NULL
            WHERE name IN (
                'Hero Images',
                'UGC Images'
            )
            """
        )

    connection.execute(
        """
        UPDATE generation_jobs
        SET owner_id = ?
        WHERE owner_id IS NULL
        """,
        (
            LOCAL_OWNER_ID,
        ),
    )


def run_migrations(
    connection,
):
    _ensure_phase_columns(
        connection
    )

    connection.execute(
        """
        UPDATE generation_profiles
        SET active_version_id = (
            SELECT pv.id
            FROM profile_versions pv
            WHERE
                pv.profile_id =
                    generation_profiles.id
            ORDER BY
                pv.version_number DESC
            LIMIT 1
        )
        WHERE active_version_id IS NULL
        """
    )

    _migrate_existing_ownership(
        connection
    )

    connection.execute(
        """
        UPDATE generation_jobs
        SET aspect_ratio = '1:1'
        WHERE
            aspect_ratio IS NULL
            OR TRIM(aspect_ratio) = ''
        """
    )

    connection.commit()


def init_database():
    connection = get_connection()

    try:
        cursor = (
            connection.cursor()
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            generation_profiles (
                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,
                owner_id TEXT,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                description TEXT,
                is_active INTEGER
                    NOT NULL DEFAULT 1,
                active_version_id INTEGER,
                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            profile_versions (
                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                version_number INTEGER NOT NULL,
                system_instruction TEXT NOT NULL,
                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (
                    profile_id
                )
                    REFERENCES
                    generation_profiles(id)
                    ON DELETE CASCADE,

                UNIQUE(
                    profile_id,
                    version_number
                )
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            generation_jobs (
                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,
                owner_id TEXT,
                profile_id INTEGER NOT NULL,
                profile_version_id INTEGER NOT NULL,
                description TEXT,
                requested_count TEXT
                    NOT NULL DEFAULT 'auto',
                aspect_ratio TEXT
                    NOT NULL DEFAULT '1:1',
                status TEXT
                    NOT NULL DEFAULT 'pending',
                system_instruction_snapshot TEXT
                    NOT NULL,

                planner_provider TEXT,
                planner_model TEXT,
                planner_raw_output TEXT,
                planner_error TEXT,
                planned_at TEXT,

                normalizer_model TEXT,
                structured_output_json TEXT,
                normalizer_error TEXT,
                normalized_at TEXT,

                planner_provider_snapshot TEXT,
                planner_model_snapshot TEXT,
                planner_reasoning_snapshot TEXT,

                image_provider_snapshot TEXT,
                image_model_snapshot TEXT,
                image_quality_snapshot TEXT,
                image_size_snapshot TEXT,
                image_output_format_snapshot TEXT,
                batch_concurrency_snapshot INTEGER,

                is_favorite INTEGER
                    NOT NULL DEFAULT 0,

                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (
                    profile_id
                )
                    REFERENCES
                    generation_profiles(id),

                FOREIGN KEY (
                    profile_version_id
                )
                    REFERENCES
                    profile_versions(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            reference_images (
                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                position INTEGER NOT NULL,
                original_filename TEXT NOT NULL,
                stored_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (
                    job_id
                )
                    REFERENCES
                    generation_jobs(id)
                    ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            generated_prompts (
                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                position INTEGER NOT NULL,
                title TEXT,
                prompt_text TEXT NOT NULL,
                metadata_json TEXT,
                status TEXT
                    NOT NULL DEFAULT 'pending',
                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (
                    job_id
                )
                    REFERENCES
                    generation_jobs(id)
                    ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            generated_images (
                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                prompt_id INTEGER,
                provider TEXT,
                file_path TEXT,
                status TEXT
                    NOT NULL DEFAULT 'pending',
                error_message TEXT,
                generation_note TEXT,
                is_favorite INTEGER
                    NOT NULL DEFAULT 0,
                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (
                    job_id
                )
                    REFERENCES
                    generation_jobs(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (
                    prompt_id
                )
                    REFERENCES
                    generated_prompts(id)
                    ON DELETE SET NULL
            )
            """
        )

        # IMPORTANT:
        # Existing Step 13 databases do not have the Step 14 owner_id
        # columns yet. Run additive migrations BEFORE creating indexes
        # that depend on those new columns.
        run_migrations(
            connection
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_profile_versions_profile
            ON profile_versions(
                profile_id
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generation_profiles_owner
            ON generation_profiles(
                owner_id
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generation_jobs_owner
            ON generation_jobs(
                owner_id
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generation_jobs_profile
            ON generation_jobs(
                profile_id
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generation_jobs_version
            ON generation_jobs(
                profile_version_id
            )
            """
        )

        # Cloud-read indexes. These columns are queried constantly by History,
        # job recovery and image-batch polling. They were small enough to scan
        # locally, but indexed lookups matter once Turso is the source of truth.
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_reference_images_job_position
            ON reference_images(
                job_id,
                position
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generated_prompts_job_position
            ON generated_prompts(
                job_id,
                position
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generated_images_job_status_prompt
            ON generated_images(
                job_id,
                status,
                prompt_id,
                id
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generated_images_prompt_status_id
            ON generated_images(
                prompt_id,
                status,
                id
            )
            """
        )

        connection.commit()

        print(
            f"Database ready: "
            f"{DATABASE_PATH}"
        )

    finally:
        connection.close()


def get_database_status():
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE
                type = 'table'
                AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        tables = [
            row["name"]
            for row in rows
        ]

        backend = (
            get_database_backend(
                DATABASE_PATH
            )
        )

        return {
            "status":
                "connected",
            "backend":
                backend.name,
            "database":
                DATABASE_PATH.name,
            "tables":
                tables,
            "table_count":
                len(
                    tables
                ),
        }

    finally:
        connection.close()

import sqlite3
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "image_agent.db"


# ============================================================
# CONNECTION
# ============================================================

def get_connection():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ============================================================
# HELPERS
# ============================================================

def column_exists(
    connection,
    table_name: str,
    column_name: str
):

    rows = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    return any(
        row["name"] == column_name
        for row in rows
    )


# ============================================================
# MIGRATIONS
# ============================================================

def run_migrations(
    connection
):

    # Existing installations from Step 4C do not
    # yet contain active_version_id.
    if not column_exists(
        connection,
        "generation_profiles",
        "active_version_id"
    ):

        connection.execute(
            """
            ALTER TABLE generation_profiles
            ADD COLUMN active_version_id INTEGER
            """
        )

    # Every old profile should initially use its
    # latest version for generation.
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

    connection.commit()


# ============================================================
# INITIALIZATION
# ============================================================

def init_database():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------------------------
        # GENERATION PROFILES
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generation_profiles (

                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,

                name TEXT
                    NOT NULL,

                slug TEXT
                    NOT NULL
                    UNIQUE,

                description TEXT,

                is_active INTEGER
                    NOT NULL
                    DEFAULT 1,

                active_version_id INTEGER,

                created_at TEXT
                    NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT
                    NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


        # ----------------------------------------------------
        # PROFILE VERSIONS
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS profile_versions (

                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,

                profile_id INTEGER
                    NOT NULL,

                version_number INTEGER
                    NOT NULL,

                system_instruction TEXT
                    NOT NULL,

                created_at TEXT
                    NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (profile_id)
                    REFERENCES generation_profiles(id)
                    ON DELETE CASCADE,

                UNIQUE(
                    profile_id,
                    version_number
                )
            )
            """
        )


        # ----------------------------------------------------
        # GENERATION JOBS
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generation_jobs (

                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,

                profile_id INTEGER
                    NOT NULL,

                profile_version_id INTEGER
                    NOT NULL,

                description TEXT,

                requested_count TEXT
                    NOT NULL
                    DEFAULT 'auto',

                status TEXT
                    NOT NULL
                    DEFAULT 'pending',

                system_instruction_snapshot TEXT
                    NOT NULL,

                created_at TEXT
                    NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT
                    NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (profile_id)
                    REFERENCES generation_profiles(id),

                FOREIGN KEY (profile_version_id)
                    REFERENCES profile_versions(id)
            )
            """
        )


        # ----------------------------------------------------
        # REFERENCE IMAGES
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reference_images (

                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,

                job_id INTEGER
                    NOT NULL,

                position INTEGER
                    NOT NULL,

                original_filename TEXT
                    NOT NULL,

                stored_filename TEXT
                    NOT NULL,

                file_path TEXT
                    NOT NULL,

                created_at TEXT
                    NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (job_id)
                    REFERENCES generation_jobs(id)
                    ON DELETE CASCADE
            )
            """
        )


        # ----------------------------------------------------
        # GENERATED PROMPTS
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generated_prompts (

                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,

                job_id INTEGER
                    NOT NULL,

                position INTEGER
                    NOT NULL,

                title TEXT,

                prompt_text TEXT
                    NOT NULL,

                metadata_json TEXT,

                status TEXT
                    NOT NULL
                    DEFAULT 'pending',

                created_at TEXT
                    NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (job_id)
                    REFERENCES generation_jobs(id)
                    ON DELETE CASCADE
            )
            """
        )


        # ----------------------------------------------------
        # GENERATED IMAGES
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS generated_images (

                id INTEGER
                    PRIMARY KEY AUTOINCREMENT,

                job_id INTEGER
                    NOT NULL,

                prompt_id INTEGER,

                provider TEXT,

                file_path TEXT,

                status TEXT
                    NOT NULL
                    DEFAULT 'pending',

                error_message TEXT,

                created_at TEXT
                    NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (job_id)
                    REFERENCES generation_jobs(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (prompt_id)
                    REFERENCES generated_prompts(id)
                    ON DELETE SET NULL
            )
            """
        )


        # ----------------------------------------------------
        # INDEXES
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_profile_versions_profile

            ON profile_versions(profile_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generation_jobs_profile

            ON generation_jobs(profile_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generation_jobs_version

            ON generation_jobs(profile_version_id)
            """
        )


        connection.commit()

        run_migrations(
            connection
        )

        print(
            f"Database ready: {DATABASE_PATH}"
        )


    finally:

        connection.close()


# ============================================================
# STATUS
# ============================================================

def get_database_status():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name

            FROM sqlite_master

            WHERE
                type = 'table'
                AND name NOT LIKE 'sqlite_%'

            ORDER BY name
            """
        )

        rows = cursor.fetchall()

        tables = [
            row["name"]
            for row in rows
        ]

        return {
            "status": "connected",
            "database": DATABASE_PATH.name,
            "tables": tables,
            "table_count": len(tables)
        }


    finally:

        connection.close()
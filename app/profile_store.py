from pathlib import Path
import re

from app.database import get_connection


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
PROFILES_DIR = BASE_DIR / "profiles"


# --------------------------------------------------
# DEFAULT PROFILES
# --------------------------------------------------

DEFAULT_PROFILES = [
    {
        "name": "Hero Images",
        "slug": "hero-images",
        "description": "Clean eCommerce hero image prompt generation.",
        "filename": "hero_images.txt",
    },
    {
        "name": "UGC Images",
        "slug": "ugc-images",
        "description": "Authentic grooming salon and tabletop UGC prompt generation.",
        "filename": "ugc_images.txt",
    },
]


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def make_slug(value: str) -> str:
    value = value.strip().lower()

    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value
    )

    return value.strip("-")


def make_unique_slug(connection, name: str) -> str:
    base_slug = make_slug(name)

    if not base_slug:
        base_slug = "profile"

    slug = base_slug
    counter = 2

    while True:
        existing = connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE slug = ?
            """,
            (slug,)
        ).fetchone()

        if existing is None:
            return slug

        slug = f"{base_slug}-{counter}"
        counter += 1


# --------------------------------------------------
# SEED DEFAULT PROFILES
# --------------------------------------------------

def seed_default_profiles():
    connection = get_connection()

    try:
        for profile in DEFAULT_PROFILES:

            file_path = (
                PROFILES_DIR /
                profile["filename"]
            )

            if not file_path.exists():
                print(
                    f"Profile seed skipped. "
                    f"Missing file: {file_path}"
                )
                continue

            existing = connection.execute(
                """
                SELECT id
                FROM generation_profiles
                WHERE slug = ?
                """,
                (profile["slug"],)
            ).fetchone()

            # Do not overwrite an existing profile.
            if existing:
                continue

            instruction = file_path.read_text(
                encoding="utf-8-sig"
            ).strip()

            if not instruction:
                print(
                    f"Profile seed skipped. "
                    f"File is empty: {file_path}"
                )
                continue

            cursor = connection.execute(
                """
                INSERT INTO generation_profiles (
                    name,
                    slug,
                    description
                )
                VALUES (?, ?, ?)
                """,
                (
                    profile["name"],
                    profile["slug"],
                    profile["description"]
                )
            )

            profile_id = cursor.lastrowid

            connection.execute(
                """
                INSERT INTO profile_versions (
                    profile_id,
                    version_number,
                    system_instruction
                )
                VALUES (?, ?, ?)
                """,
                (
                    profile_id,
                    1,
                    instruction
                )
            )

            print(
                f"Seeded profile: "
                f"{profile['name']} v1"
            )

        connection.commit()

    finally:
        connection.close()


# --------------------------------------------------
# LIST PROFILES
# --------------------------------------------------

def list_profiles():
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                gp.id,
                gp.name,
                gp.slug,
                gp.description,
                gp.is_active,
                gp.created_at,
                gp.updated_at,

                pv.id AS version_id,
                pv.version_number

            FROM generation_profiles gp

            JOIN profile_versions pv
                ON pv.id = (
                    SELECT id
                    FROM profile_versions
                    WHERE profile_id = gp.id
                    ORDER BY version_number DESC
                    LIMIT 1
                )

            WHERE gp.is_active = 1

            ORDER BY gp.name ASC
            """
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()


# --------------------------------------------------
# GET ONE PROFILE
# --------------------------------------------------

def get_profile(profile_id: int):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                gp.id,
                gp.name,
                gp.slug,
                gp.description,
                gp.is_active,
                gp.created_at,
                gp.updated_at,

                pv.id AS version_id,
                pv.version_number,
                pv.system_instruction

            FROM generation_profiles gp

            JOIN profile_versions pv
                ON pv.id = (
                    SELECT id
                    FROM profile_versions
                    WHERE profile_id = gp.id
                    ORDER BY version_number DESC
                    LIMIT 1
                )

            WHERE gp.id = ?
            """,
            (profile_id,)
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


# --------------------------------------------------
# CREATE PROFILE
# --------------------------------------------------

def create_profile(
    name: str,
    description: str,
    system_instruction: str
):
    connection = get_connection()

    try:
        slug = make_unique_slug(
            connection,
            name
        )

        cursor = connection.execute(
            """
            INSERT INTO generation_profiles (
                name,
                slug,
                description
            )
            VALUES (?, ?, ?)
            """,
            (
                name.strip(),
                slug,
                description.strip()
            )
        )

        profile_id = cursor.lastrowid

        connection.execute(
            """
            INSERT INTO profile_versions (
                profile_id,
                version_number,
                system_instruction
            )
            VALUES (?, ?, ?)
            """,
            (
                profile_id,
                1,
                system_instruction.strip()
            )
        )

        connection.commit()

    finally:
        connection.close()

    return get_profile(profile_id)


# --------------------------------------------------
# CREATE NEW PROFILE VERSION
# --------------------------------------------------

def create_profile_version(
    profile_id: int,
    system_instruction: str
):
    connection = get_connection()

    try:
        profile = connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE id = ?
            """,
            (profile_id,)
        ).fetchone()

        if profile is None:
            return None

        version_row = connection.execute(
            """
            SELECT
                COALESCE(
                    MAX(version_number),
                    0
                ) AS latest_version

            FROM profile_versions

            WHERE profile_id = ?
            """,
            (profile_id,)
        ).fetchone()

        next_version = (
            version_row["latest_version"] + 1
        )

        connection.execute(
            """
            INSERT INTO profile_versions (
                profile_id,
                version_number,
                system_instruction
            )
            VALUES (?, ?, ?)
            """,
            (
                profile_id,
                next_version,
                system_instruction.strip()
            )
        )

        connection.execute(
            """
            UPDATE generation_profiles

            SET updated_at = CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (profile_id,)
        )

        connection.commit()

    finally:
        connection.close()

    return get_profile(profile_id)
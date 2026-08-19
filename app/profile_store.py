from pathlib import Path
import re

from app.database import get_connection


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
PROFILES_DIR = BASE_DIR / "profiles"


# ============================================================
# DEFAULT PROFILES
# ============================================================

DEFAULT_PROFILES = [
    {
        "name": "Hero Images",
        "slug": "hero-images",
        "description": (
            "Clean eCommerce hero image prompt generation."
        ),
        "filename": "hero_images.txt",
    },
    {
        "name": "UGC Images",
        "slug": "ugc-images",
        "description": (
            "Authentic grooming salon and tabletop "
            "UGC prompt generation."
        ),
        "filename": "ugc_images.txt",
    },
]


# ============================================================
# HELPERS
# ============================================================

def make_slug(
    value: str
):

    value = value.strip().lower()

    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value
    )

    return value.strip("-")


def make_unique_slug(
    connection,
    name: str
):

    base_slug = make_slug(
        name
    )

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

        slug = (
            f"{base_slug}-{counter}"
        )

        counter += 1


# ============================================================
# SEED DEFAULT PROFILES
# ============================================================

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
                    "Profile seed skipped: "
                    f"{file_path}"
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


            if existing:
                continue


            instruction = file_path.read_text(
                encoding="utf-8-sig"
            ).strip()


            if not instruction:
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


            profile_id = (
                cursor.lastrowid
            )


            version_cursor = connection.execute(
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


            version_id = (
                version_cursor.lastrowid
            )


            connection.execute(
                """
                UPDATE generation_profiles

                SET active_version_id = ?

                WHERE id = ?
                """,
                (
                    version_id,
                    profile_id
                )
            )


            print(
                f"Seeded profile: "
                f"{profile['name']} v1"
            )


        connection.commit()


    finally:

        connection.close()


# ============================================================
# LIST PROFILES
# ============================================================

def list_profiles(
    include_inactive: bool = False
):

    connection = get_connection()

    try:

        where_clause = (
            ""
            if include_inactive
            else
            "WHERE gp.is_active = 1"
        )


        rows = connection.execute(
            f"""
            SELECT

                gp.id,
                gp.name,
                gp.slug,
                gp.description,
                gp.is_active,
                gp.active_version_id,
                gp.created_at,
                gp.updated_at,

                active_v.version_number
                    AS active_version_number,

                latest_v.id
                    AS latest_version_id,

                latest_v.version_number
                    AS latest_version_number,

                (
                    SELECT COUNT(*)

                    FROM profile_versions count_v

                    WHERE
                        count_v.profile_id = gp.id
                )
                    AS version_count

            FROM generation_profiles gp

            LEFT JOIN profile_versions active_v
                ON active_v.id =
                    gp.active_version_id

            LEFT JOIN profile_versions latest_v
                ON latest_v.id = (

                    SELECT id

                    FROM profile_versions

                    WHERE profile_id = gp.id

                    ORDER BY
                        version_number DESC

                    LIMIT 1
                )

            {where_clause}

            ORDER BY
                gp.is_active DESC,
                gp.name COLLATE NOCASE ASC,
                gp.id ASC
            """
        ).fetchall()


        profiles = []

        for row in rows:

            item = dict(row)

            # Compatibility with the frontend:
            # version_id/version_number always mean
            # "currently used for Generate".
            item["version_id"] = (
                item["active_version_id"]
            )

            item["version_number"] = (
                item["active_version_number"]
            )

            profiles.append(
                item
            )


        return profiles


    finally:

        connection.close()


# ============================================================
# GET PROFILE — ACTIVE GENERATION VERSION
# ============================================================

def get_profile(
    profile_id: int
):

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
                gp.active_version_id,
                gp.created_at,
                gp.updated_at,

                active_v.id
                    AS version_id,

                active_v.version_number
                    AS version_number,

                active_v.system_instruction
                    AS system_instruction,

                active_v.version_number
                    AS active_version_number,

                latest_v.id
                    AS latest_version_id,

                latest_v.version_number
                    AS latest_version_number,

                (
                    SELECT COUNT(*)

                    FROM profile_versions count_v

                    WHERE
                        count_v.profile_id = gp.id
                )
                    AS version_count

            FROM generation_profiles gp

            LEFT JOIN profile_versions active_v
                ON active_v.id =
                    gp.active_version_id

            LEFT JOIN profile_versions latest_v
                ON latest_v.id = (

                    SELECT id

                    FROM profile_versions

                    WHERE profile_id = gp.id

                    ORDER BY
                        version_number DESC

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


# ============================================================
# SPECIFIC VERSION
# ============================================================

def get_profile_version(
    profile_id: int,
    version_number: int
):

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
                gp.active_version_id,
                gp.created_at,
                gp.updated_at,

                pv.id
                    AS version_id,

                pv.version_number,

                pv.system_instruction,

                pv.created_at
                    AS version_created_at,

                active_v.version_number
                    AS active_version_number,

                latest_v.id
                    AS latest_version_id,

                latest_v.version_number
                    AS latest_version_number,

                CASE
                    WHEN pv.id =
                        gp.active_version_id
                    THEN 1
                    ELSE 0
                END
                    AS is_generation_version

            FROM generation_profiles gp

            JOIN profile_versions pv
                ON pv.profile_id = gp.id

            LEFT JOIN profile_versions active_v
                ON active_v.id =
                    gp.active_version_id

            LEFT JOIN profile_versions latest_v
                ON latest_v.id = (

                    SELECT id

                    FROM profile_versions

                    WHERE profile_id = gp.id

                    ORDER BY
                        version_number DESC

                    LIMIT 1
                )

            WHERE
                gp.id = ?
                AND pv.version_number = ?
            """,
            (
                profile_id,
                version_number
            )
        ).fetchone()


        if row is None:
            return None


        return dict(row)


    finally:

        connection.close()


# ============================================================
# VERSION HISTORY
# ============================================================

def list_profile_versions(
    profile_id: int
):

    connection = get_connection()

    try:

        rows = connection.execute(
            """
            SELECT

                pv.id AS version_id,

                pv.version_number,

                pv.created_at,

                LENGTH(
                    pv.system_instruction
                )
                    AS character_count,

                CASE
                    WHEN pv.id =
                        gp.active_version_id
                    THEN 1
                    ELSE 0
                END
                    AS is_generation_version,

                (
                    SELECT COUNT(*)

                    FROM generation_jobs gj

                    WHERE
                        gj.profile_version_id =
                        pv.id
                )
                    AS usage_count

            FROM profile_versions pv

            JOIN generation_profiles gp
                ON gp.id =
                    pv.profile_id

            WHERE pv.profile_id = ?

            ORDER BY
                pv.version_number DESC
            """,
            (profile_id,)
        ).fetchall()


        return [
            dict(row)
            for row in rows
        ]


    finally:

        connection.close()


# ============================================================
# CREATE PROFILE
# ============================================================

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


        profile_id = (
            cursor.lastrowid
        )


        version_cursor = connection.execute(
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


        version_id = (
            version_cursor.lastrowid
        )


        connection.execute(
            """
            UPDATE generation_profiles

            SET active_version_id = ?

            WHERE id = ?
            """,
            (
                version_id,
                profile_id
            )
        )


        connection.commit()


    finally:

        connection.close()


    return get_profile(
        profile_id
    )


# ============================================================
# UPDATE PROFILE METADATA
# ============================================================

def update_profile_metadata(
    profile_id: int,
    name: str,
    description: str
):

    connection = get_connection()

    try:

        existing = connection.execute(
            """
            SELECT id

            FROM generation_profiles

            WHERE
                id = ?
                AND is_active = 1
            """,
            (profile_id,)
        ).fetchone()


        if existing is None:
            return None


        connection.execute(
            """
            UPDATE generation_profiles

            SET
                name = ?,
                description = ?,
                updated_at =
                    CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                name.strip(),
                description.strip(),
                profile_id
            )
        )


        connection.commit()


    finally:

        connection.close()


    return get_profile(
        profile_id
    )


# ============================================================
# CREATE NEW VERSION
# ============================================================

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

            WHERE
                id = ?
                AND is_active = 1
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
            version_row["latest_version"]
            +
            1
        )


        version_cursor = connection.execute(
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


        new_version_id = (
            version_cursor.lastrowid
        )


        # New versions become the generation version
        # automatically. You can later switch back.
        connection.execute(
            """
            UPDATE generation_profiles

            SET
                active_version_id = ?,
                updated_at =
                    CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                new_version_id,
                profile_id
            )
        )


        connection.commit()


    finally:

        connection.close()


    return get_profile(
        profile_id
    )


# ============================================================
# USE VERSION FOR GENERATE
# ============================================================

def activate_profile_version(
    profile_id: int,
    version_number: int
):

    connection = get_connection()

    try:

        profile = connection.execute(
            """
            SELECT id

            FROM generation_profiles

            WHERE
                id = ?
                AND is_active = 1
            """,
            (profile_id,)
        ).fetchone()


        if profile is None:

            return {
                "status": "not_found"
            }


        version = connection.execute(
            """
            SELECT id

            FROM profile_versions

            WHERE
                profile_id = ?
                AND version_number = ?
            """,
            (
                profile_id,
                version_number
            )
        ).fetchone()


        if version is None:

            return {
                "status": "version_not_found"
            }


        connection.execute(
            """
            UPDATE generation_profiles

            SET
                active_version_id = ?,
                updated_at =
                    CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                version["id"],
                profile_id
            )
        )


        connection.commit()


        return {
            "status": "activated",
            "profile": get_profile(
                profile_id
            )
        }


    finally:

        connection.close()


# ============================================================
# DELETE VERSION
# ============================================================

def delete_profile_version(
    profile_id: int,
    version_number: int
):

    connection = get_connection()

    try:

        profile = connection.execute(
            """
            SELECT
                id,
                active_version_id

            FROM generation_profiles

            WHERE id = ?
            """,
            (profile_id,)
        ).fetchone()


        if profile is None:

            return {
                "status": "profile_not_found"
            }


        version = connection.execute(
            """
            SELECT
                id,
                version_number

            FROM profile_versions

            WHERE
                profile_id = ?
                AND version_number = ?
            """,
            (
                profile_id,
                version_number
            )
        ).fetchone()


        if version is None:

            return {
                "status": "version_not_found"
            }


        count_row = connection.execute(
            """
            SELECT COUNT(*) AS total

            FROM profile_versions

            WHERE profile_id = ?
            """,
            (profile_id,)
        ).fetchone()


        if count_row["total"] <= 1:

            return {
                "status": "last_version"
            }


        if (
            version["id"]
            ==
            profile["active_version_id"]
        ):

            return {
                "status": "active_version"
            }


        usage_row = connection.execute(
            """
            SELECT COUNT(*) AS total

            FROM generation_jobs

            WHERE profile_version_id = ?
            """,
            (version["id"],)
        ).fetchone()


        if usage_row["total"] > 0:

            return {
                "status": "used_by_jobs",
                "usage_count":
                    usage_row["total"]
            }


        connection.execute(
            """
            DELETE FROM profile_versions

            WHERE id = ?
            """,
            (version["id"],)
        )


        connection.execute(
            """
            UPDATE generation_profiles

            SET updated_at =
                CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (profile_id,)
        )


        connection.commit()


        return {
            "status": "deleted"
        }


    finally:

        connection.close()


# ============================================================
# ARCHIVE / RESTORE
# ============================================================

def set_profile_active(
    profile_id: int,
    is_active: bool
):

    connection = get_connection()

    try:

        existing = connection.execute(
            """
            SELECT
                id,
                active_version_id

            FROM generation_profiles

            WHERE id = ?
            """,
            (profile_id,)
        ).fetchone()


        if existing is None:
            return None


        # If somehow an archived profile has no active
        # version, restore its latest version.
        active_version_id = (
            existing["active_version_id"]
        )


        if (
            is_active
            and
            active_version_id is None
        ):

            latest = connection.execute(
                """
                SELECT id

                FROM profile_versions

                WHERE profile_id = ?

                ORDER BY
                    version_number DESC

                LIMIT 1
                """,
                (profile_id,)
            ).fetchone()


            if latest:

                active_version_id = (
                    latest["id"]
                )


        connection.execute(
            """
            UPDATE generation_profiles

            SET
                is_active = ?,
                active_version_id = ?,
                updated_at =
                    CURRENT_TIMESTAMP

            WHERE id = ?
            """,
            (
                1 if is_active else 0,
                active_version_id,
                profile_id
            )
        )


        connection.commit()


    finally:

        connection.close()


    return get_profile(
        profile_id
    )


# ============================================================
# PERMANENT PROFILE DELETE
# ============================================================

def permanently_delete_profile(
    profile_id: int
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

            return {
                "status": "not_found"
            }


        jobs = connection.execute(
            """
            SELECT COUNT(*) AS total

            FROM generation_jobs

            WHERE profile_id = ?
            """,
            (profile_id,)
        ).fetchone()


        # Once generations exist we preserve their
        # historical profile/version relationship.
        if jobs["total"] > 0:

            return {
                "status": "used_by_jobs",
                "usage_count": jobs["total"]
            }


        connection.execute(
            """
            DELETE FROM generation_profiles

            WHERE id = ?
            """,
            (profile_id,)
        )


        connection.commit()


        return {
            "status": "deleted"
        }


    finally:

        connection.close()
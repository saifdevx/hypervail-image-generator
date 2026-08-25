import re

from app.database import get_connection
from app.request_context import (
    get_current_owner_id,
)


BUILTIN_PROFILE_NAMES = {
    "Hero Images",
    "UGC Images",
}


def _slugify(
    value: str,
):
    slug = (
        value.strip()
        .lower()
    )

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        slug,
    ).strip(
        "-"
    )

    return (
        slug
        or
        "profile"
    )


def _unique_slug(
    connection,
    name: str,
    exclude_profile_id: int | None = None,
):
    base = _slugify(
        name
    )

    candidate = base
    counter = 2

    while True:
        if exclude_profile_id is None:
            row = connection.execute(
                """
                SELECT id
                FROM generation_profiles
                WHERE slug = ?
                """,
                (
                    candidate,
                ),
            ).fetchone()
        else:
            row = connection.execute(
                """
                SELECT id
                FROM generation_profiles
                WHERE
                    slug = ?
                    AND id != ?
                """,
                (
                    candidate,
                    exclude_profile_id,
                ),
            ).fetchone()

        if row is None:
            return candidate

        candidate = (
            f"{base}-{counter}"
        )

        counter += 1


def _profile_access_clause():
    return """
        (
            gp.owner_id = ?
            OR (
                gp.owner_id IS NULL
                AND gp.name IN (
                    'Hero Images',
                    'UGC Images'
                )
            )
        )
    """


def _profile_select():
    return """
        SELECT
            gp.id,
            gp.owner_id,
            gp.name,
            gp.slug,
            gp.description,
            gp.is_active,
            gp.active_version_id,
            gp.created_at,
            gp.updated_at,

            active.version_number
                AS active_version_number,
            active.system_instruction
                AS system_instruction,

            (
                SELECT
                    MAX(
                        pv2.version_number
                    )
                FROM profile_versions pv2
                WHERE
                    pv2.profile_id = gp.id
            )
                AS latest_version_number,

            active.id
                AS version_id

        FROM generation_profiles gp

        LEFT JOIN profile_versions active
            ON active.id =
                gp.active_version_id
    """


def seed_default_profiles():
    """
    Step 14 no longer seeds public Hero/UGC instructions from the normal
    profiles folder. Built-in workflow records are managed by
    builtin_workflows.sync_builtin_workflows(), and their real instruction
    text lives only under profiles/private/.
    """
    return {
        "seeded":
            False,
        "reason":
            "builtins_managed_privately",
    }


def list_profiles(
    include_inactive: bool = False,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        clauses = [
            _profile_access_clause()
        ]

        params = [
            owner_id
        ]

        if not include_inactive:
            clauses.append(
                "gp.is_active = 1"
            )

        rows = connection.execute(
            _profile_select()
            +
            """
            WHERE
            """
            +
            " AND ".join(
                f"({clause})"
                for clause
                in clauses
            )
            +
            """
            ORDER BY
                CASE
                    WHEN gp.name =
                        'Hero Images'
                        THEN 0
                    WHEN gp.name =
                        'UGC Images'
                        THEN 1
                    ELSE 2
                END,
                gp.name ASC
            """,
            tuple(
                params
            ),
        ).fetchall()

        return [
            dict(
                row
            )
            for row in rows
        ]

    finally:
        connection.close()


def get_profile(
    profile_id: int,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        row = connection.execute(
            _profile_select()
            +
            f"""
            WHERE
                gp.id = ?
                AND
                {_profile_access_clause()}
            """,
            (
                profile_id,
                owner_id,
            ),
        ).fetchone()

        return (
            dict(
                row
            )
            if row
            else
            None
        )

    finally:
        connection.close()


def get_profile_version(
    profile_id: int,
    version_number: int,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                gp.id,
                gp.owner_id,
                gp.name,
                gp.slug,
                gp.description,
                gp.is_active,
                gp.active_version_id,

                pv.id
                    AS version_id,
                pv.version_number,
                pv.system_instruction,
                pv.created_at

            FROM generation_profiles gp

            JOIN profile_versions pv
                ON pv.profile_id =
                    gp.id

            WHERE
                gp.id = ?
                AND pv.version_number = ?
                AND
                (
                    gp.owner_id = ?
                    OR (
                        gp.owner_id IS NULL
                        AND gp.name IN (
                            'Hero Images',
                            'UGC Images'
                        )
                    )
                )
            """,
            (
                profile_id,
                version_number,
                owner_id,
            ),
        ).fetchone()

        return (
            dict(
                row
            )
            if row
            else
            None
        )

    finally:
        connection.close()


def list_profile_versions(
    profile_id: int,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        allowed = connection.execute(
            """
            SELECT id
            FROM generation_profiles gp
            WHERE
                gp.id = ?
                AND
                (
                    gp.owner_id = ?
                    OR (
                        gp.owner_id IS NULL
                        AND gp.name IN (
                            'Hero Images',
                            'UGC Images'
                        )
                    )
                )
            """,
            (
                profile_id,
                owner_id,
            ),
        ).fetchone()

        if allowed is None:
            return []

        rows = connection.execute(
            """
            SELECT
                id,
                profile_id,
                version_number,
                system_instruction,
                created_at

            FROM profile_versions

            WHERE profile_id = ?

            ORDER BY
                version_number DESC
            """,
            (
                profile_id,
            ),
        ).fetchall()

        return [
            dict(
                row
            )
            for row in rows
        ]

    finally:
        connection.close()


def create_profile(
    name: str,
    description: str,
    system_instruction: str,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        duplicate = connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE
                owner_id = ?
                AND LOWER(name) =
                    LOWER(?)
            """,
            (
                owner_id,
                name,
            ),
        ).fetchone()

        if duplicate is not None:
            raise ValueError(
                "A profile with this name already exists."
            )

        slug = _unique_slug(
            connection,
            name,
        )

        cursor = connection.execute(
            """
            INSERT INTO generation_profiles (
                owner_id,
                name,
                slug,
                description,
                is_active,
                created_at,
                updated_at
            )
            VALUES (
                ?, ?, ?, ?, 1,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
            """,
            (
                owner_id,
                name,
                slug,
                description,
            ),
        )

        profile_id = (
            cursor.lastrowid
        )

        version_cursor = (
            connection.execute(
                """
                INSERT INTO profile_versions (
                    profile_id,
                    version_number,
                    system_instruction
                )
                VALUES (?, 1, ?)
                """,
                (
                    profile_id,
                    system_instruction,
                ),
            )
        )

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
                version_cursor.lastrowid,
                profile_id,
            ),
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return get_profile(
        profile_id
    )


def update_profile_metadata(
    profile_id: int,
    name: str,
    description: str,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                name
            FROM generation_profiles
            WHERE
                id = ?
                AND owner_id = ?
                AND is_active = 1
            """,
            (
                profile_id,
                owner_id,
            ),
        ).fetchone()

        if row is None:
            return None

        duplicate = connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE
                owner_id = ?
                AND LOWER(name) =
                    LOWER(?)
                AND id != ?
            """,
            (
                owner_id,
                name,
                profile_id,
            ),
        ).fetchone()

        if duplicate is not None:
            raise ValueError(
                "A profile with this name already exists."
            )

        slug = _unique_slug(
            connection,
            name,
            exclude_profile_id=
                profile_id,
        )

        connection.execute(
            """
            UPDATE generation_profiles
            SET
                name = ?,
                slug = ?,
                description = ?,
                updated_at =
                    CURRENT_TIMESTAMP
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                name,
                slug,
                description,
                profile_id,
                owner_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()

    return get_profile(
        profile_id
    )


def create_profile_version(
    profile_id: int,
    system_instruction: str,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE
                id = ?
                AND owner_id = ?
                AND is_active = 1
            """,
            (
                profile_id,
                owner_id,
            ),
        ).fetchone()

        if row is None:
            return None

        next_row = connection.execute(
            """
            SELECT
                COALESCE(
                    MAX(
                        version_number
                    ),
                    0
                ) + 1
                    AS next_version
            FROM profile_versions
            WHERE profile_id = ?
            """,
            (
                profile_id,
            ),
        ).fetchone()

        cursor = connection.execute(
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
                next_row[
                    "next_version"
                ],
                system_instruction,
            ),
        )

        connection.execute(
            """
            UPDATE generation_profiles
            SET
                active_version_id = ?,
                updated_at =
                    CURRENT_TIMESTAMP
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                cursor.lastrowid,
                profile_id,
                owner_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()

    return get_profile(
        profile_id
    )


def activate_profile_version(
    profile_id: int,
    version_number: int,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        profile = connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE
                id = ?
                AND owner_id = ?
                AND is_active = 1
            """,
            (
                profile_id,
                owner_id,
            ),
        ).fetchone()

        if profile is None:
            return {
                "status":
                    "not_found"
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
                version_number,
            ),
        ).fetchone()

        if version is None:
            return {
                "status":
                    "version_not_found"
            }

        connection.execute(
            """
            UPDATE generation_profiles
            SET
                active_version_id = ?,
                updated_at =
                    CURRENT_TIMESTAMP
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                version["id"],
                profile_id,
                owner_id,
            ),
        )

        connection.commit()

        return {
            "status":
                "activated",
            "profile":
                get_profile(
                    profile_id
                ),
        }

    finally:
        connection.close()


def delete_profile_version(
    profile_id: int,
    version_number: int,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        profile = connection.execute(
            """
            SELECT
                id,
                active_version_id
            FROM generation_profiles
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                profile_id,
                owner_id,
            ),
        ).fetchone()

        if profile is None:
            return {
                "status":
                    "profile_not_found"
            }

        versions = connection.execute(
            """
            SELECT
                id,
                version_number
            FROM profile_versions
            WHERE profile_id = ?
            ORDER BY version_number
            """,
            (
                profile_id,
            ),
        ).fetchall()

        if len(
            versions
        ) <= 1:
            return {
                "status":
                    "last_version"
            }

        version = next(
            (
                row
                for row in versions
                if int(
                    row[
                        "version_number"
                    ]
                )
                ==
                int(
                    version_number
                )
            ),
            None,
        )

        if version is None:
            return {
                "status":
                    "version_not_found"
            }

        if (
            int(
                profile[
                    "active_version_id"
                ]
                or
                0
            )
            ==
            int(
                version[
                    "id"
                ]
            )
        ):
            return {
                "status":
                    "active_version"
            }

        used = connection.execute(
            """
            SELECT
                COUNT(*) AS count
            FROM generation_jobs
            WHERE
                profile_version_id = ?
                AND owner_id = ?
            """,
            (
                version[
                    "id"
                ],
                owner_id,
            ),
        ).fetchone()

        if (
            int(
                used[
                    "count"
                ]
            )
            >
            0
        ):
            return {
                "status":
                    "used_by_jobs"
            }

        connection.execute(
            """
            DELETE FROM profile_versions
            WHERE
                id = ?
                AND profile_id = ?
            """,
            (
                version[
                    "id"
                ],
                profile_id,
            ),
        )

        connection.commit()

        return {
            "status":
                "deleted",
            "version_number":
                version_number,
        }

    finally:
        connection.close()


def set_profile_active(
    profile_id: int,
    is_active: bool,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE generation_profiles
            SET
                is_active = ?,
                updated_at =
                    CURRENT_TIMESTAMP
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                1
                if is_active
                else
                0,
                profile_id,
                owner_id,
            ),
        )

        connection.commit()

        if cursor.rowcount < 1:
            return None

    finally:
        connection.close()

    return get_profile(
        profile_id
    )


def permanently_delete_profile(
    profile_id: int,
):
    owner_id = (
        get_current_owner_id()
    )

    connection = get_connection()

    try:
        profile = connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                profile_id,
                owner_id,
            ),
        ).fetchone()

        if profile is None:
            return {
                "status":
                    "not_found"
            }

        jobs = connection.execute(
            """
            SELECT
                COUNT(*) AS count
            FROM generation_jobs
            WHERE
                profile_id = ?
                AND owner_id = ?
            """,
            (
                profile_id,
                owner_id,
            ),
        ).fetchone()

        if (
            int(
                jobs[
                    "count"
                ]
            )
            >
            0
        ):
            return {
                "status":
                    "used_by_jobs"
            }

        connection.execute(
            """
            DELETE FROM generation_profiles
            WHERE
                id = ?
                AND owner_id = ?
            """,
            (
                profile_id,
                owner_id,
            ),
        )

        connection.commit()

        return {
            "status":
                "deleted",
            "profile_id":
                profile_id,
        }

    finally:
        connection.close()

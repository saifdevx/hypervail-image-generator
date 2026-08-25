from pathlib import Path

from app.database import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
PRIVATE_PROFILE_DIR = BASE_DIR / "profiles" / "private"

HERO_PRIVATE_FILE = PRIVATE_PROFILE_DIR / "hero_images.txt"
UGC_PRIVATE_FILE = PRIVATE_PROFILE_DIR / "ugc_images.txt"

PRIVATE_PLACEHOLDER = (
    "PRIVATE_BUILTIN_WORKFLOW. "
    "The real instruction is stored outside the database profile record."
)

BUILTIN_WORKFLOWS = {
    "Hero Images": {
        "slug": "hero_images",
        "description": (
            "Turn any product photo into a professional studio shot. "
            "Upload a single reference image and get multiple polished, "
            "magazine-ready angles, dramatic lighting, clean backgrounds, "
            "catalog-perfect composition. No studio, no photographer, "
            "no editing skills required."
        ),
        "path": HERO_PRIVATE_FILE,
    },
    "UGC Images": {
        "slug": "ugc_images",
        "description": (
            "Turn any product photo into authentic, scroll-stopping content. "
            "Upload a single reference image and get natural, realistic "
            "lifestyle shots — casual settings, believable lighting, "
            "everyday moments — while keeping your product exactly accurate "
            "down to every detail. No creators, no photoshoots, no staging required."
        ),
        "path": UGC_PRIVATE_FILE,
    },
}


def is_builtin_workflow_name(name: str | None):
    return bool(
        name
        and name.strip() in BUILTIN_WORKFLOWS
    )


def get_builtin_spec(name: str | None):
    if not name:
        return None

    return BUILTIN_WORKFLOWS.get(
        name.strip()
    )


def get_builtin_description(name: str | None):
    spec = get_builtin_spec(name)

    if spec is None:
        return None

    return spec["description"]


def get_builtin_file_status():
    return {
        name: {
            "exists": spec["path"].exists(),
            "path": str(
                spec["path"].relative_to(BASE_DIR)
            ),
        }
        for name, spec
        in BUILTIN_WORKFLOWS.items()
    }


def load_builtin_instruction(name: str):
    spec = get_builtin_spec(name)

    if spec is None:
        return None

    path = spec["path"]

    if not path.exists():
        return None

    value = path.read_text(
        encoding="utf-8"
    ).strip()

    return value or None


def get_profile_name(profile_id: int):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT name
            FROM generation_profiles
            WHERE id = ?
            """,
            (profile_id,),
        ).fetchone()

        if row is None:
            return None

        return row["name"]

    finally:
        connection.close()


def is_builtin_profile_id(profile_id: int):
    return is_builtin_workflow_name(
        get_profile_name(profile_id)
    )


def sanitize_profile(profile: dict | None):
    if profile is None:
        return None

    result = dict(profile)
    name = result.get("name")

    if not is_builtin_workflow_name(
        name
    ):
        result["is_builtin"] = False
        result["instruction_visibility"] = "visible"
        result["can_edit_profile"] = True
        result["can_edit_instruction"] = True
        result["can_archive"] = True
        result["can_delete"] = True
        return result

    result["description"] = (
        get_builtin_description(
            name
        )
        or result.get(
            "description",
            "",
        )
    )

    result["is_builtin"] = True
    result["instruction_visibility"] = "private"
    result["can_edit_profile"] = False
    result["can_edit_instruction"] = False
    result["can_archive"] = False
    result["can_delete"] = False
    result["system_instruction"] = None
    result["instruction_notice"] = (
        "This is a built-in private workflow. "
        "You can use it for generation, but its full system instruction "
        "is not exposed by the app."
    )

    return result


def sanitize_profile_version(
    profile_id: int,
    version: dict | None,
):
    if version is None:
        return None

    result = dict(version)

    if not is_builtin_profile_id(
        profile_id
    ):
        return result

    result["system_instruction"] = None
    result["is_builtin"] = True
    result["instruction_visibility"] = "private"

    return result


def sync_builtin_workflows():
    """
    Keep the two public workflow records available while keeping the real
    instructions outside the profile/version database rows.

    The real instruction is loaded from profiles/private/*.txt only when a
    new generation job is prepared.
    """
    connection = get_connection()

    try:
        for name, spec in (
            BUILTIN_WORKFLOWS.items()
        ):
            profile = connection.execute(
                """
                SELECT
                    id,
                    active_version_id
                FROM generation_profiles
                WHERE name = ?
                """,
                (name,),
            ).fetchone()

            if profile is None:
                cursor = connection.execute(
                    """
                    INSERT INTO generation_profiles (
                        owner_id,
                        name,
                        slug,
                        description,
                        is_active
                    )
                    VALUES (
                        NULL,
                        ?, ?, ?, 1
                    )
                    """,
                    (
                        name,
                        spec["slug"],
                        spec["description"],
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
                            PRIVATE_PLACEHOLDER,
                        ),
                    )
                )

                connection.execute(
                    """
                    UPDATE generation_profiles
                    SET active_version_id = ?
                    WHERE id = ?
                    """,
                    (
                        version_cursor.lastrowid,
                        profile_id,
                    ),
                )

                continue

            profile_id = profile["id"]

            connection.execute(
                """
                UPDATE generation_profiles
                SET
                    owner_id = NULL,
                    slug = ?,
                    description = ?,
                    is_active = 1
                WHERE id = ?
                """,
                (
                    spec["slug"],
                    spec["description"],
                    profile_id,
                ),
            )

            # Remove old built-in instruction contents from profile_versions.
            connection.execute(
                """
                UPDATE profile_versions
                SET system_instruction = ?
                WHERE profile_id = ?
                """,
                (
                    PRIVATE_PLACEHOLDER,
                    profile_id,
                ),
            )

            if not profile[
                "active_version_id"
            ]:
                version_row = (
                    connection.execute(
                        """
                        SELECT
                            id
                        FROM profile_versions
                        WHERE profile_id = ?
                        ORDER BY version_number DESC
                        LIMIT 1
                        """,
                        (profile_id,),
                    ).fetchone()
                )

                if version_row is None:
                    cursor = (
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
                                PRIVATE_PLACEHOLDER,
                            ),
                        )
                    )

                    active_version_id = (
                        cursor.lastrowid
                    )
                else:
                    active_version_id = (
                        version_row["id"]
                    )

                connection.execute(
                    """
                    UPDATE generation_profiles
                    SET active_version_id = ?
                    WHERE id = ?
                    """,
                    (
                        active_version_id,
                        profile_id,
                    ),
                )

        connection.commit()

    finally:
        connection.close()

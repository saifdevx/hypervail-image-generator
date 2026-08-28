import os
import re
import threading
from pathlib import Path

from cryptography.fernet import (
    Fernet,
    InvalidToken,
)

from app.database import get_connection
from app.request_context import (
    get_current_owner_id,
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOCAL_KEY_FILE = DATA_DIR / ".credential_key"

PRIVATE_PLACEHOLDER = (
    "PRIVATE_MANAGED_WORKFLOW. "
    "The real instruction is encrypted in managed_workflow_versions."
)

VALID_WORKFLOW_TYPES = {
    "private",
    "template",
}

VALID_WORKFLOW_STATUSES = {
    "draft",
    "published",
    "unpublished",
    "archived",
}

SYSTEM_WORKFLOW_NAMES = {
    "Hero Images",
    "UGC Images",
}

_SCHEMA_READY = False
_SCHEMA_LOCK = threading.RLock()

_MASTER_KEY = None
_MASTER_KEY_LOCK = threading.RLock()


def _load_or_create_master_key():
    global _MASTER_KEY

    if _MASTER_KEY is not None:
        return _MASTER_KEY

    with _MASTER_KEY_LOCK:
        if _MASTER_KEY is not None:
            return _MASTER_KEY

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

            # Validate before accepting it.
            Fernet(
                key
            )

            _MASTER_KEY = key
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

            _MASTER_KEY = key
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

        _MASTER_KEY = key
        return key


def _fernet():
    return Fernet(
        _load_or_create_master_key()
    )


def _encrypt_instruction(
    instruction: str,
):
    return (
        _fernet()
        .encrypt(
            instruction.encode(
                "utf-8"
            )
        )
        .decode(
            "utf-8"
        )
    )


def _decrypt_instruction(
    encrypted: str | None,
):
    if not encrypted:
        return None

    try:
        return (
            _fernet()
            .decrypt(
                encrypted.encode(
                    "utf-8"
                )
            )
            .decode(
                "utf-8"
            )
        )

    except (
        InvalidToken,
        ValueError,
    ):
        return None


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
        "workflow"
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


def _clean_type(
    workflow_type: str,
):
    value = (
        workflow_type
        .strip()
        .lower()
    )

    if value not in VALID_WORKFLOW_TYPES:
        raise ValueError(
            "Workflow type must be Private Workflow or Public Template."
        )

    return value


def _clean_status(
    status: str,
):
    value = (
        status
        .strip()
        .lower()
    )

    if value not in VALID_WORKFLOW_STATUSES:
        raise ValueError(
            "Unsupported workflow status."
        )

    return value


def ensure_managed_workflow_schema(
    force: bool = False,
):
    global _SCHEMA_READY

    if (
        _SCHEMA_READY
        and
        not force
    ):
        return

    with _SCHEMA_LOCK:
        if (
            _SCHEMA_READY
            and
            not force
        ):
            return

        connection = get_connection()

        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS
                managed_workflows (
                    profile_id INTEGER PRIMARY KEY,
                    workflow_type TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'draft',
                    sort_order INTEGER NOT NULL DEFAULT 100,
                    is_system INTEGER NOT NULL DEFAULT 0,
                    created_by TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (
                        profile_id
                    )
                        REFERENCES generation_profiles(id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS
                managed_workflow_versions (
                    profile_version_id INTEGER PRIMARY KEY,
                    encrypted_instruction TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (
                        profile_version_id
                    )
                        REFERENCES profile_versions(id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_managed_workflows_status
                ON managed_workflows(
                    status,
                    sort_order,
                    profile_id
                )
                """
            )

            connection.commit()
            _SCHEMA_READY = True

        finally:
            connection.close()


def _managed_row(
    connection,
    profile_id: int,
):
    return connection.execute(
        """
        SELECT
            mw.profile_id,
            mw.workflow_type,
            mw.status,
            mw.sort_order,
            mw.is_system,
            mw.created_by,
            mw.created_at,
            mw.updated_at
        FROM managed_workflows mw
        WHERE mw.profile_id = ?
        """,
        (
            profile_id,
        ),
    ).fetchone()


def get_managed_workflow_type(
    profile_id: int,
):
    ensure_managed_workflow_schema()

    connection = get_connection()

    try:
        row = _managed_row(
            connection,
            profile_id,
        )

        if row is None:
            return None

        return row[
            "workflow_type"
        ]

    finally:
        connection.close()


def is_managed_profile(
    profile_id: int,
):
    return (
        get_managed_workflow_type(
            profile_id
        )
        is not None
    )


def is_global_workflow_name(
    name: str,
):
    ensure_managed_workflow_schema()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT gp.id
            FROM generation_profiles gp
            JOIN managed_workflows mw
                ON mw.profile_id = gp.id
            WHERE LOWER(gp.name) = LOWER(?)
            LIMIT 1
            """,
            (
                name.strip(),
            ),
        ).fetchone()

        return (
            row is not None
        )

    finally:
        connection.close()


def _private_instruction_for_version(
    connection,
    profile_version_id: int,
):
    row = connection.execute(
        """
        SELECT encrypted_instruction
        FROM managed_workflow_versions
        WHERE profile_version_id = ?
        """,
        (
            profile_version_id,
        ),
    ).fetchone()

    if row is None:
        return None

    return _decrypt_instruction(
        row[
            "encrypted_instruction"
        ]
    )


def get_managed_workflow_instruction(
    profile_id: int,
    profile_version_id: int | None = None,
):
    """
    Internal-only instruction resolver used by generation/admin.

    It must never be exposed through a normal public profile response when
    workflow_type == private.
    """
    ensure_managed_workflow_schema()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                gp.id,
                gp.name,
                gp.active_version_id,
                mw.workflow_type,
                mw.status,
                pv.id AS version_id,
                pv.system_instruction
            FROM generation_profiles gp
            JOIN managed_workflows mw
                ON mw.profile_id = gp.id
            JOIN profile_versions pv
                ON pv.id = COALESCE(
                    ?,
                    gp.active_version_id
                )
            WHERE
                gp.id = ?
                AND pv.profile_id = gp.id
            """,
            (
                profile_version_id,
                profile_id,
            ),
        ).fetchone()

        if row is None:
            return None

        if (
            row[
                "workflow_type"
            ]
            ==
            "template"
        ):
            value = (
                row[
                    "system_instruction"
                ]
                or
                ""
            ).strip()

            return (
                value
                or
                None
            )

        value = _private_instruction_for_version(
            connection,
            row[
                "version_id"
            ],
        )

        if value:
            return value

        # Compatibility fallback for Hero / UGC if their encrypted import has
        # not completed yet.
        if (
            row[
                "name"
            ]
            in
            SYSTEM_WORKFLOW_NAMES
        ):
            from app.builtin_workflows import (
                load_builtin_instruction,
            )

            return load_builtin_instruction(
                row[
                    "name"
                ]
            )

        return None

    finally:
        connection.close()


def seed_builtin_managed_workflows():
    """
    Convert Hero/UGC into managed private workflows without exposing their
    instruction text.

    Their current private TXT instruction is encrypted into the managed
    workflow-version table once. The TXT file remains as a compatibility
    fallback and deployment bootstrap source.
    """
    ensure_managed_workflow_schema()

    from app.builtin_workflows import (
        load_builtin_instruction,
    )

    connection = get_connection()

    try:
        for order, name in enumerate(
            (
                "Hero Images",
                "UGC Images",
            ),
            start=1,
        ):
            profile = connection.execute(
                """
                SELECT
                    id,
                    active_version_id
                FROM generation_profiles
                WHERE name = ?
                """,
                (
                    name,
                ),
            ).fetchone()

            if profile is None:
                continue

            connection.execute(
                """
                INSERT INTO managed_workflows (
                    profile_id,
                    workflow_type,
                    status,
                    sort_order,
                    is_system,
                    created_by,
                    updated_at
                )
                VALUES (
                    ?, 'private', 'published', ?, 1, 'system',
                    CURRENT_TIMESTAMP
                )

                ON CONFLICT(profile_id)
                DO NOTHING
                """,
                (
                    profile[
                        "id"
                    ],
                    order,
                ),
            )

            if not profile[
                "active_version_id"
            ]:
                continue

            existing = connection.execute(
                """
                SELECT profile_version_id
                FROM managed_workflow_versions
                WHERE profile_version_id = ?
                """,
                (
                    profile[
                        "active_version_id"
                    ],
                ),
            ).fetchone()

            if existing is not None:
                continue

            instruction = (
                load_builtin_instruction(
                    name
                )
                or
                ""
            ).strip()

            if not instruction:
                continue

            connection.execute(
                """
                INSERT INTO managed_workflow_versions (
                    profile_version_id,
                    encrypted_instruction
                )
                VALUES (?, ?)

                ON CONFLICT(profile_version_id)
                DO NOTHING
                """,
                (
                    profile[
                        "active_version_id"
                    ],
                    _encrypt_instruction(
                        instruction
                    ),
                ),
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def _current_instruction(
    connection,
    row,
):
    if row is None:
        return None

    if (
        row[
            "workflow_type"
        ]
        ==
        "template"
    ):
        value = (
            row[
                "system_instruction"
            ]
            or
            ""
        ).strip()

        return (
            value
            or
            None
        )

    return _private_instruction_for_version(
        connection,
        row[
            "version_id"
        ],
    )


def _admin_workflow_row(
    connection,
    profile_id: int,
):
    return connection.execute(
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

            mw.workflow_type,
            mw.status,
            mw.sort_order,
            mw.is_system,
            mw.created_by,
            mw.created_at AS managed_created_at,
            mw.updated_at AS managed_updated_at,

            pv.id AS version_id,
            pv.version_number,
            pv.system_instruction,

            (
                SELECT COUNT(*)
                FROM generation_jobs gj
                WHERE gj.profile_id = gp.id
            ) AS usage_count,

            (
                SELECT COUNT(*)
                FROM profile_versions pva
                WHERE pva.profile_id = gp.id
            ) AS version_count

        FROM generation_profiles gp

        JOIN managed_workflows mw
            ON mw.profile_id = gp.id

        JOIN profile_versions pv
            ON pv.id = gp.active_version_id

        WHERE gp.id = ?
        """,
        (
            profile_id,
        ),
    ).fetchone()


def _decorate_admin_workflow(
    connection,
    row,
    include_instruction: bool = False,
):
    if row is None:
        return None

    result = dict(
        row
    )

    result[
        "is_system"
    ] = bool(
        result[
            "is_system"
        ]
    )

    result[
        "is_published"
    ] = (
        result[
            "status"
        ]
        ==
        "published"
    )

    if include_instruction:
        result[
            "system_instruction"
        ] = (
            _current_instruction(
                connection,
                row,
            )
            or
            ""
        )
    else:
        result.pop(
            "system_instruction",
            None,
        )

    return result


def list_admin_workflows():
    ensure_managed_workflow_schema()

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
                gp.active_version_id,
                gp.created_at,
                gp.updated_at,

                mw.workflow_type,
                mw.status,
                mw.sort_order,
                mw.is_system,
                mw.created_by,
                mw.created_at AS managed_created_at,
                mw.updated_at AS managed_updated_at,

                pv.id AS version_id,
                pv.version_number,

                (
                    SELECT COUNT(*)
                    FROM generation_jobs gj
                    WHERE gj.profile_id = gp.id
                ) AS usage_count,

                (
                    SELECT COUNT(*)
                    FROM profile_versions pva
                    WHERE pva.profile_id = gp.id
                ) AS version_count

            FROM generation_profiles gp

            JOIN managed_workflows mw
                ON mw.profile_id = gp.id

            JOIN profile_versions pv
                ON pv.id = gp.active_version_id

            ORDER BY
                CASE mw.status
                    WHEN 'published' THEN 0
                    WHEN 'draft' THEN 1
                    WHEN 'unpublished' THEN 2
                    ELSE 3
                END,
                mw.sort_order ASC,
                gp.name ASC
            """
        ).fetchall()

        return [
            _decorate_admin_workflow(
                connection,
                row,
                include_instruction=False,
            )
            for row in rows
        ]

    finally:
        connection.close()


def get_admin_workflow(
    profile_id: int,
):
    ensure_managed_workflow_schema()

    connection = get_connection()

    try:
        row = _admin_workflow_row(
            connection,
            profile_id,
        )

        return _decorate_admin_workflow(
            connection,
            row,
            include_instruction=True,
        )

    finally:
        connection.close()


def get_workflow_summary():
    ensure_managed_workflow_schema()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(
                    CASE
                        WHEN status = 'published'
                            THEN 1
                        ELSE 0
                    END
                ) AS published,
                SUM(
                    CASE
                        WHEN status = 'draft'
                            THEN 1
                        ELSE 0
                    END
                ) AS drafts,
                SUM(
                    CASE
                        WHEN workflow_type = 'private'
                            THEN 1
                        ELSE 0
                    END
                ) AS private_count,
                SUM(
                    CASE
                        WHEN workflow_type = 'template'
                            THEN 1
                        ELSE 0
                    END
                ) AS template_count
            FROM managed_workflows
            """
        ).fetchone()

        return {
            "total":
                int(
                    row[
                        "total"
                    ]
                    or
                    0
                ),
            "published":
                int(
                    row[
                        "published"
                    ]
                    or
                    0
                ),
            "drafts":
                int(
                    row[
                        "drafts"
                    ]
                    or
                    0
                ),
            "private":
                int(
                    row[
                        "private_count"
                    ]
                    or
                    0
                ),
            "templates":
                int(
                    row[
                        "template_count"
                    ]
                    or
                    0
                ),
        }

    finally:
        connection.close()


def _ensure_unique_global_name(
    connection,
    name: str,
    exclude_profile_id: int | None = None,
):
    if exclude_profile_id is None:
        row = connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE
                owner_id IS NULL
                AND LOWER(name) = LOWER(?)
            LIMIT 1
            """,
            (
                name,
            ),
        ).fetchone()
    else:
        row = connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE
                owner_id IS NULL
                AND LOWER(name) = LOWER(?)
                AND id != ?
            LIMIT 1
            """,
            (
                name,
                exclude_profile_id,
            ),
        ).fetchone()

    if row is not None:
        raise ValueError(
            "A global workflow with this name already exists."
        )


def _insert_workflow_version(
    connection,
    profile_id: int,
    workflow_type: str,
    system_instruction: str,
):
    next_row = connection.execute(
        """
        SELECT
            COALESCE(
                MAX(version_number),
                0
            ) + 1 AS next_version
        FROM profile_versions
        WHERE profile_id = ?
        """,
        (
            profile_id,
        ),
    ).fetchone()

    next_version = int(
        next_row[
            "next_version"
        ]
        or
        1
    )

    stored_instruction = (
        system_instruction
        if workflow_type == "template"
        else
        PRIVATE_PLACEHOLDER
    )

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
            next_version,
            stored_instruction,
        ),
    )

    version_id = (
        cursor.lastrowid
    )

    if (
        workflow_type
        ==
        "private"
    ):
        connection.execute(
            """
            INSERT INTO managed_workflow_versions (
                profile_version_id,
                encrypted_instruction
            )
            VALUES (?, ?)
            """,
            (
                version_id,
                _encrypt_instruction(
                    system_instruction
                ),
            ),
        )

    connection.execute(
        """
        UPDATE generation_profiles
        SET
            active_version_id = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            version_id,
            profile_id,
        ),
    )

    return {
        "version_id":
            version_id,
        "version_number":
            next_version,
    }


def create_managed_workflow(
    name: str,
    description: str,
    system_instruction: str,
    workflow_type: str,
    status: str = "draft",
    sort_order: int = 100,
):
    ensure_managed_workflow_schema()

    name = (
        name
        .strip()
    )

    description = (
        description
        .strip()
    )

    system_instruction = (
        system_instruction
        .strip()
    )

    workflow_type = _clean_type(
        workflow_type
    )

    status = _clean_status(
        status
    )

    if not name:
        raise ValueError(
            "Workflow name cannot be empty."
        )

    if not system_instruction:
        raise ValueError(
            "System instruction cannot be empty."
        )

    connection = get_connection()

    try:
        _ensure_unique_global_name(
            connection,
            name,
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
                NULL,
                ?, ?, ?,
                1,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
            """,
            (
                name,
                slug,
                description,
            ),
        )

        profile_id = (
            cursor.lastrowid
        )

        connection.execute(
            """
            INSERT INTO managed_workflows (
                profile_id,
                workflow_type,
                status,
                sort_order,
                is_system,
                created_by,
                updated_at
            )
            VALUES (
                ?, ?, ?, ?, 0, ?,
                CURRENT_TIMESTAMP
            )
            """,
            (
                profile_id,
                workflow_type,
                status,
                max(
                    0,
                    int(
                        sort_order
                    ),
                ),
                get_current_owner_id(),
            ),
        )

        _insert_workflow_version(
            connection,
            profile_id,
            workflow_type,
            system_instruction,
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return get_admin_workflow(
        profile_id
    )


def update_managed_workflow(
    profile_id: int,
    *,
    name: str,
    description: str,
    workflow_type: str,
    system_instruction: str,
    sort_order: int,
):
    ensure_managed_workflow_schema()

    name = name.strip()
    description = description.strip()
    system_instruction = (
        system_instruction
        .strip()
    )

    workflow_type = _clean_type(
        workflow_type
    )

    if not name:
        raise ValueError(
            "Workflow name cannot be empty."
        )

    if not system_instruction:
        raise ValueError(
            "System instruction cannot be empty."
        )

    connection = get_connection()

    try:
        row = _admin_workflow_row(
            connection,
            profile_id,
        )

        if row is None:
            return None

        _ensure_unique_global_name(
            connection,
            name,
            exclude_profile_id=
                profile_id,
        )

        current_instruction = (
            _current_instruction(
                connection,
                row,
            )
            or
            ""
        )

        old_type = (
            row[
                "workflow_type"
            ]
        )

        if (
            workflow_type
            !=
            old_type
        ):
            raise ValueError(
                "Workflow type cannot be changed after creation. "
                "Create a new workflow if you need the other type."
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
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                name,
                slug,
                description,
                profile_id,
            ),
        )

        connection.execute(
            """
            UPDATE managed_workflows
            SET
                workflow_type = ?,
                sort_order = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE profile_id = ?
            """,
            (
                workflow_type,
                max(
                    0,
                    int(
                        sort_order
                    ),
                ),
                profile_id,
            ),
        )

        if (
            system_instruction
            !=
            current_instruction
        ):
            _insert_workflow_version(
                connection,
                profile_id,
                workflow_type,
                system_instruction,
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return get_admin_workflow(
        profile_id
    )


def set_managed_workflow_status(
    profile_id: int,
    status: str,
):
    ensure_managed_workflow_schema()

    status = _clean_status(
        status
    )

    connection = get_connection()

    try:
        row = _admin_workflow_row(
            connection,
            profile_id,
        )

        if row is None:
            return None

        instruction = (
            _current_instruction(
                connection,
                row,
            )
            or
            ""
        ).strip()

        if (
            status
            ==
            "published"
            and
            not instruction
        ):
            raise ValueError(
                "Add a valid system instruction before publishing."
            )

        connection.execute(
            """
            UPDATE managed_workflows
            SET
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE profile_id = ?
            """,
            (
                status,
                profile_id,
            ),
        )

        connection.execute(
            """
            UPDATE generation_profiles
            SET
                is_active = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                0
                if status
                ==
                "archived"
                else
                1,
                profile_id,
            ),
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return get_admin_workflow(
        profile_id
    )


def duplicate_managed_workflow(
    profile_id: int,
):
    source = get_admin_workflow(
        profile_id
    )

    if source is None:
        return None

    base_name = (
        f"{source['name']} Copy"
    )

    connection = get_connection()

    try:
        candidate = base_name
        counter = 2

        while connection.execute(
            """
            SELECT id
            FROM generation_profiles
            WHERE
                owner_id IS NULL
                AND LOWER(name) = LOWER(?)
            """,
            (
                candidate,
            ),
        ).fetchone():
            candidate = (
                f"{base_name} {counter}"
            )
            counter += 1

    finally:
        connection.close()

    return create_managed_workflow(
        name=candidate,
        description=(
            source.get(
                "description"
            )
            or
            ""
        ),
        system_instruction=(
            source.get(
                "system_instruction"
            )
            or
            ""
        ),
        workflow_type=(
            source[
                "workflow_type"
            ]
        ),
        status="draft",
        sort_order=(
            int(
                source.get(
                    "sort_order"
                )
                or
                100
            )
            +
            1
        ),
    )


def list_managed_workflow_versions(
    profile_id: int,
):
    ensure_managed_workflow_schema()

    connection = get_connection()

    try:
        workflow = _managed_row(
            connection,
            profile_id,
        )

        if workflow is None:
            return []

        profile = connection.execute(
            """
            SELECT active_version_id
            FROM generation_profiles
            WHERE id = ?
            """,
            (
                profile_id,
            ),
        ).fetchone()

        rows = connection.execute(
            """
            SELECT
                pv.id,
                pv.profile_id,
                pv.version_number,
                pv.created_at,
                CASE
                    WHEN pv.id = ?
                        THEN 1
                    ELSE 0
                END AS is_active
            FROM profile_versions pv
            WHERE pv.profile_id = ?
            ORDER BY pv.version_number DESC
            """,
            (
                (
                    profile[
                        "active_version_id"
                    ]
                    if profile
                    else
                    None
                ),
                profile_id,
            ),
        ).fetchall()

        return [
            {
                **dict(
                    row
                ),
                "is_active":
                    bool(
                        row[
                            "is_active"
                        ]
                    ),
            }
            for row in rows
        ]

    finally:
        connection.close()


def rollback_managed_workflow(
    profile_id: int,
    version_number: int,
):
    ensure_managed_workflow_schema()

    connection = get_connection()

    try:
        workflow = _managed_row(
            connection,
            profile_id,
        )

        if workflow is None:
            return {
                "status":
                    "not_found"
            }

        version = connection.execute(
            """
            SELECT
                id,
                version_number,
                system_instruction
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

        if (
            workflow[
                "workflow_type"
            ]
            ==
            "private"
        ):
            encrypted = connection.execute(
                """
                SELECT encrypted_instruction
                FROM managed_workflow_versions
                WHERE profile_version_id = ?
                """,
                (
                    version[
                        "id"
                    ],
                ),
            ).fetchone()

            if (
                encrypted is None
                or
                not _decrypt_instruction(
                    encrypted[
                        "encrypted_instruction"
                    ]
                )
            ):
                return {
                    "status":
                        "instruction_missing"
                }

        connection.execute(
            """
            UPDATE generation_profiles
            SET
                active_version_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                version[
                    "id"
                ],
                profile_id,
            ),
        )

        connection.execute(
            """
            UPDATE managed_workflows
            SET updated_at = CURRENT_TIMESTAMP
            WHERE profile_id = ?
            """,
            (
                profile_id,
            ),
        )

        connection.commit()

        return {
            "status":
                "activated",
            "workflow":
                get_admin_workflow(
                    profile_id
                ),
        }

    finally:
        connection.close()


def delete_managed_workflow(
    profile_id: int,
):
    ensure_managed_workflow_schema()

    connection = get_connection()

    try:
        row = _admin_workflow_row(
            connection,
            profile_id,
        )

        if row is None:
            return {
                "status":
                    "not_found"
            }

        if bool(
            row[
                "is_system"
            ]
        ):
            return {
                "status":
                    "system_protected"
            }

        jobs = int(
            row[
                "usage_count"
            ]
            or
            0
        )

        if jobs:
            return {
                "status":
                    "used_by_jobs"
            }

        connection.execute(
            """
            DELETE FROM generation_profiles
            WHERE id = ?
            """,
            (
                profile_id,
            ),
        )

        connection.commit()

        return {
            "status":
                "deleted",
            "profile_id":
                profile_id,
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def create_user_copy_from_template(
    profile_id: int,
):
    ensure_managed_workflow_schema()

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                gp.id,
                gp.name,
                gp.description,
                gp.active_version_id,
                mw.workflow_type,
                mw.status,
                pv.system_instruction
            FROM generation_profiles gp
            JOIN managed_workflows mw
                ON mw.profile_id = gp.id
            JOIN profile_versions pv
                ON pv.id = gp.active_version_id
            WHERE gp.id = ?
            """,
            (
                profile_id,
            ),
        ).fetchone()

        if (
            row is None
            or
            row[
                "workflow_type"
            ]
            !=
            "template"
            or
            row[
                "status"
            ]
            !=
            "published"
        ):
            return None

        name = (
            f"{row['name']} — My Copy"
        )

        instruction = (
            row[
                "system_instruction"
            ]
            or
            ""
        ).strip()

        description = (
            row[
                "description"
            ]
            or
            ""
        )

    finally:
        connection.close()

    from app.profile_store import (
        create_profile,
    )

    base_name = name
    counter = 2

    while True:
        try:
            return create_profile(
                name=name,
                description=description,
                system_instruction=
                    instruction,
            )

        except ValueError as error:
            if (
                "already exists"
                not in
                str(
                    error
                ).lower()
            ):
                raise

            name = (
                f"{base_name} {counter}"
            )

            counter += 1

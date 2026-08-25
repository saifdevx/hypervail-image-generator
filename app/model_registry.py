import json

from app.database import get_connection


TIERS = (
    "economy",
    "balanced",
    "premium",
)

CAPABILITIES = {
    "planner",
    "image",
}

PROVIDERS = {
    "openai",
    "gemini",
}


DEFAULT_MODELS = [
    {
        "provider": "openai",
        "capability": "planner",
        "tier": "economy",
        "model_id": "gpt-5.6-luna",
        "display_name": "Economy",
        "note": "Lowest credit usage / fastest OpenAI planning option.",
        "config": {
            "reasoning": "low",
        },
        "sort_order": 10,
    },
    {
        "provider": "openai",
        "capability": "planner",
        "tier": "balanced",
        "model_id": "gpt-5.6-terra",
        "display_name": "Balanced",
        "note": "Better reasoning and fidelity with moderate usage.",
        "config": {
            "reasoning": "medium",
        },
        "sort_order": 20,
    },
    {
        "provider": "openai",
        "capability": "planner",
        "tier": "premium",
        "model_id": "gpt-5.6-sol",
        "display_name": "Best Quality",
        "note": "Highest-quality OpenAI planner tier.",
        "config": {
            "reasoning": "high",
        },
        "sort_order": 30,
    },
    {
        "provider": "gemini",
        "capability": "planner",
        "tier": "economy",
        "model_id": "gemini-3.1-flash-lite",
        "display_name": "Economy",
        "note": "Lowest-cost Gemini planner tier.",
        "config": {},
        "sort_order": 10,
    },
    {
        "provider": "gemini",
        "capability": "planner",
        "tier": "balanced",
        "model_id": "gemini-3.5-flash-lite",
        "display_name": "Balanced",
        "note": "Moderate Gemini planner tier.",
        "config": {},
        "sort_order": 20,
    },
    {
        "provider": "gemini",
        "capability": "planner",
        "tier": "premium",
        "model_id": "gemini-3.6-flash",
        "display_name": "Best Quality",
        "note": "Strongest Gemini planner tier currently configured in Hyperex.",
        "config": {},
        "sort_order": 30,
    },
    {
        "provider": "openai",
        "capability": "image",
        "tier": "economy",
        "model_id": "gpt-image-2",
        "display_name": "Economy",
        "note": "GPT Image 2 using low quality.",
        "config": {
            "quality": "low",
        },
        "sort_order": 10,
    },
    {
        "provider": "openai",
        "capability": "image",
        "tier": "balanced",
        "model_id": "gpt-image-2",
        "display_name": "Balanced",
        "note": "GPT Image 2 using medium quality.",
        "config": {
            "quality": "medium",
        },
        "sort_order": 20,
    },
    {
        "provider": "openai",
        "capability": "image",
        "tier": "premium",
        "model_id": "gpt-image-2",
        "display_name": "Best Quality",
        "note": "GPT Image 2 using high quality.",
        "config": {
            "quality": "high",
        },
        "sort_order": 30,
    },
    {
        "provider": "gemini",
        "capability": "image",
        "tier": "economy",
        "model_id": "gemini-3.1-flash-lite-image",
        "display_name": "Economy",
        "note": "Fast / economical Gemini image tier.",
        "config": {
            "size": "1K",
        },
        "sort_order": 10,
    },
    {
        "provider": "gemini",
        "capability": "image",
        "tier": "balanced",
        "model_id": "gemini-3.1-flash-image",
        "display_name": "Balanced",
        "note": "Higher-quality Gemini image generation.",
        "config": {
            "size": "1K",
        },
        "sort_order": 20,
    },
    {
        "provider": "gemini",
        "capability": "image",
        "tier": "premium",
        "model_id": "gemini-3.1-flash-image",
        "display_name": "Best Quality",
        "note": "Higher-resolution Gemini image tier.",
        "config": {
            "size": "2K",
        },
        "sort_order": 30,
    },
]


def ensure_model_registry_schema():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS model_registry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                capability TEXT NOT NULL,
                tier TEXT NOT NULL,
                model_id TEXT NOT NULL,
                display_name TEXT NOT NULL,
                note TEXT,
                config_json TEXT NOT NULL DEFAULT '{}',
                enabled INTEGER NOT NULL DEFAULT 1,
                sort_order INTEGER NOT NULL DEFAULT 100,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (
                    provider,
                    capability,
                    tier
                )
            )
            """
        )

        for item in DEFAULT_MODELS:
            connection.execute(
                """
                INSERT OR IGNORE INTO model_registry (
                    provider,
                    capability,
                    tier,
                    model_id,
                    display_name,
                    note,
                    config_json,
                    enabled,
                    sort_order
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
                """,
                (
                    item["provider"],
                    item["capability"],
                    item["tier"],
                    item["model_id"],
                    item["display_name"],
                    item["note"],
                    json.dumps(
                        item.get(
                            "config",
                            {},
                        )
                    ),
                    item["sort_order"],
                ),
            )

        connection.commit()

    finally:
        connection.close()


def list_models(
    provider: str | None = None,
    capability: str | None = None,
    enabled_only: bool = False,
):
    ensure_model_registry_schema()
    connection = get_connection()

    try:
        clauses = []
        params = []

        if provider:
            clauses.append(
                "provider = ?"
            )
            params.append(
                provider
            )

        if capability:
            clauses.append(
                "capability = ?"
            )
            params.append(
                capability
            )

        if enabled_only:
            clauses.append(
                "enabled = 1"
            )

        where = (
            "WHERE "
            +
            " AND ".join(
                clauses
            )
            if clauses
            else
            ""
        )

        rows = connection.execute(
            f"""
            SELECT *
            FROM model_registry
            {where}
            ORDER BY
                capability ASC,
                provider ASC,
                sort_order ASC,
                id ASC
            """,
            tuple(
                params
            ),
        ).fetchall()

        output = []

        for row in rows:
            item = dict(
                row
            )

            try:
                item["config"] = (
                    json.loads(
                        item.pop(
                            "config_json"
                        )
                        or
                        "{}"
                    )
                )
            except Exception:
                item["config"] = {}

            item["enabled"] = bool(
                item["enabled"]
            )

            output.append(
                item
            )

        return output

    finally:
        connection.close()


def model_options(
    provider: str,
    capability: str,
):
    """
    Return unique API model IDs for the existing Settings model dropdown.

    The Admin registry can contain several product tiers that point at the
    same underlying API model with different quality/reasoning config.
    A dedicated tier selector will be introduced after the registry is
    proven stable, so duplicate HTML option values are intentionally
    collapsed here.
    """
    options = []
    seen_model_ids = set()

    for item in list_models(
        provider=
            provider,
        capability=
            capability,
        enabled_only=True,
    ):
        api_model_id = (
            item[
                "model_id"
            ]
        )

        if (
            api_model_id
            in
            seen_model_ids
        ):
            continue

        seen_model_ids.add(
            api_model_id
        )

        options.append(
            {
                "id":
                    api_model_id,
                "label": (
                    f"{item['display_name']} · "
                    f"{api_model_id}"
                ),
                "note":
                    item.get(
                        "note"
                    )
                    or
                    "",
                "tier":
                    item[
                        "tier"
                    ],
                "config":
                    item.get(
                        "config",
                        {},
                    ),
            }
        )

    return options


def allowed_model_ids(
    provider: str,
    capability: str,
):
    return {
        item[
            "model_id"
        ]
        for item
        in list_models(
            provider=
                provider,
            capability=
                capability,
            enabled_only=True,
        )
    }


def update_model(
    model_id: int,
    values: dict,
):
    ensure_model_registry_schema()

    allowed = {
        "model_id",
        "display_name",
        "note",
        "enabled",
        "sort_order",
        "config",
    }

    updates = []
    params = []

    for key, value in (
        values.items()
    ):
        if key not in allowed:
            continue

        column = (
            "config_json"
            if key == "config"
            else key
        )

        if key == "config":
            value = json.dumps(
                value
                or
                {}
            )

        if key == "enabled":
            value = (
                1
                if bool(
                    value
                )
                else
                0
            )

        updates.append(
            f"{column} = ?"
        )
        params.append(
            value
        )

    if not updates:
        return None

    updates.append(
        "updated_at = CURRENT_TIMESTAMP"
    )

    params.append(
        model_id
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            f"""
            UPDATE model_registry
            SET
                {", ".join(updates)}
            WHERE id = ?
            """,
            tuple(
                params
            ),
        )

        connection.commit()

        if cursor.rowcount < 1:
            return None

    finally:
        connection.close()

    rows = [
        item
        for item
        in list_models()
        if int(
            item["id"]
        )
        ==
        int(
            model_id
        )
    ]

    return (
        rows[0]
        if rows
        else
        None
    )

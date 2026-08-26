import json
import threading

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
        "note": "Lowest usage for everyday product analysis.",
        "config": {"reasoning": "low"},
        "sort_order": 10,
    },
    {
        "provider": "openai",
        "capability": "planner",
        "tier": "balanced",
        "model_id": "gpt-5.6-terra",
        "display_name": "Balanced",
        "note": "Recommended balance of quality and usage.",
        "config": {"reasoning": "medium"},
        "sort_order": 20,
    },
    {
        "provider": "openai",
        "capability": "planner",
        "tier": "premium",
        "model_id": "gpt-5.6-sol",
        "display_name": "Best Quality",
        "note": "Strongest OpenAI planning quality.",
        "config": {"reasoning": "high"},
        "sort_order": 30,
    },
    {
        "provider": "gemini",
        "capability": "planner",
        "tier": "economy",
        "model_id": "gemini-3.5-flash-lite",
        "display_name": "Economy",
        "note": "Fastest, most cost-efficient Gemini planning tier.",
        "config": {},
        "sort_order": 10,
    },
    {
        "provider": "gemini",
        "capability": "planner",
        "tier": "balanced",
        "model_id": "gemini-3.6-flash",
        "display_name": "Balanced",
        "note": "Recommended balance of speed and multimodal quality.",
        "config": {},
        "sort_order": 20,
    },
    {
        "provider": "gemini",
        "capability": "planner",
        "tier": "premium",
        "model_id": "gemini-3.7-flash",
        "display_name": "Best Quality",
        "note": "Strongest Gemini planning tier configured in Hyperex.",
        "config": {},
        "sort_order": 30,
    },
    {
        "provider": "openai",
        "capability": "image",
        "tier": "economy",
        "model_id": "gpt-image-2",
        "display_name": "Economy",
        "note": "GPT Image 2 with the lowest-cost quality preset.",
        "config": {"quality": "low"},
        "sort_order": 10,
    },
    {
        "provider": "openai",
        "capability": "image",
        "tier": "balanced",
        "model_id": "gpt-image-2",
        "display_name": "Balanced",
        "note": "GPT Image 2 with the recommended quality preset.",
        "config": {"quality": "medium"},
        "sort_order": 20,
    },
    {
        "provider": "openai",
        "capability": "image",
        "tier": "premium",
        "model_id": "gpt-image-2",
        "display_name": "Best Quality",
        "note": "GPT Image 2 with the strongest quality preset.",
        "config": {"quality": "high"},
        "sort_order": 30,
    },
    {
        "provider": "gemini",
        "capability": "image",
        "tier": "economy",
        "model_id": "gemini-3.1-flash-lite-image",
        "display_name": "Economy",
        "note": "Nano Banana 2 Lite for low-cost, high-volume images.",
        "config": {"size": "1K"},
        "sort_order": 10,
    },
    {
        "provider": "gemini",
        "capability": "image",
        "tier": "balanced",
        "model_id": "gemini-3.1-flash-image",
        "display_name": "Balanced",
        "note": "Nano Banana 2 for stronger everyday image quality.",
        "config": {"size": "1K"},
        "sort_order": 20,
    },
    {
        "provider": "gemini",
        "capability": "image",
        "tier": "premium",
        "model_id": "gemini-3-pro-image",
        "display_name": "Best Quality",
        "note": "Nano Banana Pro for the strongest native Gemini image quality.",
        "config": {"size": "2K"},
        "sort_order": 30,
    },
]


_SCHEMA_READY = False
_MODEL_CACHE = None
_MODEL_GENERATION = 0
_LOCK = threading.RLock()


def _clone_model(item: dict):
    cloned = dict(item)
    cloned["config"] = dict(item.get("config") or {})
    return cloned


def _default_item(provider: str, capability: str, tier: str):
    for item in DEFAULT_MODELS:
        if (
            item["provider"] == provider
            and item["capability"] == capability
            and item["tier"] == tier
        ):
            return item
    return None


def _apply_registry_revision_2(connection):
    migrations = [
        (
            "gemini",
            "planner",
            "economy",
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash-lite",
        ),
        (
            "gemini",
            "planner",
            "balanced",
            "gemini-3.5-flash-lite",
            "gemini-3.6-flash",
        ),
        (
            "gemini",
            "planner",
            "premium",
            "gemini-3.6-flash",
            "gemini-3.7-flash",
        ),
        (
            "gemini",
            "image",
            "premium",
            "gemini-3.1-flash-image",
            "gemini-3-pro-image",
        ),
    ]

    for provider, capability, tier, old_model, new_model in migrations:
        item = _default_item(provider, capability, tier)
        if item is None:
            continue

        connection.execute(
            """
            UPDATE model_registry
            SET
                model_id = ?,
                display_name = ?,
                note = ?,
                config_json = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                provider = ?
                AND capability = ?
                AND tier = ?
                AND model_id = ?
            """,
            (
                new_model,
                item["display_name"],
                item["note"],
                json.dumps(item.get("config", {})),
                provider,
                capability,
                tier,
                old_model,
            ),
        )


def ensure_model_registry_schema(force: bool = False):
    """Run DDL/migrations once per process, not on every Settings read."""
    global _SCHEMA_READY, _MODEL_CACHE, _MODEL_GENERATION

    if _SCHEMA_READY and not force:
        return

    with _LOCK:
        if _SCHEMA_READY and not force:
            return

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
                    UNIQUE (provider, capability, tier)
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS model_registry_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
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
                        json.dumps(item.get("config", {})),
                        item["sort_order"],
                    ),
                )

            revision_row = connection.execute(
                """
                SELECT value
                FROM model_registry_meta
                WHERE key = 'defaults_revision'
                """
            ).fetchone()

            try:
                revision = int(revision_row["value"] if revision_row else 1)
            except (TypeError, ValueError):
                revision = 1

            if revision < 2:
                _apply_registry_revision_2(connection)
                connection.execute(
                    """
                    INSERT INTO model_registry_meta (key, value)
                    VALUES ('defaults_revision', '2')
                    ON CONFLICT(key)
                    DO UPDATE SET value = excluded.value
                    """
                )

            connection.commit()
            _SCHEMA_READY = True
            _MODEL_CACHE = None
            _MODEL_GENERATION += 1
        finally:
            connection.close()


def invalidate_model_cache():
    global _MODEL_CACHE, _MODEL_GENERATION
    with _LOCK:
        _MODEL_CACHE = None
        _MODEL_GENERATION += 1


def get_model_generation():
    return _MODEL_GENERATION


def _load_all_models(refresh: bool = False):
    global _MODEL_CACHE

    ensure_model_registry_schema()

    with _LOCK:
        if _MODEL_CACHE is not None and not refresh:
            return [_clone_model(item) for item in _MODEL_CACHE]

        connection = get_connection()
        try:
            rows = connection.execute(
                """
                SELECT *
                FROM model_registry
                ORDER BY
                    capability ASC,
                    provider ASC,
                    sort_order ASC,
                    id ASC
                """
            ).fetchall()
        finally:
            connection.close()

        output = []
        for row in rows:
            item = dict(row)
            try:
                item["config"] = json.loads(item.pop("config_json") or "{}")
            except Exception:
                item.pop("config_json", None)
                item["config"] = {}

            item["enabled"] = bool(item.get("enabled"))
            output.append(item)

        _MODEL_CACHE = [_clone_model(item) for item in output]
        return [_clone_model(item) for item in output]


def list_models(
    provider: str | None = None,
    capability: str | None = None,
    enabled_only: bool = False,
):
    rows = _load_all_models()

    return [
        item
        for item in rows
        if (
            (not provider or item["provider"] == provider)
            and (not capability or item["capability"] == capability)
            and (not enabled_only or item["enabled"])
        )
    ]


def get_model_tier(
    provider: str,
    capability: str,
    tier: str,
    enabled_only: bool = True,
):
    for item in list_models(
        provider=provider,
        capability=capability,
        enabled_only=enabled_only,
    ):
        if item["tier"] == tier:
            return item
    return None


def _tier_option(item: dict):
    return {
        "id": item["tier"],
        "label": item["display_name"],
        "model_id": item["model_id"],
        "note": item.get("note") or "",
        "config": dict(item.get("config") or {}),
    }


def tier_options(provider: str, capability: str):
    return [
        _tier_option(item)
        for item in list_models(
            provider=provider,
            capability=capability,
            enabled_only=True,
        )
    ]


def tier_catalog():
    """Build all four user tier lists from one cached registry read."""
    catalog = {
        "planner": {"openai": [], "gemini": []},
        "image": {"openai": [], "gemini": []},
    }

    for item in list_models(enabled_only=True):
        capability = item.get("capability")
        provider = item.get("provider")
        if capability in catalog and provider in catalog[capability]:
            catalog[capability][provider].append(_tier_option(item))

    return catalog


def model_options(provider: str, capability: str):
    """Legacy compatibility list for older Hyperex clients."""
    options = []
    seen_model_ids = set()

    for item in list_models(
        provider=provider,
        capability=capability,
        enabled_only=True,
    ):
        api_model_id = item["model_id"]
        if api_model_id in seen_model_ids:
            continue

        seen_model_ids.add(api_model_id)
        options.append(
            {
                "id": api_model_id,
                "label": f"{item['display_name']} · {api_model_id}",
                "note": item.get("note") or "",
                "tier": item["tier"],
                "config": dict(item.get("config") or {}),
            }
        )

    return options


def allowed_model_ids(provider: str, capability: str):
    return {
        item["model_id"]
        for item in list_models(
            provider=provider,
            capability=capability,
            enabled_only=True,
        )
    }


def update_model(model_id: int, values: dict):
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

    for key, value in values.items():
        if key not in allowed:
            continue

        column = "config_json" if key == "config" else key

        if key == "config":
            value = json.dumps(value or {})
        elif key == "enabled":
            value = 1 if bool(value) else 0

        updates.append(f"{column} = ?")
        params.append(value)

    if not updates:
        return None

    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(model_id)

    connection = get_connection()
    try:
        cursor = connection.execute(
            f"""
            UPDATE model_registry
            SET {", ".join(updates)}
            WHERE id = ?
            """,
            tuple(params),
        )
        connection.commit()

        if cursor.rowcount < 1:
            return None
    finally:
        connection.close()

    invalidate_model_cache()

    for item in list_models():
        if int(item["id"]) == int(model_id):
            return item
    return None

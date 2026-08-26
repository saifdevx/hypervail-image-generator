import os
import threading
import time

from app.database import get_connection
from app.request_context import (
    get_current_owner_id,
    LOCAL_OWNER_ID,
)
from app.model_registry import (
    get_model_tier,
    get_model_generation,
    tier_catalog,
)


DEFAULTS = {
    "planner_provider": os.getenv("PLANNER_PROVIDER", "gemini"),
    "planner_tier": os.getenv("PLANNER_TIER", "economy"),
    "gemini_planner_model": os.getenv(
        "GEMINI_PROMPT_MODEL",
        "gemini-3.5-flash-lite",
    ),
    "openai_planner_model": os.getenv(
        "OPENAI_PROMPT_MODEL",
        "gpt-5.6-luna",
    ),
    "openai_planner_reasoning": os.getenv(
        "OPENAI_PLANNER_REASONING_EFFORT",
        "low",
    ),
    "image_provider": os.getenv("IMAGE_PROVIDER", "openai"),
    "image_tier": os.getenv("IMAGE_TIER", "economy"),
    "openai_image_model": os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2"),
    "openai_image_quality": os.getenv("OPENAI_IMAGE_QUALITY", "low"),
    "openai_image_size": os.getenv("OPENAI_IMAGE_SIZE", "1024x1024"),
    "openai_image_output_format": os.getenv(
        "OPENAI_IMAGE_OUTPUT_FORMAT",
        "jpeg",
    ),
    "gemini_image_model": os.getenv(
        "GEMINI_IMAGE_MODEL",
        "gemini-3.1-flash-lite-image",
    ),
    "gemini_image_size": os.getenv("GEMINI_IMAGE_SIZE", "1K"),
    "gemini_image_aspect_ratio": os.getenv(
        "GEMINI_IMAGE_ASPECT_RATIO",
        "1:1",
    ),
    "batch_concurrency": os.getenv("IMAGE_BATCH_CONCURRENCY", "2"),
    "auto_generate_images": "true",
    "confirm_batch_over": "4",
    "max_output_count": "8",
    "draft_autosave": "true",
}


CATALOG = {
    "planner_providers": [
        {"id": "gemini", "label": "Google Gemini"},
        {"id": "openai", "label": "OpenAI"},
    ],
    "image_providers": [
        {"id": "openai", "label": "OpenAI"},
        {"id": "gemini", "label": "Google Gemini"},
    ],
    "openai_reasoning": ["none", "low", "medium", "high"],
    "openai_image_quality": ["low", "medium", "high"],
    "openai_image_sizes": [
        "1024x1024",
        "1024x1536",
        "1536x1024",
    ],
    "gemini_image_sizes": ["1K", "2K", "4K"],
    "gemini_image_aspect_ratios": [
        "1:1",
        "3:2",
        "2:3",
        "4:3",
        "3:4",
        "16:9",
        "9:16",
    ],
    "batch_concurrency": [1, 2, 3, 4],
    "confirm_batch_over": [1, 4, 6, 8],
    "max_output_count": [4, 6, 8, 12, 16],
}


_SCHEMA_READY = False
_SCHEMA_LOCK = threading.RLock()
_RUNTIME_CACHE = {}
_RUNTIME_CACHE_LOCK = threading.RLock()
_RUNTIME_CACHE_TTL_SECONDS = 3.0


def ensure_settings_schema(force: bool = False):
    """
    Run the structural migration once per process.

    Checkpoint 0.5 previously re-ran this migration for every individual
    setting read. On Windows/SQLite that meant many DDL checks + commits for
    one /api/settings request. Runtime reads now stay read-only and fast.
    """
    global _SCHEMA_READY

    if _SCHEMA_READY and not force:
        return

    with _SCHEMA_LOCK:
        if _SCHEMA_READY and not force:
            return

        connection = get_connection()
        try:
            columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(app_settings)"
                ).fetchall()
            }

            if not columns:
                connection.execute(
                    """
                    CREATE TABLE app_settings (
                        owner_id TEXT NOT NULL,
                        key TEXT NOT NULL,
                        value TEXT NOT NULL,
                        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (owner_id, key)
                    )
                    """
                )

            elif "owner_id" not in columns:
                connection.execute(
                    "ALTER TABLE app_settings RENAME TO app_settings_legacy"
                )
                connection.execute(
                    """
                    CREATE TABLE app_settings (
                        owner_id TEXT NOT NULL,
                        key TEXT NOT NULL,
                        value TEXT NOT NULL,
                        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (owner_id, key)
                    )
                    """
                )
                connection.execute(
                    """
                    INSERT INTO app_settings (
                        owner_id,
                        key,
                        value,
                        updated_at
                    )
                    SELECT ?, key, value, updated_at
                    FROM app_settings_legacy
                    """,
                    (LOCAL_OWNER_ID,),
                )
                connection.execute("DROP TABLE app_settings_legacy")

            image_columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(generated_images)"
                ).fetchall()
            }
            if image_columns and "generation_note" not in image_columns:
                connection.execute(
                    "ALTER TABLE generated_images ADD COLUMN generation_note TEXT"
                )

            job_columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(generation_jobs)"
                ).fetchall()
            }
            if job_columns and "planner_provider" not in job_columns:
                connection.execute(
                    "ALTER TABLE generation_jobs ADD COLUMN planner_provider TEXT"
                )

            connection.commit()
            _SCHEMA_READY = True
        finally:
            connection.close()


def _owner_setting_rows(owner_id: str):
    ensure_settings_schema()
    connection = get_connection()
    try:
        rows = connection.execute(
            """
            SELECT key, value
            FROM app_settings
            WHERE owner_id = ?
            """,
            (owner_id,),
        ).fetchall()
        return {row["key"]: row["value"] for row in rows}
    finally:
        connection.close()


def get_setting(key: str, default=None):
    owner_id = get_current_owner_id()
    rows = _owner_setting_rows(owner_id)
    return rows.get(key, DEFAULTS.get(key, default))


def _bool_value(value):
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _normalized_tier(value):
    value = str(value or "").strip().lower()
    if value in {"economy", "balanced", "premium"}:
        return value
    return "economy"


def _normalized_provider(value, fallback):
    value = str(value or "").strip().lower()
    return value if value in {"openai", "gemini"} else fallback


def _bounded_int(value, default, minimum, maximum):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(parsed, maximum))


def _resolve_model_tier(settings, provider_key, tier_key, capability):
    provider = settings[provider_key]
    tier = settings[tier_key]
    model = get_model_tier(
        provider,
        capability,
        tier,
        enabled_only=True,
    )
    return provider, tier, model


def _build_runtime_settings(owner_id: str):
    stored = _owner_setting_rows(owner_id)

    # One database read for the whole Settings page.
    raw = {
        key: stored.get(key, value)
        for key, value in DEFAULTS.items()
    }

    raw["planner_provider"] = _normalized_provider(
        raw["planner_provider"],
        "gemini",
    )
    raw["image_provider"] = _normalized_provider(
        raw["image_provider"],
        "openai",
    )
    raw["planner_tier"] = _normalized_tier(raw["planner_tier"])
    raw["image_tier"] = _normalized_tier(raw["image_tier"])

    settings = {
        **raw,
        "batch_concurrency": _bounded_int(
            raw["batch_concurrency"],
            2,
            1,
            4,
        ),
        "confirm_batch_over": _bounded_int(
            raw["confirm_batch_over"],
            4,
            1,
            16,
        ),
        "max_output_count": _bounded_int(
            raw["max_output_count"],
            8,
            1,
            16,
        ),
        "auto_generate_images": _bool_value(raw["auto_generate_images"]),
        "draft_autosave": _bool_value(raw["draft_autosave"]),
    }

    if settings["confirm_batch_over"] > settings["max_output_count"]:
        settings["confirm_batch_over"] = settings["max_output_count"]

    planner_provider, planner_tier, planner_model = _resolve_model_tier(
        settings,
        "planner_provider",
        "planner_tier",
        "planner",
    )
    image_provider, image_tier, image_model = _resolve_model_tier(
        settings,
        "image_provider",
        "image_tier",
        "image",
    )

    settings["planner_tier_available"] = planner_model is not None
    settings["image_tier_available"] = image_model is not None

    settings["planner_resolved_model"] = (
        planner_model["model_id"] if planner_model else None
    )
    settings["image_resolved_model"] = (
        image_model["model_id"] if image_model else None
    )

    settings["planner_tier_note"] = (
        planner_model.get("note")
        if planner_model
        else "This level is currently unavailable. Choose another option."
    )
    settings["image_tier_note"] = (
        image_model.get("note")
        if image_model
        else "This level is currently unavailable. Choose another option."
    )

    # Translate beginner-facing tiers into the legacy runtime keys already
    # consumed by planner/image services. Job snapshots preserve the exact
    # resolved API model and quality used at creation time.
    if planner_model:
        planner_config = planner_model.get("config") or {}
        if planner_provider == "openai":
            settings["openai_planner_model"] = planner_model["model_id"]
            settings["openai_planner_reasoning"] = planner_config.get(
                "reasoning",
                "medium",
            )
        else:
            settings["gemini_planner_model"] = planner_model["model_id"]

    if image_model:
        image_config = image_model.get("config") or {}
        if image_provider == "openai":
            settings["openai_image_model"] = image_model["model_id"]
            settings["openai_image_quality"] = image_config.get(
                "quality",
                "medium",
            )
        else:
            settings["gemini_image_model"] = image_model["model_id"]
            if image_config.get("size"):
                settings["gemini_image_size"] = image_config["size"]

    return settings


def invalidate_runtime_settings_cache(owner_id: str | None = None):
    with _RUNTIME_CACHE_LOCK:
        if owner_id is None:
            _RUNTIME_CACHE.clear()
        else:
            _RUNTIME_CACHE.pop(owner_id, None)


def get_runtime_settings(force_refresh: bool = False):
    owner_id = get_current_owner_id()
    now = time.monotonic()
    generation = get_model_generation()

    if not force_refresh:
        with _RUNTIME_CACHE_LOCK:
            cached = _RUNTIME_CACHE.get(owner_id)

            if cached:
                cached_at, cached_generation, payload = cached
                if (
                    cached_generation == generation
                    and
                    now - cached_at < _RUNTIME_CACHE_TTL_SECONDS
                ):
                    return dict(payload)

    settings = _build_runtime_settings(owner_id)

    with _RUNTIME_CACHE_LOCK:
        _RUNTIME_CACHE[owner_id] = (
            now,
            generation,
            dict(settings),
        )

    return settings


def _validate(values: dict):
    current = {
        key: value
        for key, value in get_runtime_settings().items()
        if key in DEFAULTS
    }
    merged = {**current, **values}

    merged["planner_provider"] = _normalized_provider(
        merged.get("planner_provider"),
        "gemini",
    )
    merged["image_provider"] = _normalized_provider(
        merged.get("image_provider"),
        "openai",
    )
    merged["planner_tier"] = _normalized_tier(merged.get("planner_tier"))
    merged["image_tier"] = _normalized_tier(merged.get("image_tier"))

    planner_model = get_model_tier(
        merged["planner_provider"],
        "planner",
        merged["planner_tier"],
        enabled_only=True,
    )
    if planner_model is None:
        raise ValueError(
            "That prompt quality level is unavailable. Choose another level."
        )

    image_model = get_model_tier(
        merged["image_provider"],
        "image",
        merged["image_tier"],
        enabled_only=True,
    )
    if image_model is None:
        raise ValueError(
            "That image quality level is unavailable. Choose another level."
        )

    merged["batch_concurrency"] = _bounded_int(
        merged.get("batch_concurrency"),
        2,
        1,
        4,
    )
    merged["confirm_batch_over"] = _bounded_int(
        merged.get("confirm_batch_over"),
        4,
        1,
        16,
    )
    merged["max_output_count"] = _bounded_int(
        merged.get("max_output_count"),
        8,
        1,
        16,
    )
    if merged["confirm_batch_over"] > merged["max_output_count"]:
        merged["confirm_batch_over"] = merged["max_output_count"]

    merged["auto_generate_images"] = _bool_value(
        merged.get("auto_generate_images")
    )
    merged["draft_autosave"] = _bool_value(merged.get("draft_autosave"))

    if merged.get("openai_planner_reasoning") not in CATALOG["openai_reasoning"]:
        merged["openai_planner_reasoning"] = "medium"
    if merged.get("openai_image_quality") not in CATALOG["openai_image_quality"]:
        merged["openai_image_quality"] = "medium"
    if merged.get("openai_image_size") not in CATALOG["openai_image_sizes"]:
        merged["openai_image_size"] = "1024x1024"
    if merged.get("gemini_image_size") not in CATALOG["gemini_image_sizes"]:
        merged["gemini_image_size"] = "1K"
    if (
        merged.get("gemini_image_aspect_ratio")
        not in CATALOG["gemini_image_aspect_ratios"]
    ):
        merged["gemini_image_aspect_ratio"] = "1:1"

    return merged


def update_runtime_settings(values: dict):
    ensure_settings_schema()
    validated = _validate(values)
    owner_id = get_current_owner_id()

    # Only write fields the client intentionally changed. Resolved API model
    # IDs stay derived from the Admin registry, so switching a registry model
    # takes effect for new jobs without rewriting every user's settings row.
    keys_to_write = [
        key
        for key in values
        if key in DEFAULTS
    ]

    if not keys_to_write:
        return get_runtime_settings()

    connection = get_connection()
    try:
        for key in keys_to_write:
            value = validated[key]
            if isinstance(value, bool):
                value = "true" if value else "false"

            connection.execute(
                """
                INSERT INTO app_settings (
                    owner_id,
                    key,
                    value,
                    updated_at
                )
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(owner_id, key)
                DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (owner_id, key, str(value)),
            )

        connection.commit()
    finally:
        connection.close()

    invalidate_runtime_settings_cache(
        owner_id
    )

    return get_runtime_settings(
        force_refresh=True
    )


def get_settings_catalog():
    tiers = tier_catalog()
    return {
        **CATALOG,
        "planner_tiers": tiers["planner"],
        "image_tiers": tiers["image"],
    }

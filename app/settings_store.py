import os
from app.database import get_connection
from app.request_context import (
    get_current_owner_id,
    LOCAL_OWNER_ID,
)
from app.model_registry import (
    model_options,
    allowed_model_ids,
)


DEFAULTS = {
    "planner_provider": os.getenv(
        "PLANNER_PROVIDER",
        "gemini"
    ),
    "gemini_planner_model": os.getenv(
        "GEMINI_PROMPT_MODEL",
        "gemini-3.6-flash"
    ),
    "openai_planner_model": os.getenv(
        "OPENAI_PROMPT_MODEL",
        "gpt-5.6-luna"
    ),
    "openai_planner_reasoning": os.getenv(
        "OPENAI_PLANNER_REASONING_EFFORT",
        "low"
    ),
    "image_provider": os.getenv(
        "IMAGE_PROVIDER",
        "openai"
    ),
    "openai_image_model": os.getenv(
        "OPENAI_IMAGE_MODEL",
        "gpt-image-2"
    ),
    "openai_image_quality": os.getenv(
        "OPENAI_IMAGE_QUALITY",
        "low"
    ),
    "openai_image_size": os.getenv(
        "OPENAI_IMAGE_SIZE",
        "1024x1024"
    ),
    "openai_image_output_format": os.getenv(
        "OPENAI_IMAGE_OUTPUT_FORMAT",
        "jpeg"
    ),
    "gemini_image_model": os.getenv(
        "GEMINI_IMAGE_MODEL",
        "gemini-3.1-flash-image"
    ),
    "gemini_image_size": os.getenv(
        "GEMINI_IMAGE_SIZE",
        "1K"
    ),
    "gemini_image_aspect_ratio": os.getenv(
        "GEMINI_IMAGE_ASPECT_RATIO",
        "1:1"
    ),
    "batch_concurrency": os.getenv(
        "IMAGE_BATCH_CONCURRENCY",
        "2"
    ),
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
    "planner_models": {},
    "openai_reasoning": [
        "none",
        "low",
        "medium",
        "high",
    ],
    "image_providers": [
        {"id": "openai", "label": "OpenAI"},
        {"id": "gemini", "label": "Google Gemini"},
    ],
    "image_models": {},
    "openai_image_quality": [
        "low",
        "medium",
        "high",
    ],
    "openai_image_sizes": [
        "1024x1024",
        "1024x1536",
        "1536x1024",
    ],
    "gemini_image_sizes": [
        "1K",
        "2K",
        "4K",
    ],
    "gemini_image_aspect_ratios": [
        "1:1",
        "3:2",
        "2:3",
        "4:3",
        "3:4",
        "16:9",
        "9:16",
    ],
    "batch_concurrency": [
        1,
        2,
        3,
        4,
    ],
    "confirm_batch_over": [
        1,
        4,
        6,
        8,
    ],
    "max_output_count": [
        4,
        6,
        8,
        12,
        16,
    ],
}


def ensure_settings_schema():
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
                    updated_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (
                        owner_id,
                        key
                    )
                )
                """
            )

        elif "owner_id" not in columns:
            connection.execute(
                """
                ALTER TABLE app_settings
                RENAME TO app_settings_legacy
                """
            )

            connection.execute(
                """
                CREATE TABLE app_settings (
                    owner_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (
                        owner_id,
                        key
                    )
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
                SELECT
                    ?,
                    key,
                    value,
                    updated_at
                FROM app_settings_legacy
                """,
                (
                    LOCAL_OWNER_ID,
                ),
            )

            connection.execute(
                """
                DROP TABLE app_settings_legacy
                """
            )

        # Phase compatibility.
        image_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(generated_images)"
            ).fetchall()
        }

        if (
            "generation_note"
            not in
            image_columns
        ):
            connection.execute(
                """
                ALTER TABLE generated_images
                ADD COLUMN generation_note TEXT
                """
            )

        job_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(generation_jobs)"
            ).fetchall()
        }

        if (
            "planner_provider"
            not in
            job_columns
        ):
            connection.execute(
                """
                ALTER TABLE generation_jobs
                ADD COLUMN planner_provider TEXT
                """
            )

        owner_id = (
            get_current_owner_id()
        )

        for key, value in (
            DEFAULTS.items()
        ):
            connection.execute(
                """
                INSERT OR IGNORE INTO app_settings (
                    owner_id,
                    key,
                    value
                )
                VALUES (?, ?, ?)
                """,
                (
                    owner_id,
                    key,
                    str(
                        value
                    ),
                ),
            )

        connection.commit()

    finally:
        connection.close()


def get_setting(
    key: str,
    default=None,
):
    ensure_settings_schema()
    connection = get_connection()

    owner_id = (
        get_current_owner_id()
    )

    try:
        row = connection.execute(
            """
            SELECT value
            FROM app_settings
            WHERE
                owner_id = ?
                AND key = ?
            """,
            (
                owner_id,
                key,
            )
        ).fetchone()

        if row is None:
            return (
                DEFAULTS.get(
                    key,
                    default
                )
            )

        return row["value"]

    finally:
        connection.close()


def _bool_value(
    value,
):
    return str(value).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def get_runtime_settings():
    ensure_settings_schema()

    raw = {
        key: get_setting(
            key,
            value
        )
        for key, value in DEFAULTS.items()
    }

    try:
        concurrency = int(
            raw[
                "batch_concurrency"
            ]
        )
    except (ValueError, TypeError):
        concurrency = 2

    concurrency = max(
        1,
        min(concurrency, 4)
    )

    try:
        confirm_batch_over = int(
            raw[
                "confirm_batch_over"
            ]
        )
    except (
        ValueError,
        TypeError,
    ):
        confirm_batch_over = 4

    try:
        max_output_count = int(
            raw[
                "max_output_count"
            ]
        )
    except (
        ValueError,
        TypeError,
    ):
        max_output_count = 8

    return {
        **raw,
        "batch_concurrency":
            concurrency,
        "confirm_batch_over":
            max(
                1,
                min(
                    confirm_batch_over,
                    16,
                ),
            ),
        "max_output_count":
            max(
                1,
                min(
                    max_output_count,
                    16,
                ),
            ),
        "auto_generate_images":
            _bool_value(
                raw[
                    "auto_generate_images"
                ]
            ),
        "draft_autosave":
            _bool_value(
                raw[
                    "draft_autosave"
                ]
            ),
    }


def _validate(
    values: dict,
):
    current = get_runtime_settings()
    merged = {
        **current,
        **values,
    }

    if merged["planner_provider"] not in {
        "gemini",
        "openai",
    }:
        raise ValueError(
            "Planner provider must be gemini or openai."
        )

    planner_models = (
        allowed_model_ids(
            merged[
                "planner_provider"
            ],
            "planner",
        )
    )

    selected_planner_model = (
        merged[
            "gemini_planner_model"
        ]
        if merged[
            "planner_provider"
        ]
        ==
        "gemini"
        else merged[
            "openai_planner_model"
        ]
    )

    if selected_planner_model not in planner_models:
        raise ValueError(
            "Selected planner model is not supported."
        )

    if merged[
        "openai_planner_reasoning"
    ] not in CATALOG[
        "openai_reasoning"
    ]:
        raise ValueError(
            "Unsupported OpenAI reasoning effort."
        )

    if merged["image_provider"] not in {
        "gemini",
        "openai",
    }:
        raise ValueError(
            "Image provider must be gemini or openai."
        )

    if merged[
        "openai_image_model"
    ] not in (
        allowed_model_ids(
            "openai",
            "image",
        )
    ):
        raise ValueError(
            "Unsupported OpenAI image model."
        )

    if merged[
        "gemini_image_model"
    ] not in (
        allowed_model_ids(
            "gemini",
            "image",
        )
    ):
        raise ValueError(
            "Unsupported Gemini image model."
        )

    if merged[
        "openai_image_quality"
    ] not in CATALOG[
        "openai_image_quality"
    ]:
        raise ValueError(
            "Unsupported OpenAI image quality."
        )

    if merged[
        "openai_image_size"
    ] not in CATALOG[
        "openai_image_sizes"
    ]:
        raise ValueError(
            "Unsupported OpenAI image size."
        )

    # Flash Lite Image only supports 1K.
    if (
        merged[
            "gemini_image_model"
        ]
        ==
        "gemini-3.1-flash-lite-image"
    ):
        merged[
            "gemini_image_size"
        ] = "1K"

    if merged[
        "gemini_image_size"
    ] not in CATALOG[
        "gemini_image_sizes"
    ]:
        raise ValueError(
            "Unsupported Gemini image size."
        )

    if merged[
        "gemini_image_aspect_ratio"
    ] not in CATALOG[
        "gemini_image_aspect_ratios"
    ]:
        raise ValueError(
            "Unsupported Gemini aspect ratio."
        )

    try:
        merged[
            "batch_concurrency"
        ] = max(
            1,
            min(
                int(
                    merged[
                        "batch_concurrency"
                    ]
                ),
                4,
            ),
        )
    except (ValueError, TypeError):
        raise ValueError(
            "Batch concurrency must be between 1 and 4."
        )

    try:
        merged[
            "confirm_batch_over"
        ] = max(
            1,
            min(
                int(
                    merged[
                        "confirm_batch_over"
                    ]
                ),
                16,
            ),
        )
    except (
        ValueError,
        TypeError,
    ):
        raise ValueError(
            "Confirm batch threshold must be between 1 and 16."
        )

    try:
        merged[
            "max_output_count"
        ] = max(
            1,
            min(
                int(
                    merged[
                        "max_output_count"
                    ]
                ),
                16,
            ),
        )
    except (
        ValueError,
        TypeError,
    ):
        raise ValueError(
            "Maximum output count must be between 1 and 16."
        )

    if (
        merged[
            "confirm_batch_over"
        ]
        >
        merged[
            "max_output_count"
        ]
    ):
        merged[
            "confirm_batch_over"
        ] = merged[
            "max_output_count"
        ]

    merged[
        "auto_generate_images"
    ] = _bool_value(
        merged[
            "auto_generate_images"
        ]
    )

    merged[
        "draft_autosave"
    ] = _bool_value(
        merged[
            "draft_autosave"
        ]
    )

    return merged


def update_runtime_settings(
    values: dict,
):
    ensure_settings_schema()
    validated = _validate(
        values
    )

    connection = get_connection()
    owner_id = (
        get_current_owner_id()
    )

    try:
        for key in DEFAULTS:
            if key not in validated:
                continue

            value = validated[
                key
            ]

            if isinstance(
                value,
                bool
            ):
                value = (
                    "true"
                    if value
                    else
                    "false"
                )

            connection.execute(
                """
                INSERT INTO app_settings (
                    owner_id,
                    key,
                    value,
                    updated_at
                )
                VALUES (
                    ?, ?, ?,
                    CURRENT_TIMESTAMP
                )

                ON CONFLICT(
                    owner_id,
                    key
                )
                DO UPDATE SET
                    value =
                        excluded.value,
                    updated_at =
                        CURRENT_TIMESTAMP
                """,
                (
                    owner_id,
                    key,
                    str(
                        value
                    ),
                )
            )

        connection.commit()

    finally:
        connection.close()

    return get_runtime_settings()


def get_settings_catalog():
    return {
        **CATALOG,
        "planner_models": {
            "openai":
                model_options(
                    "openai",
                    "planner",
                ),
            "gemini":
                model_options(
                    "gemini",
                    "planner",
                ),
        },
        "image_models": {
            "openai":
                model_options(
                    "openai",
                    "image",
                ),
            "gemini":
                model_options(
                    "gemini",
                    "image",
                ),
        },
    }

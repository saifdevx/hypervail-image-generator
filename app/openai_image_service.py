import os
from importlib.metadata import PackageNotFoundError, version

from openai import OpenAI

from app.settings_store import get_runtime_settings
from app.credential_store import (
    get_saved_provider_api_key,
)


DEFAULT_OPENAI_IMAGE_MODEL = "gpt-image-2"
DEFAULT_OPENAI_IMAGE_QUALITY = "low"
DEFAULT_OPENAI_IMAGE_SIZE = "1024x1024"
DEFAULT_OPENAI_OUTPUT_FORMAT = "jpeg"

SUPPORTED_QUALITIES = {
    "low",
    "medium",
    "high",
    "auto",
}

SUPPORTED_OUTPUT_FORMATS = {
    "png",
    "jpeg",
    "webp",
}


def get_openai_api_key():
    saved = (
        get_saved_provider_api_key(
            "openai"
        )
    )

    if saved:
        return saved

    value = os.getenv(
        "OPENAI_API_KEY"
    )

    if not value:
        return None

    cleaned = (
        value
        .strip()
        .strip('"')
        .strip("'")
    )

    return cleaned or None


def get_openai_image_model():
    return (
        get_runtime_settings()[
            "openai_image_model"
        ]
    )

def get_openai_image_quality():
    return (
        get_runtime_settings()[
            "openai_image_quality"
        ]
    )

def get_openai_image_size():
    return (
        get_runtime_settings()[
            "openai_image_size"
        ]
    )

def get_openai_output_format():
    return (
        get_runtime_settings()[
            "openai_image_output_format"
        ]
    )

def get_openai_sdk_version():
    try:
        return version(
            "openai"
        )
    except PackageNotFoundError:
        return "unknown"


def create_openai_client(
    api_key: str | None = None,
):
    api_key = (
        api_key
        or
        get_openai_api_key()
    )

    if not api_key:
        return None

    return OpenAI(
        api_key=api_key
    )


def safe_openai_error_message(
    error: Exception,
    api_key: str | None = None,
):
    message = str(
        error
    )

    api_key = (
        api_key
        or
        get_openai_api_key()
    )

    if api_key:
        message = message.replace(
            api_key,
            "[REDACTED]",
        )

    return message[:2000]


def get_openai_image_status():
    return {
        "provider": "openai",
        "configured": bool(
            get_openai_api_key()
        ),
        "model": get_openai_image_model(),
        "quality": get_openai_image_quality(),
        "size": get_openai_image_size(),
        "output_format": get_openai_output_format(),
        "key_source": (
            "saved_connection"
            if get_saved_provider_api_key(
                "openai"
            )
            else (
                "OPENAI_API_KEY"
                if os.getenv(
                    "OPENAI_API_KEY"
                )
                else
                None
            )
        ),
        "sdk_version": get_openai_sdk_version(),
    }


def test_openai_connection(
    api_key_override: str | None = None,
):
    client = create_openai_client(
        api_key_override
    )

    if client is None:
        return {
            "ok": False,
            "error": (
                "OpenAI API key is not configured. "
                "Add OPENAI_API_KEY to .env and restart FastAPI."
            ),
        }

    model = get_openai_image_model()

    try:
        result = client.models.retrieve(
            model
        )

        return {
            "ok": True,
            "provider": "openai",
            "model": getattr(
                result,
                "id",
                model,
            ),
            "sdk_version": get_openai_sdk_version(),
        }

    except Exception as error:
        return {
            "ok": False,
            "provider": "openai",
            "model": model,
            "error": safe_openai_error_message(
                error,
                api_key_override,
            ),
        }

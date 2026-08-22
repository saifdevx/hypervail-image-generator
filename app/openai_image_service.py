import os
from importlib.metadata import PackageNotFoundError, version

from openai import OpenAI


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
        os.getenv(
            "OPENAI_IMAGE_MODEL",
            DEFAULT_OPENAI_IMAGE_MODEL,
        )
        .strip()
        or DEFAULT_OPENAI_IMAGE_MODEL
    )


def get_openai_image_quality():
    value = (
        os.getenv(
            "OPENAI_IMAGE_QUALITY",
            DEFAULT_OPENAI_IMAGE_QUALITY,
        )
        .strip()
        .lower()
    )

    if value not in SUPPORTED_QUALITIES:
        return DEFAULT_OPENAI_IMAGE_QUALITY

    return value


def get_openai_image_size():
    return (
        os.getenv(
            "OPENAI_IMAGE_SIZE",
            DEFAULT_OPENAI_IMAGE_SIZE,
        )
        .strip()
        or DEFAULT_OPENAI_IMAGE_SIZE
    )


def get_openai_output_format():
    value = (
        os.getenv(
            "OPENAI_IMAGE_OUTPUT_FORMAT",
            DEFAULT_OPENAI_OUTPUT_FORMAT,
        )
        .strip()
        .lower()
    )

    if value not in SUPPORTED_OUTPUT_FORMATS:
        return DEFAULT_OPENAI_OUTPUT_FORMAT

    return value


def get_openai_sdk_version():
    try:
        return version(
            "openai"
        )
    except PackageNotFoundError:
        return "unknown"


def create_openai_client():
    api_key = get_openai_api_key()

    if not api_key:
        return None

    return OpenAI(
        api_key=api_key
    )


def safe_openai_error_message(
    error: Exception,
):
    message = str(
        error
    )

    api_key = get_openai_api_key()

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
            "OPENAI_API_KEY"
            if get_openai_api_key()
            else None
        ),
        "sdk_version": get_openai_sdk_version(),
    }


def test_openai_connection():
    client = create_openai_client()

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
                error
            ),
        }

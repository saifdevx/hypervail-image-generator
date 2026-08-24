import os
from importlib.metadata import (
    PackageNotFoundError,
    version,
)
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.credential_store import (
    get_saved_provider_api_key,
)


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

ENV_PATH = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_PATH,
    override=True,
)

DEFAULT_MODEL = "gemini-3.6-flash"


def get_api_key():
    saved = (
        get_saved_provider_api_key(
            "gemini"
        )
    )

    if saved:
        return (
            saved,
            "saved_connection",
        )

    gemini_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if gemini_key:
        cleaned_key = (
            gemini_key
            .strip()
            .strip('"')
            .strip("'")
        )

        if cleaned_key:
            return (
                cleaned_key,
                "GEMINI_API_KEY",
            )

    google_key = os.getenv(
        "GOOGLE_API_KEY"
    )

    if google_key:
        cleaned_key = (
            google_key
            .strip()
            .strip('"')
            .strip("'")
        )

        if cleaned_key:
            return (
                cleaned_key,
                "GOOGLE_API_KEY",
            )

    return (
        None,
        None,
    )


def get_prompt_model():
    model = os.getenv(
        "GEMINI_PROMPT_MODEL",
        DEFAULT_MODEL,
    )

    model = model.strip()

    if not model:
        model = DEFAULT_MODEL

    return model


def get_sdk_version():
    try:
        return version(
            "google-genai"
        )
    except PackageNotFoundError:
        return "unknown"


def create_gemini_client(
    api_key: str | None = None,
):
    if not api_key:
        api_key, _ = get_api_key()

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


def safe_error_message(
    error: Exception,
    api_key: str | None,
):
    message = str(error)

    if api_key:
        message = message.replace(
            api_key,
            "[REDACTED]",
        )

    return message[:1000]


def get_gemini_status():
    api_key, key_source = (
        get_api_key()
    )

    return {
        "provider": "gemini",
        "configured": bool(api_key),
        "model": get_prompt_model(),
        "connection_method": "generate_content",
        "key_source": key_source,
        "sdk_version": get_sdk_version(),
        "env_file_found": ENV_PATH.exists(),
        "store_interactions": False,
    }


def test_gemini_connection(
    api_key_override: str | None = None,
):
    if api_key_override:
        api_key = (
            api_key_override
            .strip()
        )
        key_source = (
            "provided_for_test"
        )
    else:
        api_key, key_source = (
            get_api_key()
        )

    model = get_prompt_model()

    if not api_key:
        return {
            "ok": False,
            "provider": "gemini",
            "model": model,
            "error": (
                "Gemini API key is not configured. "
                "Add GEMINI_API_KEY to your .env file "
                "and restart FastAPI."
            ),
        }

    try:
        client = create_gemini_client(
            api_key
        )

        response = client.models.generate_content(
            model=model,
            contents=(
                "Reply with exactly this text "
                "and nothing else: IMAGE_AGENT_OK"
            ),
        )

        response_text = (
            response.text
            or ""
        ).strip()

        success = (
            "IMAGE_AGENT_OK"
            in response_text
        )

        return {
            "ok": success,
            "provider": "gemini",
            "model": model,
            "connection_method": "generate_content",
            "key_source": key_source,
            "sdk_version": get_sdk_version(),
            "response": response_text[:200],
            "store_interactions": False,
            "error": (
                None
                if success
                else (
                    "Gemini responded successfully, "
                    "but the returned text was unexpected."
                )
            ),
        }

    except Exception as error:
        return {
            "ok": False,
            "provider": "gemini",
            "model": model,
            "connection_method": "generate_content",
            "key_source": key_source,
            "sdk_version": get_sdk_version(),
            "store_interactions": False,
            "error": safe_error_message(
                error,
                api_key,
            ),
        }

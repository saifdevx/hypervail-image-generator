import os

from app.credential_store import (
    get_saved_connection_status,
    get_saved_provider_api_key,
)
from app.request_context import (
    LOCAL_OWNER_ID,
    get_current_owner_id,
)
from app.user_service import get_user


SUPPORTED_PROVIDERS = {
    "openai",
    "gemini",
}


def _clean_provider(provider: str):
    value = str(provider or "").strip().lower()
    if value not in SUPPORTED_PROVIDERS:
        raise ValueError("Unsupported provider.")
    return value


def _server_key(provider: str):
    provider = _clean_provider(provider)

    if provider == "openai":
        value = (os.getenv("OPENAI_API_KEY") or "").strip()
        return (value or None, "OPENAI_API_KEY" if value else None)

    value = (os.getenv("GEMINI_API_KEY") or "").strip()
    if value:
        return value, "GEMINI_API_KEY"

    value = (os.getenv("GOOGLE_API_KEY") or "").strip()
    return (value or None, "GOOGLE_API_KEY" if value else None)


def user_can_use_server_ai_keys(owner_id: str | None = None):
    owner_id = owner_id or get_current_owner_id()

    # Local mode is the developer/admin account and keeps the old local
    # fallback behaviour.
    if owner_id == LOCAL_OWNER_ID:
        return True

    user = get_user(owner_id)
    if not user:
        return False

    if (
        user.get("role") == "admin"
        and user.get("status") == "active"
    ):
        return True

    return bool(
        user.get("status") == "active"
        and int(user.get("allow_server_ai_keys") or 0) == 1
    )


def resolve_provider_api_key(
    provider: str,
    owner_id: str | None = None,
):
    """
    Resolve the credential Hyperex is allowed to use for one account.

    Priority is always the user's own encrypted BYOK key. The Render/.env
    server key is only a fallback for an active Admin account or an account
    explicitly granted access by Admin.
    """
    provider = _clean_provider(provider)
    owner_id = owner_id or get_current_owner_id()

    saved = get_saved_provider_api_key(
        provider,
        owner_id=owner_id,
    )
    if saved:
        return saved, "saved_connection"

    if not user_can_use_server_ai_keys(owner_id):
        return None, None

    key, env_source = _server_key(provider)
    if not key:
        return None, None

    user = get_user(owner_id)
    source = (
        "admin_server_key"
        if owner_id == LOCAL_OWNER_ID
        or (user and user.get("role") == "admin")
        else "admin_server_access"
    )

    # The environment variable name remains server-side. The browser only
    # receives the friendly source above.
    return key, source


def get_provider_access_status(
    owner_id: str | None = None,
):
    owner_id = owner_id or get_current_owner_id()
    saved = get_saved_connection_status(
        owner_id=owner_id,
    )
    server_allowed = user_can_use_server_ai_keys(
        owner_id
    )

    result = {
        "server_ai_access": server_allowed,
    }

    for provider in sorted(SUPPORTED_PROVIDERS):
        saved_item = dict(saved.get(provider) or {})
        is_saved = bool(saved_item.get("saved"))
        server_key, _ = _server_key(provider)
        server_available = bool(server_key)

        if is_saved:
            configured = True
            source = "saved_connection"
        elif server_allowed and server_available:
            configured = True
            user = get_user(owner_id)
            source = (
                "admin_server_key"
                if owner_id == LOCAL_OWNER_ID
                or (user and user.get("role") == "admin")
                else "admin_server_access"
            )
        else:
            configured = False
            source = None

        result[provider] = {
            **saved_item,
            "saved": is_saved,
            "configured": configured,
            "source": source,
            "server_access": server_allowed,
            "server_available": server_available if server_allowed else False,
        }

    return result


def single_saved_provider(
    owner_id: str | None = None,
):
    """Return the user's only saved BYOK provider, otherwise None."""
    owner_id = owner_id or get_current_owner_id()
    saved = get_saved_connection_status(
        owner_id=owner_id,
    )

    providers = [
        provider
        for provider in sorted(SUPPORTED_PROVIDERS)
        if bool((saved.get(provider) or {}).get("saved"))
    ]

    return providers[0] if len(providers) == 1 else None

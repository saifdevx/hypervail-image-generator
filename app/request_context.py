from contextvars import ContextVar


LOCAL_OWNER_ID = "local"

_current_owner_id = ContextVar(
    "image_agent_owner_id",
    default=LOCAL_OWNER_ID,
)

_current_owner_email = ContextVar(
    "image_agent_owner_email",
    default="local@image-agent.dev",
)


def set_current_user(
    owner_id: str,
    email: str | None = None,
):
    owner_token = (
        _current_owner_id.set(
            owner_id
        )
    )

    email_token = (
        _current_owner_email.set(
            email
            or
            ""
        )
    )

    return (
        owner_token,
        email_token,
    )


def reset_current_user(
    tokens,
):
    owner_token, email_token = tokens

    _current_owner_id.reset(
        owner_token
    )

    _current_owner_email.reset(
        email_token
    )


def get_current_owner_id():
    return (
        _current_owner_id.get()
        or
        LOCAL_OWNER_ID
    )


def get_current_owner_email():
    return (
        _current_owner_email.get()
        or
        ""
    )

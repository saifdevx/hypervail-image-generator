import os
from dataclasses import dataclass
from typing import Protocol

import httpx
from fastapi import Request
from fastapi.responses import Response


ACCESS_COOKIE = "hyperex_access"
REFRESH_COOKIE = "hyperex_refresh"

LOCAL_USER_ID = "local"
LOCAL_USER_EMAIL = "local@hyperex.dev"


@dataclass
class AuthSession:
    authenticated: bool
    user_id: str | None = None
    email: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None
    refreshed: bool = False


class AuthAdapter(Protocol):
    async def sign_up(
        self,
        email: str,
        password: str,
    ) -> dict:
        ...

    async def sign_in(
        self,
        email: str,
        password: str,
    ) -> dict:
        ...

    async def resolve_request_session(
        self,
        request: Request,
    ) -> AuthSession:
        ...


class LocalAuthAdapter:
    async def sign_up(
        self,
        email: str,
        password: str,
    ):
        return {
            "ok": True,
            "session": AuthSession(
                authenticated=True,
                user_id=LOCAL_USER_ID,
                email=LOCAL_USER_EMAIL,
            ),
            "needs_confirmation": False,
        }

    async def sign_in(
        self,
        email: str,
        password: str,
    ):
        return {
            "ok": True,
            "session": AuthSession(
                authenticated=True,
                user_id=LOCAL_USER_ID,
                email=LOCAL_USER_EMAIL,
            ),
        }

    async def resolve_request_session(
        self,
        request: Request,
    ):
        return AuthSession(
            authenticated=True,
            user_id=LOCAL_USER_ID,
            email=LOCAL_USER_EMAIL,
        )


class FirebaseAuthAdapter:
    SIGN_UP_URL = (
        "https://identitytoolkit.googleapis.com/"
        "v1/accounts:signUp"
    )

    SIGN_IN_URL = (
        "https://identitytoolkit.googleapis.com/"
        "v1/accounts:signInWithPassword"
    )

    LOOKUP_URL = (
        "https://identitytoolkit.googleapis.com/"
        "v1/accounts:lookup"
    )

    REFRESH_URL = (
        "https://securetoken.googleapis.com/"
        "v1/token"
    )

    def __init__(
        self,
        api_key: str,
    ):
        self.api_key = api_key

    def _url(
        self,
        base: str,
    ):
        return (
            f"{base}?key={self.api_key}"
        )

    @staticmethod
    def _safe_error(
        response: httpx.Response,
    ):
        try:
            payload = response.json()
        except Exception:
            return (
                "Firebase Authentication request failed "
                f"({response.status_code})."
            )

        message = (
            payload.get("error", {})
            .get("message")
        )

        if not message:
            return (
                "Firebase Authentication request failed "
                f"({response.status_code})."
            )

        friendly = {
            "EMAIL_EXISTS":
                "That email already has an account.",
            "EMAIL_NOT_FOUND":
                "No account exists for that email.",
            "INVALID_PASSWORD":
                "The password is incorrect.",
            "INVALID_LOGIN_CREDENTIALS":
                "The email or password is incorrect.",
            "USER_DISABLED":
                "This Firebase account is disabled.",
            "OPERATION_NOT_ALLOWED":
                (
                    "Email/password sign-in is not enabled "
                    "in Firebase Authentication."
                ),
            "WEAK_PASSWORD":
                "Use a stronger password.",
            "TOO_MANY_ATTEMPTS_TRY_LATER":
                (
                    "Firebase temporarily blocked this request "
                    "after too many attempts. Try again later."
                ),
        }

        return friendly.get(
            message,
            message.replace(
                "_",
                " ",
            ).title(),
        )

    @staticmethod
    def _session_from_payload(
        payload: dict,
        refreshed: bool = False,
    ):
        user_id = (
            payload.get("localId")
            or
            payload.get("user_id")
        )

        access_token = (
            payload.get("idToken")
            or
            payload.get("id_token")
        )

        refresh_token = (
            payload.get("refreshToken")
            or
            payload.get("refresh_token")
        )

        if (
            not user_id
            or
            not access_token
        ):
            return AuthSession(
                authenticated=False
            )

        expires_raw = (
            payload.get("expiresIn")
            or
            payload.get("expires_in")
            or
            3600
        )

        try:
            expires_in = int(
                expires_raw
            )
        except (
            TypeError,
            ValueError,
        ):
            expires_in = 3600

        return AuthSession(
            authenticated=True,
            user_id=str(
                user_id
            ),
            email=(
                payload.get("email")
                or
                ""
            ),
            access_token=
                access_token,
            refresh_token=
                refresh_token,
            expires_in=
                expires_in,
            refreshed=
                refreshed,
        )

    async def sign_up(
        self,
        email: str,
        password: str,
    ):
        async with httpx.AsyncClient(
            timeout=20.0
        ) as client:
            response = await client.post(
                self._url(
                    self.SIGN_UP_URL
                ),
                json={
                    "email":
                        email,
                    "password":
                        password,
                    "returnSecureToken":
                        True,
                },
            )

        if response.status_code >= 400:
            return {
                "ok": False,
                "error":
                    self._safe_error(
                        response
                    ),
            }

        session = (
            self._session_from_payload(
                response.json()
            )
        )

        return {
            "ok":
                session.authenticated,
            "session":
                session,
            "needs_confirmation":
                False,
        }

    async def sign_in(
        self,
        email: str,
        password: str,
    ):
        async with httpx.AsyncClient(
            timeout=20.0
        ) as client:
            response = await client.post(
                self._url(
                    self.SIGN_IN_URL
                ),
                json={
                    "email":
                        email,
                    "password":
                        password,
                    "returnSecureToken":
                        True,
                },
            )

        if response.status_code >= 400:
            return {
                "ok": False,
                "error":
                    self._safe_error(
                        response
                    ),
            }

        session = (
            self._session_from_payload(
                response.json()
            )
        )

        return {
            "ok":
                session.authenticated,
            "session":
                session,
        }

    async def _lookup(
        self,
        access_token: str,
    ):
        async with httpx.AsyncClient(
            timeout=15.0
        ) as client:
            response = await client.post(
                self._url(
                    self.LOOKUP_URL
                ),
                json={
                    "idToken":
                        access_token,
                },
            )

        if response.status_code >= 400:
            return AuthSession(
                authenticated=False
            )

        payload = response.json()

        users = (
            payload.get("users")
            or
            []
        )

        if not users:
            return AuthSession(
                authenticated=False
            )

        user = users[0]

        return AuthSession(
            authenticated=True,
            user_id=str(
                user.get("localId")
                or
                ""
            ),
            email=(
                user.get("email")
                or
                ""
            ),
            access_token=
                access_token,
        )

    async def _refresh(
        self,
        refresh_token: str,
    ):
        if not refresh_token:
            return AuthSession(
                authenticated=False
            )

        async with httpx.AsyncClient(
            timeout=20.0
        ) as client:
            response = await client.post(
                self._url(
                    self.REFRESH_URL
                ),
                data={
                    "grant_type":
                        "refresh_token",
                    "refresh_token":
                        refresh_token,
                },
            )

        if response.status_code >= 400:
            return AuthSession(
                authenticated=False
            )

        session = (
            self._session_from_payload(
                response.json(),
                refreshed=True,
            )
        )

        if not session.email:
            lookup = await self._lookup(
                session.access_token
                or
                ""
            )

            session.email = (
                lookup.email
            )

        return session

    async def resolve_request_session(
        self,
        request: Request,
    ):
        access_token = (
            request.cookies.get(
                ACCESS_COOKIE
            )
            or
            ""
        )

        refresh_token = (
            request.cookies.get(
                REFRESH_COOKIE
            )
            or
            ""
        )

        if access_token:
            session = await self._lookup(
                access_token
            )

            if session.authenticated:
                session.refresh_token = (
                    refresh_token
                )

                return session

        if refresh_token:
            return await self._refresh(
                refresh_token
            )

        return AuthSession(
            authenticated=False
        )


def get_auth_provider():
    value = (
        os.getenv(
            "AUTH_PROVIDER",
            os.getenv(
                "AUTH_MODE",
                "local",
            ),
        )
        or
        "local"
    ).strip().lower()

    if value not in {
        "local",
        "firebase",
    }:
        return "local"

    return value


def get_firebase_web_api_key():
    return (
        os.getenv(
            "FIREBASE_WEB_API_KEY"
        )
        or
        ""
    ).strip()


def get_auth_adapter():
    provider = (
        get_auth_provider()
    )

    if provider == "firebase":
        api_key = (
            get_firebase_web_api_key()
        )

        if not api_key:
            raise RuntimeError(
                "AUTH_PROVIDER=firebase but "
                "FIREBASE_WEB_API_KEY is missing."
            )

        return FirebaseAuthAdapter(
            api_key
        )

    return LocalAuthAdapter()


def auth_is_configured():
    if (
        get_auth_provider()
        ==
        "local"
    ):
        return True

    return bool(
        get_firebase_web_api_key()
    )


async def sign_up(
    email: str,
    password: str,
):
    try:
        adapter = (
            get_auth_adapter()
        )
    except RuntimeError as error:
        return {
            "ok": False,
            "error":
                str(
                    error
                ),
        }

    return await adapter.sign_up(
        email,
        password,
    )


async def sign_in(
    email: str,
    password: str,
):
    try:
        adapter = (
            get_auth_adapter()
        )
    except RuntimeError as error:
        return {
            "ok": False,
            "error":
                str(
                    error
                ),
        }

    return await adapter.sign_in(
        email,
        password,
    )


async def resolve_request_session(
    request: Request,
):
    try:
        adapter = (
            get_auth_adapter()
        )
    except RuntimeError:
        return AuthSession(
            authenticated=False
        )

    return (
        await
        adapter.resolve_request_session(
            request
        )
    )


def _cookie_secure(
    request: Request | None = None,
):
    explicit = (
        os.getenv(
            "COOKIE_SECURE"
        )
        or
        ""
    ).strip().lower()

    if explicit in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return True

    if explicit in {
        "0",
        "false",
        "no",
        "off",
    }:
        return False

    if request is not None:
        return (
            request.url.scheme
            ==
            "https"
        )

    return False


def apply_session_cookies(
    response: Response,
    session: AuthSession,
    request: Request | None = None,
):
    if (
        get_auth_provider()
        ==
        "local"
    ):
        return

    secure = (
        _cookie_secure(
            request
        )
    )

    if session.access_token:
        response.set_cookie(
            ACCESS_COOKIE,
            session.access_token,
            httponly=True,
            secure=secure,
            samesite="lax",
            max_age=max(
                60,
                int(
                    session.expires_in
                    or
                    3600
                )
            ),
            path="/",
        )

    if session.refresh_token:
        response.set_cookie(
            REFRESH_COOKIE,
            session.refresh_token,
            httponly=True,
            secure=secure,
            samesite="lax",
            max_age=60
                *
                60
                *
                24
                *
                30,
            path="/",
        )


def clear_session_cookies(
    response: Response,
):
    response.delete_cookie(
        ACCESS_COOKIE,
        path="/",
    )

    response.delete_cookie(
        REFRESH_COOKIE,
        path="/",
    )


def get_auth_public_config():
    return {
        "provider":
            get_auth_provider(),
        "configured":
            auth_is_configured(),
    }

import os
import time
from dataclasses import dataclass
from typing import Protocol

import httpx
from fastapi import Request
from fastapi.responses import Response


ACCESS_COOKIE = "hyperex_access"
REFRESH_COOKIE = "hyperex_refresh"

LOCAL_USER_ID = "local"
LOCAL_USER_EMAIL = "local@hyperex.dev"

OOB_COOLDOWN_SECONDS = 60
_oob_cooldowns: dict[str, float] = {}


@dataclass
class AuthSession:
    authenticated: bool
    user_id: str | None = None
    email: str | None = None
    email_verified: bool = True
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
                email_verified=True,
            ),
            "needs_confirmation": False,
            "verification_sent": False,
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
                email_verified=True,
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
            email_verified=True,
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

    SEND_OOB_URL = (
        "https://identitytoolkit.googleapis.com/"
        "v1/accounts:sendOobCode"
    )

    UPDATE_URL = (
        "https://identitytoolkit.googleapis.com/"
        "v1/accounts:update"
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
    def _firebase_error_code(
        response: httpx.Response,
    ):
        try:
            payload = response.json()
        except Exception:
            return ""

        return str(
            payload.get("error", {})
            .get("message")
            or
            ""
        )

    @classmethod
    def _safe_error(
        cls,
        response: httpx.Response,
    ):
        message = (
            cls._firebase_error_code(
                response
            )
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
                "The email or password is incorrect.",
            "INVALID_PASSWORD":
                "The email or password is incorrect.",
            "INVALID_LOGIN_CREDENTIALS":
                "The email or password is incorrect.",
            "USER_DISABLED":
                "This account is disabled.",
            "OPERATION_NOT_ALLOWED":
                (
                    "Email/password sign-in is not enabled "
                    "for this Firebase project."
                ),
            "WEAK_PASSWORD":
                "Use a stronger password.",
            "TOO_MANY_ATTEMPTS_TRY_LATER":
                (
                    "Too many attempts. Please wait a little "
                    "and try again."
                ),
            "INVALID_EMAIL":
                "Enter a valid email address.",
            "INVALID_ID_TOKEN":
                "Your session expired. Sign in again.",
            "USER_NOT_FOUND":
                "Your account could not be found. Sign in again.",
            "CREDENTIAL_TOO_OLD_LOGIN_AGAIN":
                (
                    "For security, sign out and sign in again "
                    "before changing your password."
                ),
        }

        # Some Firebase errors include suffix/detail text after a colon.
        base_code = (
            message.split(
                " : ",
                1,
            )[0]
        )

        return friendly.get(
            message,
            friendly.get(
                base_code,
                message.replace(
                    "_",
                    " ",
                ).title(),
            ),
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
            email_verified=bool(
                payload.get(
                    "emailVerified",
                    False,
                )
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

        verification = {
            "ok": False,
            "error":
                "Account created, but the verification email could not be sent.",
        }

        if (
            session.authenticated
            and
            session.access_token
        ):
            verification = (
                await
                self.send_verification(
                    session.access_token
                )
            )

        return {
            "ok":
                session.authenticated,
            "session":
                session,
            "needs_confirmation":
                True,
            "verification_sent":
                bool(
                    verification.get(
                        "ok"
                    )
                ),
            "verification_error":
                (
                    None
                    if verification.get(
                        "ok"
                    )
                    else
                    verification.get(
                        "error"
                    )
                ),
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

        if (
            session.authenticated
            and
            session.access_token
        ):
            lookup = await self._lookup(
                session.access_token
            )

            if lookup.authenticated:
                session.email = (
                    lookup.email
                    or
                    session.email
                )
                session.email_verified = (
                    lookup.email_verified
                )

        return {
            "ok":
                session.authenticated,
            "session":
                session,
        }

    async def send_verification(
        self,
        access_token: str,
    ):
        async with httpx.AsyncClient(
            timeout=20.0
        ) as client:
            response = await client.post(
                self._url(
                    self.SEND_OOB_URL
                ),
                json={
                    "requestType":
                        "VERIFY_EMAIL",
                    "idToken":
                        access_token,
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

        payload = response.json()

        return {
            "ok": True,
            "email":
                payload.get(
                    "email"
                ),
        }

    async def send_password_reset(
        self,
        email: str,
    ):
        async with httpx.AsyncClient(
            timeout=20.0
        ) as client:
            response = await client.post(
                self._url(
                    self.SEND_OOB_URL
                ),
                json={
                    "requestType":
                        "PASSWORD_RESET",
                    "email":
                        email,
                },
            )

        if response.status_code >= 400:
            code = (
                self._firebase_error_code(
                    response
                )
            )

            # Do not reveal whether an email is registered.
            if (
                code == "EMAIL_NOT_FOUND"
            ):
                return {
                    "ok": True,
                    "generic": True,
                }

            return {
                "ok": False,
                "error":
                    self._safe_error(
                        response
                    ),
            }

        return {
            "ok": True,
            "generic": True,
        }

    async def change_password(
        self,
        access_token: str,
        new_password: str,
    ):
        async with httpx.AsyncClient(
            timeout=20.0
        ) as client:
            response = await client.post(
                self._url(
                    self.UPDATE_URL
                ),
                json={
                    "idToken":
                        access_token,
                    "password":
                        new_password,
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

        # The update response may not always contain the verification field.
        if (
            session.authenticated
            and
            session.access_token
        ):
            lookup = await self._lookup(
                session.access_token
            )

            if lookup.authenticated:
                session.email = (
                    lookup.email
                    or
                    session.email
                )
                session.email_verified = (
                    lookup.email_verified
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
            email_verified=bool(
                user.get(
                    "emailVerified",
                    False,
                )
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

        if (
            session.authenticated
            and
            session.access_token
        ):
            lookup = await self._lookup(
                session.access_token
            )

            if lookup.authenticated:
                session.email = (
                    lookup.email
                    or
                    session.email
                )
                session.email_verified = (
                    lookup.email_verified
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


def _cooldown_remaining(
    key: str,
):
    now = time.monotonic()
    last = _oob_cooldowns.get(
        key
    )

    if last is None:
        return 0

    elapsed = now - last

    if elapsed >= OOB_COOLDOWN_SECONDS:
        return 0

    return max(
        1,
        int(
            OOB_COOLDOWN_SECONDS
            -
            elapsed
        ),
    )


def _mark_cooldown(
    key: str,
):
    _oob_cooldowns[
        key
    ] = time.monotonic()


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

    result = await adapter.sign_up(
        email,
        password,
    )

    if (
        get_auth_provider()
        ==
        "firebase"
        and
        result.get(
            "verification_sent"
        )
    ):
        session = result.get(
            "session"
        )

        if session:
            _mark_cooldown(
                "verify:"
                +
                str(
                    session.user_id
                    or
                    session.email
                    or
                    ""
                )
            )

    return result


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


async def send_verification_email(
    session: AuthSession,
):
    if (
        get_auth_provider()
        !=
        "firebase"
    ):
        return {
            "ok": True,
            "already_verified": True,
            "retry_after": 0,
        }

    if session.email_verified:
        return {
            "ok": True,
            "already_verified": True,
            "retry_after": 0,
        }

    if (
        not session.authenticated
        or
        not session.access_token
    ):
        return {
            "ok": False,
            "error":
                "Sign in again before requesting another verification email.",
        }

    key = (
        "verify:"
        +
        str(
            session.user_id
            or
            session.email
            or
            ""
        )
    )

    remaining = (
        _cooldown_remaining(
            key
        )
    )

    if remaining:
        return {
            "ok": False,
            "cooldown": True,
            "retry_after":
                remaining,
            "error":
                (
                    "Please wait before requesting "
                    "another verification email."
                ),
        }

    adapter = get_auth_adapter()

    result = (
        await
        adapter.send_verification(
            session.access_token
        )
    )

    if result.get(
        "ok"
    ):
        _mark_cooldown(
            key
        )
        result[
            "retry_after"
        ] = OOB_COOLDOWN_SECONDS

    return result


async def send_password_reset_email(
    email: str,
):
    if (
        get_auth_provider()
        !=
        "firebase"
    ):
        return {
            "ok": True,
            "retry_after": 0,
        }

    clean_email = (
        email
        .strip()
        .lower()
    )

    key = (
        "reset:"
        +
        clean_email
    )

    remaining = (
        _cooldown_remaining(
            key
        )
    )

    if remaining:
        return {
            "ok": False,
            "cooldown": True,
            "retry_after":
                remaining,
            "error":
                "Please wait before requesting another reset email.",
        }

    adapter = get_auth_adapter()

    result = (
        await
        adapter.send_password_reset(
            clean_email
        )
    )

    if result.get(
        "ok"
    ):
        _mark_cooldown(
            key
        )
        result[
            "retry_after"
        ] = OOB_COOLDOWN_SECONDS

    return result


async def change_password(
    session: AuthSession,
    new_password: str,
):
    if (
        get_auth_provider()
        !=
        "firebase"
    ):
        return {
            "ok": False,
            "error":
                "Password changes are only available with Firebase authentication.",
        }

    if (
        not session.authenticated
        or
        not session.access_token
    ):
        return {
            "ok": False,
            "error":
                "Your session expired. Sign in again.",
        }

    adapter = get_auth_adapter()

    return (
        await
        adapter.change_password(
            session.access_token,
            new_password,
        )
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

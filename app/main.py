from contextlib import asynccontextmanager
from pathlib import Path
import re
import os
import secrets

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    Request,
)
from fastapi.responses import (
    FileResponse,
    Response,
    JSONResponse,
    RedirectResponse,
)
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.database import (
    init_database,
    get_database_status,
    get_connection,
)
from app.profile_store import (
    seed_default_profiles,
    list_profiles,
    get_profile,
    get_profile_version,
    list_profile_versions,
    create_profile,
    update_profile_metadata,
    create_profile_version,
    activate_profile_version,
    delete_profile_version,
    set_profile_active,
    permanently_delete_profile,
)
from app.job_store import (
    MAX_IMAGE_BYTES,
    SUPPORTED_JOB_ASPECT_RATIOS,
    ensure_job_schema,
    detect_image_type,
    create_prepared_job,
    get_job,
    get_reference_file,
)
from app.gemini_service import (
    get_gemini_status,
    test_gemini_connection,
)
from app.openai_image_service import (
    get_openai_image_status,
    test_openai_connection,
)
from app.planner_service import (
    plan_job,
    get_planner_status,
    test_selected_planner,
)
from app.normalizer_service import (
    normalize_job,
    get_structured_prompts,
    get_prompt_packages,
)
from app.image_service import (
    get_image_provider_status,
    generate_prompt_image,
    generate_all_prompt_images,
    get_job_images,
    get_image_batch_status,
    get_generated_image_file,
)
from app.settings_store import (
    ensure_settings_schema,
    get_runtime_settings,
    update_runtime_settings,
    get_settings_catalog,
)
from app.results_service import (
    build_job_zip,
    get_download_name,
)
from app.history_service import (
    ensure_history_schema,
    list_history_jobs,
    get_history_options,
    get_history_detail,
    set_job_favorite,
    set_image_favorite,
)
from app.builtin_workflows import (
    sync_builtin_workflows,
    sanitize_profile,
    sanitize_profile_version,
    is_builtin_profile_id,
    is_builtin_workflow_name,
    get_builtin_file_status,
)
from app.credential_store import (
    ensure_credential_schema,
    save_provider_api_key,
    remove_provider_api_key,
    get_saved_connection_status,
)
from app.cleanup_service import (
    delete_generated_image,
    delete_job,
    recover_stale_generations,
    cleanup_orphan_directories,
)
from app.auth_service import (
    get_auth_provider,
    get_auth_public_config,
    sign_up,
    sign_in,
    resolve_request_session,
    apply_session_cookies,
    clear_session_cookies,
)
from app.request_context import (
    set_current_user,
    reset_current_user,
    get_current_owner_id,
    get_current_owner_email,
)
from app.account_service import (
    claim_local_data,
)
from app.user_service import (
    ensure_user_schema,
    ensure_user,
    get_user,
    user_is_admin,
    update_user_access,
)
from app.model_registry import (
    ensure_model_registry_schema,
    list_models,
    update_model,
)
from app.usage_service import (
    ensure_usage_schema,
    record_usage,
    user_usage_summary,
)
from app.admin_service import (
    get_admin_dashboard,
)
from app.platform.queue_backend import (
    get_generation_queue,
    get_queue_provider,
)


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


class ProfileCreateRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=120,
    )
    description: str = Field(
        default="",
        max_length=500,
    )
    system_instruction: str = Field(
        min_length=1,
    )


class ProfileUpdateRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=120,
    )
    description: str = Field(
        default="",
        max_length=500,
    )


class ProfileVersionRequest(BaseModel):
    system_instruction: str = Field(
        min_length=1,
    )


class RegenerateImageRequest(BaseModel):
    extra_direction: str = Field(
        default="",
        max_length=2000,
    )


class SettingsUpdateRequest(BaseModel):
    planner_provider: str | None = None
    gemini_planner_model: str | None = None
    openai_planner_model: str | None = None
    openai_planner_reasoning: str | None = None

    image_provider: str | None = None
    openai_image_model: str | None = None
    openai_image_quality: str | None = None
    openai_image_size: str | None = None
    openai_image_output_format: str | None = None

    gemini_image_model: str | None = None
    gemini_image_size: str | None = None
    gemini_image_aspect_ratio: str | None = None

    batch_concurrency: int | None = None
    auto_generate_images: bool | None = None
    confirm_batch_over: int | None = None
    max_output_count: int | None = None
    draft_autosave: bool | None = None


class ProviderKeyRequest(BaseModel):
    api_key: str = Field(
        min_length=8,
        max_length=1000,
    )


class AuthCredentialsRequest(BaseModel):
    email: str = Field(
        min_length=3,
        max_length=320,
    )
    password: str = Field(
        min_length=6,
        max_length=200,
    )


class AdminModelUpdateRequest(BaseModel):
    model_id: str | None = None
    display_name: str | None = None
    note: str | None = None
    enabled: bool | None = None
    sort_order: int | None = None
    config: dict | None = None


class AdminUserUpdateRequest(BaseModel):
    role: str | None = None
    status: str | None = None


class InternalQueueTask(BaseModel):
    task: str
    job_id: int
    user_id: str
    prompt_id: int | None = None
    regenerate_completed: bool = False
    extra_direction: str = ""


class FavoriteRequest(BaseModel):
    favorite: bool


def normalize_requested_aspect_ratio(
    value: str,
):
    normalized = (
        value
        .strip()
    )

    if (
        normalized
        not in
        SUPPORTED_JOB_ASPECT_RATIOS
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                "Unsupported aspect ratio. "
                "Choose one of: "
                + ", ".join(
                    sorted(
                        SUPPORTED_JOB_ASPECT_RATIOS
                    )
                )
            ),
        )

    return normalized


def require_editable_profile(
    profile_id: int,
):
    profile = get_profile(
        profile_id
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    if is_builtin_profile_id(
        profile_id
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "This is a built-in private workflow. "
                "It can be used for generation, but it "
                "cannot be edited, archived, or deleted."
            ),
        )

    return profile


def require_admin():
    owner_id = (
        get_current_owner_id()
    )

    if not user_is_admin(
        owner_id
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Administrator access required."
            ),
        )

    return get_user(
        owner_id
    )


def normalize_requested_count(
    value: str,
):
    normalized = (
        value
        .strip()
        .lower()
    )

    if normalized == "auto":
        return "auto"

    try:
        number = int(
            normalized
        )
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=(
                "requested_count must be "
                "'auto' or a whole number."
            ),
        )

    if (
        number < 1
        or number > 16
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                "requested_count must be "
                "between 1 and 16."
            ),
        )

    return str(
        number
    )


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    init_database()
    ensure_settings_schema()
    ensure_history_schema()
    ensure_job_schema()
    ensure_credential_schema()
    ensure_user_schema()
    ensure_model_registry_schema()
    ensure_usage_schema()
    seed_default_profiles()
    sync_builtin_workflows()
    ensure_user(
        "local",
        "local@hyperex.dev",
    )
    recover_stale_generations(
        stale_minutes=30
    )
    yield


app = FastAPI(
    title="Hyperex",
    description=(
        "Hyperex AI product image studio"
    ),
    version="0.14.0-phase2-cloud",
    lifespan=lifespan,
)


@app.middleware(
    "http"
)
async def auth_and_security(
    request: Request,
    call_next,
):
    path = request.url.path

    public_api = (
        path.startswith(
            "/api/auth/"
        )
        or
        path == "/health"
        or
        path == "/api/internal/queue/consume"
    )

    should_authenticate = (
        path.startswith(
            "/api/"
        )
        and
        not public_api
    )

    session = None
    context_tokens = None

    if should_authenticate:
        session = (
            await
            resolve_request_session(
                request
            )
        )

        if not session.authenticated:
            return JSONResponse(
                status_code=401,
                content={
                    "detail":
                        "Authentication required."
                },
            )

        app_user = ensure_user(
            session.user_id
            or
            "",
            session.email,
        )

        if (
            not app_user
            or
            app_user.get(
                "status"
            )
            !=
            "active"
        ):
            return JSONResponse(
                status_code=403,
                content={
                    "detail":
                        "This Hyperex account is suspended."
                },
            )

        # Central ownership guard for all existing job/image routes.
        # Service-level filters remain as defense in depth.
        job_match = re.match(
            r"^/api/jobs/(\d+)",
            path,
        )

        history_match = re.match(
            r"^/api/history/(\d+)",
            path,
        )

        image_match = re.match(
            r"^/api/images/(\d+)",
            path,
        )

        connection = None

        try:
            if job_match:
                connection = (
                    get_connection()
                )

                row = connection.execute(
                    """
                    SELECT id
                    FROM generation_jobs
                    WHERE
                        id = ?
                        AND owner_id = ?
                    """,
                    (
                        int(
                            job_match.group(
                                1
                            )
                        ),
                        session.user_id,
                    ),
                ).fetchone()

                if row is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "detail":
                                "Job not found."
                        },
                    )

            elif history_match:
                connection = (
                    get_connection()
                )

                row = connection.execute(
                    """
                    SELECT id
                    FROM generation_jobs
                    WHERE
                        id = ?
                        AND owner_id = ?
                    """,
                    (
                        int(
                            history_match.group(
                                1
                            )
                        ),
                        session.user_id,
                    ),
                ).fetchone()

                if row is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "detail":
                                "Job not found."
                        },
                    )

            elif image_match:
                connection = (
                    get_connection()
                )

                row = connection.execute(
                    """
                    SELECT gi.id
                    FROM generated_images gi

                    JOIN generation_jobs gj
                        ON gj.id =
                            gi.job_id

                    WHERE
                        gi.id = ?
                        AND gj.owner_id = ?
                    """,
                    (
                        int(
                            image_match.group(
                                1
                            )
                        ),
                        session.user_id,
                    ),
                ).fetchone()

                if row is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "detail":
                                "Image not found."
                        },
                    )

        finally:
            if connection is not None:
                connection.close()

        context_tokens = (
            set_current_user(
                session.user_id
                or
                "",
                session.email,
            )
        )

    try:
        response = await call_next(
            request
        )

    finally:
        if context_tokens is not None:
            reset_current_user(
                context_tokens
            )

    if (
        session is not None
        and
        session.refreshed
    ):
        apply_session_cookies(
            response,
            session,
            request,
        )

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    response.headers[
        "X-Frame-Options"
    ] = "DENY"

    response.headers[
        "Referrer-Policy"
    ] = "strict-origin-when-cross-origin"

    response.headers[
        "Permissions-Policy"
    ] = (
        "camera=(self), "
        "microphone=(), "
        "geolocation=()"
    )

    response.headers[
        "Content-Security-Policy"
    ] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )

    if (
        path.startswith(
            "/api/provider-connections"
        )
        or
        path.startswith(
            "/api/auth/"
        )
    ):
        response.headers[
            "Cache-Control"
        ] = "no-store"

    return response


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            STATIC_DIR
        )
    ),
    name="static",
)


@app.get(
    "/",
    include_in_schema=False,
)
def home():
    return FileResponse(
        str(
            STATIC_DIR /
            "index.html"
        )
    )


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# AUTHENTICATION
# ============================================================

@app.get(
    "/api/auth/config"
)
def auth_config():
    return get_auth_public_config()


@app.get(
    "/api/auth/session"
)
async def auth_session(
    request: Request,
):
    session = (
        await
        resolve_request_session(
            request
        )
    )

    app_user = (
        ensure_user(
            session.user_id
            or
            "",
            session.email,
        )
        if session.authenticated
        else
        None
    )

    response = JSONResponse(
        content={
            "authenticated":
                bool(
                    session.authenticated
                ),
            "provider":
                get_auth_provider(),
            "user": (
                {
                    "id":
                        session.user_id,
                    "email":
                        session.email,
                    "role":
                        (
                            app_user.get(
                                "role"
                            )
                            if app_user
                            else
                            "user"
                        ),
                    "status":
                        (
                            app_user.get(
                                "status"
                            )
                            if app_user
                            else
                            "active"
                        ),
                }
                if session.authenticated
                else
                None
            ),
        }
    )

    if (
        session.authenticated
        and
        session.refreshed
    ):
        apply_session_cookies(
            response,
            session,
            request,
        )

    return response


@app.post(
    "/api/auth/signup"
)
async def auth_signup(
    request: Request,
    payload: AuthCredentialsRequest,
):
    result = await sign_up(
        payload.email.strip(),
        payload.password,
    )

    if not result.get(
        "ok"
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                result.get(
                    "error"
                )
                or
                "Sign up failed."
            ),
        )

    session = result.get(
        "session"
    )

    if (
        session
        and
        session.authenticated
    ):
        ensure_user(
            session.user_id
            or
            "",
            session.email,
        )

    response = JSONResponse(
        content={
            "ok":
                True,
            "needs_confirmation":
                bool(
                    result.get(
                        "needs_confirmation"
                    )
                ),
            "authenticated":
                bool(
                    session
                    and
                    session.authenticated
                ),
        }
    )

    if (
        session
        and
        session.authenticated
    ):
        apply_session_cookies(
            response,
            session,
            request,
        )

    return response


@app.post(
    "/api/auth/login"
)
async def auth_login(
    request: Request,
    payload: AuthCredentialsRequest,
):
    result = await sign_in(
        payload.email.strip(),
        payload.password,
    )

    if not result.get(
        "ok"
    ):
        raise HTTPException(
            status_code=401,
            detail=(
                result.get(
                    "error"
                )
                or
                "Login failed."
            ),
        )

    session = result[
        "session"
    ]

    app_user = ensure_user(
        session.user_id
        or
        "",
        session.email,
    )

    response = JSONResponse(
        content={
            "ok":
                True,
            "user": {
                "id":
                    session.user_id,
                "email":
                    session.email,
                "role":
                    (
                        app_user.get(
                            "role"
                        )
                        if app_user
                        else
                        "user"
                    ),
            },
        }
    )

    apply_session_cookies(
        response,
        session,
        request,
    )

    return response


@app.post(
    "/api/auth/logout"
)
def auth_logout():
    response = JSONResponse(
        content={
            "ok": True
        }
    )

    clear_session_cookies(
        response
    )

    return response


@app.get(
    "/api/account"
)
def account_details():
    owner_id = (
        get_current_owner_id()
    )

    user = (
        ensure_user(
            owner_id,
            get_current_owner_email(),
        )
        or
        {}
    )

    return {
        "id":
            owner_id,
        "email":
            get_current_owner_email(),
        "auth_provider":
            get_auth_provider(),
        "role":
            user.get(
                "role",
                "user",
            ),
        "status":
            user.get(
                "status",
                "active",
            ),
        "usage":
            user_usage_summary(
                owner_id
            ),
    }


@app.post(
    "/api/account/claim-local-data"
)
def account_claim_local_data():
    return claim_local_data()


# ============================================================
# ADMIN
# ============================================================

@app.get(
    "/api/admin/dashboard"
)
def admin_dashboard():
    require_admin()

    return get_admin_dashboard()


@app.get(
    "/api/admin/models"
)
def admin_models():
    require_admin()

    return {
        "models":
            list_models()
    }


@app.patch(
    "/api/admin/models/{registry_id}"
)
def admin_model_update(
    registry_id: int,
    request: AdminModelUpdateRequest,
):
    require_admin()

    values = (
        request.model_dump(
            exclude_none=True
        )
    )

    result = update_model(
        registry_id,
        values,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Model registry item not found.",
        )

    return result


@app.patch(
    "/api/admin/users/{user_id}"
)
def admin_user_update(
    user_id: str,
    request: AdminUserUpdateRequest,
):
    require_admin()

    try:
        result = update_user_access(
            user_id,
            role=request.role,
            status=request.status,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(
                error
            ),
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return result


@app.get(
    "/api/database/status"
)
def database_status():
    return get_database_status()


@app.get(
    "/api/builtin-workflows/status"
)
def builtin_workflow_status():
    return {
        "files":
            get_builtin_file_status()
    }


# ============================================================
# PROVIDER CONNECTIONS / USER-OWNED API KEYS
# ============================================================

@app.get(
    "/api/provider-connections"
)
def provider_connections():
    saved = (
        get_saved_connection_status()
    )

    openai_status = (
        get_openai_image_status()
    )

    gemini_status = (
        get_gemini_status()
    )

    return {
        "openai": {
            **saved[
                "openai"
            ],
            "configured":
                bool(
                    openai_status.get(
                        "configured"
                    )
                ),
            "source":
                openai_status.get(
                    "key_source"
                ),
        },
        "gemini": {
            **saved[
                "gemini"
            ],
            "configured":
                bool(
                    gemini_status.get(
                        "configured"
                    )
                ),
            "source":
                gemini_status.get(
                    "key_source"
                ),
        },
    }


@app.post(
    "/api/provider-connections/{provider}"
)
def provider_connection_save(
    provider: str,
    request: ProviderKeyRequest,
):
    provider = (
        provider
        .strip()
        .lower()
    )

    api_key = (
        request
        .api_key
        .strip()
    )

    if provider == "openai":
        test = (
            test_openai_connection(
                api_key_override=
                    api_key
            )
        )

    elif provider == "gemini":
        test = (
            test_gemini_connection(
                api_key_override=
                    api_key
            )
        )

    else:
        raise HTTPException(
            status_code=404,
            detail=(
                "Unsupported provider."
            ),
        )

    if not test.get(
        "ok"
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                test.get(
                    "error"
                )
                or
                "The API key could not be verified."
            ),
        )

    try:
        saved = (
            save_provider_api_key(
                provider,
                api_key,
            )
        )
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(
                error
            ),
        )

    return {
        "ok": True,
        "connection":
            saved,
        "test": {
            "provider":
                test.get(
                    "provider",
                    provider,
                ),
            "model":
                test.get(
                    "model"
                ),
        },
    }


@app.delete(
    "/api/provider-connections/{provider}"
)
def provider_connection_delete(
    provider: str,
):
    provider = (
        provider
        .strip()
        .lower()
    )

    if provider not in {
        "openai",
        "gemini",
    }:
        raise HTTPException(
            status_code=404,
            detail=(
                "Unsupported provider."
            ),
        )

    return remove_provider_api_key(
        provider
    )


# ============================================================
# APPLICATION SETTINGS
# ============================================================

@app.get(
    "/api/settings"
)
def application_settings():
    return {
        "settings":
            get_runtime_settings(),
        "catalog":
            get_settings_catalog(),
        "planner":
            get_planner_status(),
        "image":
            get_image_provider_status(),
    }


@app.patch(
    "/api/settings"
)
def application_settings_update(
    request: SettingsUpdateRequest,
):
    values = {
        key: value
        for key, value
        in request.model_dump().items()
        if value is not None
    }

    try:
        settings = (
            update_runtime_settings(
                values
            )
        )
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(
                error
            ),
        )

    return {
        "settings":
            settings,
        "planner":
            get_planner_status(),
        "image":
            get_image_provider_status(),
    }


@app.get(
    "/api/providers/planner/status"
)
def planner_provider_status():
    return get_planner_status()


@app.post(
    "/api/providers/planner/test"
)
def planner_provider_test():
    result = (
        test_selected_planner()
    )

    if not result.get(
        "ok"
    ):
        raise HTTPException(
            status_code=503,
            detail=(
                result.get(
                    "error"
                )
                or
                "Planner connection test failed."
            ),
        )

    return result


# ============================================================
# GEMINI PROVIDER
# ============================================================

@app.get(
    "/api/providers/gemini/status"
)
def gemini_status():
    return get_gemini_status()


@app.post(
    "/api/providers/gemini/test"
)
def gemini_test():
    result = (
        test_gemini_connection()
    )

    if not result["ok"]:
        raise HTTPException(
            status_code=503,
            detail=(
                result.get("error")
                or
                "Gemini connection test failed."
            ),
        )

    return result


@app.get(
    "/api/providers/image/status"
)
def image_provider_status():
    return get_image_provider_status()


@app.get(
    "/api/providers/gemini/image/status"
)
def gemini_image_status():
    status = get_image_provider_status()
    return status["providers"]["gemini"]


@app.get(
    "/api/providers/openai/image/status"
)
def openai_image_status():
    return get_openai_image_status()


@app.post(
    "/api/providers/openai/test"
)
def openai_test():
    result = test_openai_connection()

    if not result["ok"]:
        raise HTTPException(
            status_code=503,
            detail=(
                result.get("error")
                or
                "OpenAI connection test failed."
            ),
        )

    return result


# ============================================================
# HISTORY / CREATIVE LIBRARY
# ============================================================

@app.get(
    "/api/history"
)
def history_list(
    q: str = "",
    profile_id: int | None = None,
    planner_provider: str | None = None,
    image_provider: str | None = None,
    status: str | None = None,
    favorites_only: bool = False,
    limit: int = 100,
    offset: int = 0,
):
    safe_limit = max(
        1,
        min(
            limit,
            200,
        ),
    )

    safe_offset = max(
        0,
        offset,
    )

    return list_history_jobs(
        q=q,
        profile_id=
            profile_id,
        planner_provider=
            planner_provider,
        image_provider=
            image_provider,
        status=status,
        favorites_only=
            favorites_only,
        limit=
            safe_limit,
        offset=
            safe_offset,
    )


@app.get(
    "/api/history/options"
)
def history_options():
    return get_history_options()


@app.get(
    "/api/history/{job_id}"
)
def history_detail(
    job_id: int,
):
    result = get_history_detail(
        job_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return result


@app.patch(
    "/api/history/{job_id}/favorite"
)
def history_job_favorite(
    job_id: int,
    request: FavoriteRequest,
):
    result = set_job_favorite(
        job_id,
        request.favorite,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return result


@app.patch(
    "/api/images/{image_id}/favorite"
)
def generated_image_favorite(
    image_id: int,
    request: FavoriteRequest,
):
    result = set_image_favorite(
        image_id,
        request.favorite,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Generated image not found."
            ),
        )

    return result


# ============================================================
# PROFILES
# ============================================================

@app.get(
    "/api/profiles"
)
def profiles_list(
    include_archived: bool = False,
):
    return {
        "profiles": [
            sanitize_profile(
                profile
            )
            for profile
            in list_profiles(
                include_inactive=
                    include_archived
            )
        ]
    }


@app.get(
    "/api/profiles/{profile_id}"
)
def profile_details(
    profile_id: int,
):
    profile = get_profile(
        profile_id
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return sanitize_profile(
        profile
    )


@app.post(
    "/api/profiles",
    status_code=201,
)
def profile_create(
    request: ProfileCreateRequest,
):
    name = (
        request.name.strip()
    )

    instruction = (
        request
        .system_instruction
        .strip()
    )

    if not name:
        raise HTTPException(
            status_code=422,
            detail=(
                "Profile name cannot be empty."
            ),
        )

    if not instruction:
        raise HTTPException(
            status_code=422,
            detail=(
                "System instruction cannot be empty."
            ),
        )

    if is_builtin_workflow_name(
        name
    ):
        raise HTTPException(
            status_code=409,
            detail=(
                "That workflow name is reserved "
                "for a built-in private workflow."
            ),
        )

    try:
        return create_profile(
            name=name,
            description=
                request
                .description
                .strip(),
            system_instruction=
                instruction,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(
                error
            ),
        )


@app.patch(
    "/api/profiles/{profile_id}"
)
def profile_update(
    profile_id: int,
    request: ProfileUpdateRequest,
):
    require_editable_profile(
        profile_id
    )

    try:
        profile = (
            update_profile_metadata(
                profile_id=
                    profile_id,
                name=
                    request
                    .name
                    .strip(),
                description=
                    request
                    .description
                    .strip(),
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(
                error
            ),
        )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Active profile not found."
            ),
        )

    return profile


@app.post(
    "/api/profiles/{profile_id}/instruction"
)
def profile_instruction_save(
    profile_id: int,
    request: ProfileVersionRequest,
):
    require_editable_profile(
        profile_id
    )

    instruction = (
        request
        .system_instruction
        .strip()
    )

    if not instruction:
        raise HTTPException(
            status_code=422,
            detail=(
                "System instruction cannot be empty."
            ),
        )

    profile = (
        create_profile_version(
            profile_id=
                profile_id,
            system_instruction=
                instruction,
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Active profile not found."
            ),
        )

    return profile


@app.get(
    "/api/profiles/{profile_id}/versions"
)
def profile_versions(
    profile_id: int,
):
    profile = get_profile(
        profile_id
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    versions = (
        list_profile_versions(
            profile_id
        )
    )

    return {
        "profile_id":
            profile_id,
        "active_version_number":
            profile[
                "active_version_number"
            ],
        "latest_version_number":
            profile[
                "latest_version_number"
            ],
        "versions": [
            sanitize_profile_version(
                profile_id,
                version,
            )
            for version
            in versions
        ],
    }


@app.get(
    "/api/profiles/{profile_id}"
    "/versions/{version_number}"
)
def profile_version_details(
    profile_id: int,
    version_number: int,
):
    profile = (
        get_profile_version(
            profile_id,
            version_number,
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Profile version not found"
            ),
        )

    return sanitize_profile_version(
        profile_id,
        profile,
    )


@app.post(
    "/api/profiles/{profile_id}/versions",
    status_code=201,
)
def profile_version_create(
    profile_id: int,
    request: ProfileVersionRequest,
):
    require_editable_profile(
        profile_id
    )

    instruction = (
        request
        .system_instruction
        .strip()
    )

    if not instruction:
        raise HTTPException(
            status_code=422,
            detail=(
                "System instruction cannot be empty."
            ),
        )

    profile = (
        create_profile_version(
            profile_id=
                profile_id,
            system_instruction=
                instruction,
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Active profile not found."
            ),
        )

    return profile


@app.post(
    "/api/profiles/{profile_id}"
    "/versions/{version_number}/activate"
)
def profile_version_activate(
    profile_id: int,
    version_number: int,
):
    require_editable_profile(
        profile_id
    )

    result = (
        activate_profile_version(
            profile_id,
            version_number,
        )
    )

    if (
        result["status"]
        ==
        "not_found"
    ):
        raise HTTPException(
            status_code=404,
            detail=(
                "Active profile not found."
            ),
        )

    if (
        result["status"]
        ==
        "version_not_found"
    ):
        raise HTTPException(
            status_code=404,
            detail=(
                "Profile version not found."
            ),
        )

    return result


@app.delete(
    "/api/profiles/{profile_id}"
    "/versions/{version_number}"
)
def profile_version_delete(
    profile_id: int,
    version_number: int,
):
    require_editable_profile(
        profile_id
    )

    result = (
        delete_profile_version(
            profile_id,
            version_number,
        )
    )

    status = result[
        "status"
    ]

    messages = {
        "profile_not_found":
            (
                404,
                "Profile not found.",
            ),
        "version_not_found":
            (
                404,
                "Profile version not found.",
            ),
        "last_version":
            (
                409,
                (
                    "You cannot delete the only "
                    "remaining version."
                ),
            ),
        "active_version":
            (
                409,
                (
                    "This version is currently used "
                    "for Generate. Activate another "
                    "version first."
                ),
            ),
        "used_by_jobs":
            (
                409,
                (
                    "This version is used by "
                    "generation history and cannot "
                    "be deleted."
                ),
            ),
    }

    if status in messages:
        code, message = (
            messages[
                status
            ]
        )

        raise HTTPException(
            status_code=code,
            detail=message,
        )

    return result


@app.delete(
    "/api/profiles/{profile_id}"
)
def profile_archive(
    profile_id: int,
):
    require_editable_profile(
        profile_id
    )

    profile = (
        set_profile_active(
            profile_id,
            False,
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return {
        "status": "archived",
        "profile": profile,
    }


@app.post(
    "/api/profiles/{profile_id}/restore"
)
def profile_restore(
    profile_id: int,
):
    require_editable_profile(
        profile_id
    )

    profile = (
        set_profile_active(
            profile_id,
            True,
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return {
        "status": "restored",
        "profile": profile,
    }


@app.delete(
    "/api/profiles/{profile_id}/permanent"
)
def profile_permanent_delete(
    profile_id: int,
):
    require_editable_profile(
        profile_id
    )

    result = (
        permanently_delete_profile(
            profile_id
        )
    )

    if (
        result["status"]
        ==
        "not_found"
    ):
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    if (
        result["status"]
        ==
        "used_by_jobs"
    ):
        raise HTTPException(
            status_code=409,
            detail=(
                "This profile is used by "
                "generation history. Archive "
                "it instead of permanently "
                "deleting it."
            ),
        )

    return result


# ============================================================
# JOBS
# ============================================================

@app.post(
    "/api/jobs",
    status_code=201,
)
async def job_create(
    profile_id: int = Form(...),
    description: str = Form(""),
    requested_count: str = Form(
        "auto"
    ),
    aspect_ratio: str = Form(
        "1:1"
    ),
    files: list[
        UploadFile
    ] = File(...),
):
    if (
        len(files) < 1
        or len(files) > 4
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                "Upload between 1 and 4 "
                "reference images."
            ),
        )

    clean_description = (
        description.strip()
    )

    if (
        len(clean_description)
        >
        5000
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                "Creative direction must be "
                "5000 characters or fewer."
            ),
        )

    clean_requested_count = (
        normalize_requested_count(
            requested_count
        )
    )

    clean_aspect_ratio = (
        normalize_requested_aspect_ratio(
            aspect_ratio
        )
    )

    runtime_settings = (
        get_runtime_settings()
    )

    if (
        clean_requested_count
        !=
        "auto"
        and
        int(
            clean_requested_count
        )
        >
        int(
            runtime_settings[
                "max_output_count"
            ]
        )
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                "Requested output count is above "
                "your configured safety limit."
            ),
        )

    validated_uploads = []

    for position, upload in enumerate(
        files,
        start=1,
    ):
        try:
            data = await upload.read(
                MAX_IMAGE_BYTES + 1
            )
        finally:
            await upload.close()

        if not data:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Image {position} is empty."
                ),
            )

        if (
            len(data)
            >
            MAX_IMAGE_BYTES
        ):
            raise HTTPException(
                status_code=413,
                detail=(
                    f"Image {position} is larger "
                    "than 20 MB."
                ),
            )

        detected = (
            detect_image_type(
                data
            )
        )

        if detected is None:
            raise HTTPException(
                status_code=415,
                detail=(
                    f"Image {position} is not a "
                    "valid PNG, JPG or WEBP file."
                ),
            )

        validated_uploads.append(
            {
                "original_filename":
                    (
                        upload.filename
                        or
                        f"reference_{position}"
                    ),
                "data":
                    data,
                "extension":
                    detected[
                        "extension"
                    ],
                "media_type":
                    detected[
                        "media_type"
                    ],
            }
        )

    result = (
        create_prepared_job(
            profile_id=
                profile_id,
            description=
                clean_description,
            requested_count=
                clean_requested_count,
            aspect_ratio=
                clean_aspect_ratio,
            runtime_settings=
                runtime_settings,
            uploads=
                validated_uploads,
        )
    )

    if (
        result["status"]
        ==
        "profile_unavailable"
    ):
        raise HTTPException(
            status_code=409,
            detail=(
                "The selected profile is "
                "archived, missing, or has no "
                "active generation version."
            ),
        )

    if (
        result["status"]
        ==
        "builtin_instruction_missing"
    ):
        raise HTTPException(
            status_code=503,
            detail=(
                "The private instruction file for "
                f"{result.get('profile_name', 'this workflow')} "
                "is missing. Add the private .txt file under "
                "profiles/private/ and retry."
            ),
        )

    job = result[
        "job"
    ]

    record_usage(
        "job_created",
        job_id=
            job[
                "id"
            ],
        quantity=1,
        metadata={
            "requested_count":
                job.get(
                    "requested_count"
                ),
            "aspect_ratio":
                job.get(
                    "aspect_ratio"
                ),
        },
    )

    return job


@app.get(
    "/api/jobs/{job_id}"
)
def job_details(
    job_id: int,
):
    job = get_job(
        job_id
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    structured = (
        get_structured_prompts(
            job_id
        )
    )

    if structured is not None:
        job["structured"] = (
            structured
        )

    return job


@app.get(
    "/api/jobs/{job_id}"
    "/references/{reference_id}/file",
    include_in_schema=False,
)
def reference_image_file(
    job_id: int,
    reference_id: int,
):
    reference = (
        get_reference_file(
            job_id,
            reference_id,
        )
    )

    if reference is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Reference image not found."
            ),
        )

    if reference.get("signed_url"):
        return RedirectResponse(
            reference["signed_url"],
            status_code=307,
        )

    if reference.get("path") is not None:
        return FileResponse(
            path=str(reference["path"]),
            media_type=reference["media_type"],
        )

    return Response(
        content=b"",
        status_code=404,
    )


# ============================================================
# PLANNER + STRUCTURED PROMPTS
# ============================================================

@app.post(
    "/api/jobs/{job_id}/plan"
)
def job_plan(
    job_id: int,
):
    result = plan_job(
        job_id
    )

    if result["ok"]:
        job = result[
            "job"
        ]

        record_usage(
            "planner_completed",
            job_id=
                job_id,
            provider=
                job.get(
                    "planner_provider"
                ),
            model=
                job.get(
                    "planner_model"
                ),
        )

        return job

    code = result.get(
        "code"
    )

    if code == "job_not_found":
        status_code = 404
    elif code == "provider_not_configured":
        status_code = 503
    else:
        status_code = 502

    raise HTTPException(
        status_code=status_code,
        detail=result.get(
            "error",
            "Prompt planning failed.",
        ),
    )


@app.post(
    "/api/jobs/{job_id}/normalize"
)
def job_normalize(
    job_id: int,
):
    result = normalize_job(
        job_id
    )

    if result["ok"]:
        return result[
            "result"
        ]

    code = result.get(
        "code"
    )

    if code == "job_not_found":
        status_code = 404
    elif code == "missing_raw_plan":
        status_code = 409
    else:
        status_code = 502

    raise HTTPException(
        status_code=status_code,
        detail=result.get(
            "error",
            "Prompt normalization failed.",
        ),
    )


@app.get(
    "/api/jobs/{job_id}/prompts"
)
def job_prompts(
    job_id: int,
):
    result = (
        get_structured_prompts(
            job_id
        )
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return result


@app.get(
    "/api/jobs/{job_id}/packages"
)
def job_prompt_packages(
    job_id: int,
):
    result = get_prompt_packages(
        job_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return result


def _queue_task_response(task: dict, local_callable):
    queue = get_generation_queue()
    dispatched = queue.dispatch(
        task,
        local_callable=local_callable,
    )

    if dispatched.get("queued"):
        return {
            "ok": True,
            "status": "queued",
            "queue_provider": queue.name,
            "task": task,
        }

    return dispatched["result"]


def _run_internal_queue_task(task: InternalQueueTask):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT owner_id
            FROM generation_jobs
            WHERE id = ?
            """,
            (task.job_id,),
        ).fetchone()
    finally:
        connection.close()

    if row is None or row["owner_id"] != task.user_id:
        raise HTTPException(
            status_code=404,
            detail="Queued job not found.",
        )

    tokens = set_current_user(
        task.user_id,
        "",
    )

    try:
        if task.task == "generate_all":
            result = generate_all_prompt_images(
                job_id=task.job_id,
                regenerate_completed=task.regenerate_completed,
            )

            successful = [
                item
                for item in result.get("results", [])
                if item.get("ok")
            ]

            if successful:
                first = successful[0]
                record_usage(
                    "image_generated",
                    job_id=task.job_id,
                    provider=first.get("provider"),
                    model=first.get("model"),
                    quantity=len(successful),
                )

            return result

        if task.task in {"generate_one", "regenerate_one"}:
            if task.prompt_id is None:
                raise HTTPException(
                    status_code=422,
                    detail="Queued image task is missing prompt_id.",
                )

            result = generate_prompt_image(
                task.job_id,
                task.prompt_id,
                extra_direction=(
                    task.extra_direction
                    if task.task == "regenerate_one"
                    else ""
                ),
            )

            if result.get("ok"):
                record_usage(
                    "image_regenerated"
                    if task.task == "regenerate_one"
                    else "image_generated",
                    job_id=task.job_id,
                    provider=result.get("provider"),
                    model=result.get("model"),
                )

            return result

        raise HTTPException(
            status_code=422,
            detail="Unsupported queue task.",
        )

    finally:
        reset_current_user(tokens)


@app.post(
    "/api/internal/queue/consume",
    include_in_schema=False,
)
def internal_queue_consume(
    request: Request,
    task: InternalQueueTask,
):
    expected = (
        os.getenv("HYPEREX_QUEUE_SHARED_SECRET")
        or
        ""
    ).strip()

    supplied = (
        request.headers.get("X-Hyperex-Queue-Secret")
        or
        ""
    ).strip()

    if (
        not expected
        or
        not supplied
        or
        not secrets.compare_digest(expected, supplied)
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid queue worker secret.",
        )

    result = _run_internal_queue_task(task)

    if result.get("code"):
        raise HTTPException(
            status_code=502,
            detail=result.get("error", "Queued generation failed."),
        )

    return {
        "ok": True,
        "result": result,
    }


# ============================================================
# STEP 9 — IMAGE GENERATION
# ============================================================

@app.post(
    "/api/jobs/{job_id}"
    "/prompts/{prompt_id}/generate-image"
)
def prompt_generate_image(
    job_id: int,
    prompt_id: int,
):
    owner_id = get_current_owner_id()

    task = {
        "task": "generate_one",
        "job_id": job_id,
        "user_id": owner_id,
        "prompt_id": prompt_id,
    }

    result = _queue_task_response(
        task,
        lambda: generate_prompt_image(
            job_id,
            prompt_id,
        ),
    )

    if result.get("status") == "queued":
        return result

    if result["ok"]:
        record_usage(
            "image_generated",
            job_id=job_id,
            provider=result.get("provider"),
            model=result.get("model"),
        )
        return result

    code = result.get("code")

    if code == "job_not_found":
        status_code = 404
    elif code in {"package_invalid", "no_references"}:
        status_code = 409
    elif code == "provider_not_configured":
        status_code = 503
    else:
        status_code = 502

    raise HTTPException(
        status_code=status_code,
        detail=result.get("error", "Image generation failed."),
    )


@app.post(
    "/api/jobs/{job_id}"
    "/prompts/{prompt_id}/regenerate-image"
)
def prompt_regenerate_image(
    job_id: int,
    prompt_id: int,
    request: RegenerateImageRequest,
):
    owner_id = get_current_owner_id()
    extra_direction = request.extra_direction.strip()

    task = {
        "task": "regenerate_one",
        "job_id": job_id,
        "user_id": owner_id,
        "prompt_id": prompt_id,
        "extra_direction": extra_direction,
    }

    result = _queue_task_response(
        task,
        lambda: generate_prompt_image(
            job_id,
            prompt_id,
            extra_direction=extra_direction,
        ),
    )

    if result.get("status") == "queued":
        return result

    if result["ok"]:
        record_usage(
            "image_regenerated",
            job_id=job_id,
            provider=result.get("provider"),
            model=result.get("model"),
        )
        return result

    code = result.get("code")

    if code == "job_not_found":
        status_code = 404
    elif code in {"package_invalid", "no_references"}:
        status_code = 409
    elif code == "provider_not_configured":
        status_code = 503
    else:
        status_code = 502

    raise HTTPException(
        status_code=status_code,
        detail=result.get("error", "Image regeneration failed."),
    )


@app.post(
    "/api/jobs/{job_id}/generate-all-images"
)
def job_generate_all_images(
    job_id: int,
    regenerate_completed: bool = False,
):
    owner_id = get_current_owner_id()

    task = {
        "task": "generate_all",
        "job_id": job_id,
        "user_id": owner_id,
        "regenerate_completed": regenerate_completed,
    }

    result = _queue_task_response(
        task,
        lambda: generate_all_prompt_images(
            job_id=job_id,
            regenerate_completed=regenerate_completed,
        ),
    )

    if result.get("status") == "queued":
        return result

    if result.get("code"):
        code = result.get("code")

        if code == "job_not_found":
            status_code = 404
        elif code in {
            "package_invalid",
            "no_references",
            "batch_in_progress",
        }:
            status_code = 409
        elif code == "provider_not_configured":
            status_code = 503
        else:
            status_code = 502

        raise HTTPException(
            status_code=status_code,
            detail=result.get("error", "Batch image generation failed."),
        )

    successful = [
        item
        for item in result.get("results", [])
        if item.get("ok")
    ]

    if successful:
        first = successful[0]
        record_usage(
            "image_generated",
            job_id=job_id,
            provider=first.get("provider"),
            model=first.get("model"),
            quantity=len(successful),
        )

    return result


@app.get(
    "/api/jobs/{job_id}/image-batch"
)
def job_image_batch_status(
    job_id: int,
):
    job = get_job(
        job_id
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    result = get_image_batch_status(
        job_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return result


@app.get(
    "/api/jobs/{job_id}/images"
)
def job_generated_images(
    job_id: int,
):
    job = get_job(
        job_id
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return get_job_images(
        job_id
    )


@app.delete(
    "/api/images/{image_id}"
)
def generated_image_delete(
    image_id: int,
):
    result = (
        delete_generated_image(
            image_id
        )
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Generated image not found."
            ),
        )

    return result


@app.delete(
    "/api/jobs/{job_id}"
)
def generation_job_delete(
    job_id: int,
):
    result = delete_job(
        job_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Job not found."
            ),
        )

    return result


@app.post(
    "/api/maintenance/cleanup"
)
def maintenance_cleanup():
    if get_auth_provider() != "local":
        raise HTTPException(
            status_code=403,
            detail=(
                "Global maintenance is disabled "
                "for normal user accounts."
            ),
        )

    return {
        "stale":
            recover_stale_generations(
                stale_minutes=30
            ),
        "orphans":
            cleanup_orphan_directories(),
    }


@app.get(
    "/api/images/{image_id}/download",
    include_in_schema=False,
)
def generated_image_download(
    image_id: int,
):
    image = (
        get_generated_image_file(
            image_id
        )
    )

    if image is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Generated image not found."
            ),
        )

    filename = (
        get_download_name(
            image_id
        )
        or
        f"image-{image_id}.jpg"
    )

    if image.get("storage_ref"):
        from app.image_service import STORAGE as IMAGE_STORAGE
        signed = IMAGE_STORAGE.signed_get_url(
            image["storage_ref"],
            download_name=filename,
        )
        if signed:
            return RedirectResponse(
                signed,
                status_code=307,
            )

    if image.get("path") is not None:
        return FileResponse(
            path=str(image["path"]),
            media_type=image["media_type"],
            filename=filename,
        )

    raise HTTPException(status_code=404, detail="Generated image file unavailable.")


@app.get(
    "/api/jobs/{job_id}/download.zip",
    include_in_schema=False,
)
def job_download_zip(
    job_id: int,
):
    archive = (
        build_job_zip(
            job_id
        )
    )

    if archive is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "No downloadable job results found."
            ),
        )

    return Response(
        content=
            archive[
                "bytes"
            ],
        media_type=
            "application/zip",
        headers={
            "Content-Disposition":
                (
                    "attachment; filename="
                    f"\"{archive['filename']}\""
                )
        },
    )


@app.get(
    "/api/images/{image_id}/file",
    include_in_schema=False,
)
def generated_image_file(
    image_id: int,
):
    image = (
        get_generated_image_file(
            image_id
        )
    )

    if image is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Generated image not found."
            ),
        )

    if image.get("signed_url"):
        return RedirectResponse(
            image["signed_url"],
            status_code=307,
        )

    if image.get("path") is not None:
        return FileResponse(
            path=str(image["path"]),
            media_type=image["media_type"],
        )

    raise HTTPException(status_code=404, detail="Generated image file unavailable.")

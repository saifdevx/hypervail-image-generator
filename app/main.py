from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.database import (
    init_database,
    get_database_status
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
    permanently_delete_profile
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


# ============================================================
# REQUEST MODELS
# ============================================================

class ProfileCreateRequest(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=120
    )

    description: str = Field(
        default="",
        max_length=500
    )

    system_instruction: str = Field(
        min_length=1
    )


class ProfileUpdateRequest(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=120
    )

    description: str = Field(
        default="",
        max_length=500
    )


class ProfileVersionRequest(BaseModel):

    system_instruction: str = Field(
        min_length=1
    )


# ============================================================
# LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    init_database()

    seed_default_profiles()

    yield


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="Image Agent",
    description=(
        "Custom AI product image generation agent"
    ),
    version="0.4.2",
    lifespan=lifespan,
)


# ============================================================
# STATIC
# ============================================================

app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static",
)


# ============================================================
# FRONTEND
# ============================================================

@app.get(
    "/",
    include_in_schema=False
)
def home():

    return FileResponse(
        str(
            STATIC_DIR /
            "index.html"
        )
    )


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/api/database/status")
def database_status():

    return get_database_status()


# ============================================================
# PROFILES
# ============================================================

@app.get("/api/profiles")
def profiles_list(
    include_archived: bool = False
):

    return {
        "profiles": list_profiles(
            include_inactive=
                include_archived
        )
    }


@app.get(
    "/api/profiles/{profile_id}"
)
def profile_details(
    profile_id: int
):

    profile = get_profile(
        profile_id
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


@app.post(
    "/api/profiles",
    status_code=201
)
def profile_create(
    request: ProfileCreateRequest
):

    name = request.name.strip()

    instruction = (
        request.system_instruction.strip()
    )

    if not name:

        raise HTTPException(
            status_code=422,
            detail=(
                "Profile name cannot be empty."
            )
        )

    if not instruction:

        raise HTTPException(
            status_code=422,
            detail=(
                "System instruction cannot be empty."
            )
        )

    return create_profile(
        name=name,
        description=(
            request.description.strip()
        ),
        system_instruction=
            instruction
    )


@app.patch(
    "/api/profiles/{profile_id}"
)
def profile_update(
    profile_id: int,
    request: ProfileUpdateRequest
):

    profile = update_profile_metadata(
        profile_id=profile_id,
        name=request.name.strip(),
        description=(
            request.description.strip()
        )
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Active profile not found."
            )
        )

    return profile


# ============================================================
# VERSIONS
# ============================================================

@app.get(
    "/api/profiles/{profile_id}/versions"
)
def profile_versions(
    profile_id: int
):

    profile = get_profile(
        profile_id
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return {
        "profile_id": profile_id,
        "active_version_number":
            profile[
                "active_version_number"
            ],
        "latest_version_number":
            profile[
                "latest_version_number"
            ],
        "versions":
            list_profile_versions(
                profile_id
            )
    }


@app.get(
    "/api/profiles/{profile_id}/versions/{version_number}"
)
def profile_version_details(
    profile_id: int,
    version_number: int
):

    profile = get_profile_version(
        profile_id,
        version_number
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Profile version not found"
            )
        )

    return profile


@app.post(
    "/api/profiles/{profile_id}/versions",
    status_code=201
)
def profile_version_create(
    profile_id: int,
    request: ProfileVersionRequest
):

    instruction = (
        request.system_instruction.strip()
    )

    if not instruction:

        raise HTTPException(
            status_code=422,
            detail=(
                "System instruction cannot be empty."
            )
        )

    profile = create_profile_version(
        profile_id=profile_id,
        system_instruction=
            instruction
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Active profile not found."
            )
        )

    return profile


@app.post(
    "/api/profiles/{profile_id}/versions/{version_number}/activate"
)
def profile_version_activate(
    profile_id: int,
    version_number: int
):

    result = activate_profile_version(
        profile_id,
        version_number
    )

    if result["status"] == "not_found":

        raise HTTPException(
            status_code=404,
            detail=(
                "Active profile not found."
            )
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
            )
        )

    return result


@app.delete(
    "/api/profiles/{profile_id}/versions/{version_number}"
)
def profile_version_delete(
    profile_id: int,
    version_number: int
):

    result = delete_profile_version(
        profile_id,
        version_number
    )

    status = result["status"]

    if status == "profile_not_found":

        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    if status == "version_not_found":

        raise HTTPException(
            status_code=404,
            detail=(
                "Profile version not found."
            )
        )

    if status == "last_version":

        raise HTTPException(
            status_code=409,
            detail=(
                "You cannot delete the only "
                "remaining version."
            )
        )

    if status == "active_version":

        raise HTTPException(
            status_code=409,
            detail=(
                "This version is currently used "
                "for Generate. Activate another "
                "version before deleting it."
            )
        )

    if status == "used_by_jobs":

        raise HTTPException(
            status_code=409,
            detail=(
                "This version is already used "
                "by generation history and "
                "cannot be deleted."
            )
        )

    return result


# ============================================================
# ARCHIVE / RESTORE
# ============================================================

@app.delete(
    "/api/profiles/{profile_id}"
)
def profile_archive(
    profile_id: int
):

    profile = set_profile_active(
        profile_id,
        False
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return {
        "status": "archived",
        "profile": profile
    }


@app.post(
    "/api/profiles/{profile_id}/restore"
)
def profile_restore(
    profile_id: int
):

    profile = set_profile_active(
        profile_id,
        True
    )

    if profile is None:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return {
        "status": "restored",
        "profile": profile
    }


# ============================================================
# PERMANENT DELETE
# ============================================================

@app.delete(
    "/api/profiles/{profile_id}/permanent"
)
def profile_permanent_delete(
    profile_id: int
):

    result = permanently_delete_profile(
        profile_id
    )

    if result["status"] == "not_found":

        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    if result["status"] == "used_by_jobs":

        raise HTTPException(
            status_code=409,
            detail=(
                "This profile is used by "
                "generation history. Archive "
                "it instead of permanently "
                "deleting it."
            )
        )

    return result
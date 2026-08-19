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
    set_profile_active
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
# APPLICATION LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    init_database()

    seed_default_profiles()

    yield


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Image Agent",
    description=(
        "Custom AI product image generation agent"
    ),
    version="0.4.1",
    lifespan=lifespan,
)


# ============================================================
# STATIC FILES
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


# ============================================================
# DATABASE STATUS
# ============================================================

@app.get(
    "/api/database/status"
)
def database_status():

    return get_database_status()


# ============================================================
# LIST PROFILES
# ============================================================

@app.get(
    "/api/profiles"
)
def profiles_list(
    include_archived: bool = False
):

    return {
        "profiles": list_profiles(
            include_inactive=include_archived
        )
    }


# ============================================================
# GET PROFILE
# ============================================================

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


# ============================================================
# GET PROFILE VERSION HISTORY
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
        "versions": list_profile_versions(
            profile_id
        )
    }


# ============================================================
# GET SPECIFIC PROFILE VERSION
# ============================================================

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
            detail="Profile version not found"
        )


    return profile


# ============================================================
# CREATE PROFILE
# ============================================================

@app.post(
    "/api/profiles",
    status_code=201
)
def profile_create(
    request: ProfileCreateRequest
):

    name = request.name.strip()

    description = (
        request.description.strip()
    )

    instruction = (
        request.system_instruction.strip()
    )


    if not name:

        raise HTTPException(
            status_code=422,
            detail="Profile name cannot be empty."
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
        description=description,
        system_instruction=instruction
    )


# ============================================================
# UPDATE PROFILE DETAILS
# ============================================================

@app.patch(
    "/api/profiles/{profile_id}"
)
def profile_update(
    profile_id: int,
    request: ProfileUpdateRequest
):

    name = request.name.strip()

    description = (
        request.description.strip()
    )


    if not name:

        raise HTTPException(
            status_code=422,
            detail="Profile name cannot be empty."
        )


    profile = update_profile_metadata(
        profile_id=profile_id,
        name=name,
        description=description
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
# CREATE NEW PROFILE VERSION
# ============================================================

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
        system_instruction=instruction
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
# ARCHIVE PROFILE
# ============================================================

@app.delete(
    "/api/profiles/{profile_id}"
)
def profile_archive(
    profile_id: int
):

    profile = set_profile_active(
        profile_id=profile_id,
        is_active=False
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


# ============================================================
# RESTORE PROFILE
# ============================================================

@app.post(
    "/api/profiles/{profile_id}/restore"
)
def profile_restore(
    profile_id: int
):

    profile = set_profile_active(
        profile_id=profile_id,
        is_active=True
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
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
    create_profile,
    create_profile_version
)


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

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


class ProfileVersionRequest(BaseModel):
    system_instruction: str = Field(
        min_length=1
    )


# --------------------------------------------------
# APPLICATION LIFESPAN
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Make sure database tables exist.
    init_database()

    # Import built-in profiles only if
    # they do not already exist.
    seed_default_profiles()

    yield


# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Image Agent",
    description=(
        "Custom AI product image generation agent"
    ),
    version="0.4.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static",
)


# --------------------------------------------------
# FRONTEND
# --------------------------------------------------

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


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

@app.get("/api/database/status")
def database_status():
    return get_database_status()


# --------------------------------------------------
# PROFILE LIST
# --------------------------------------------------

@app.get("/api/profiles")
def profiles_list():
    return {
        "profiles": list_profiles()
    }


# --------------------------------------------------
# PROFILE DETAILS
# --------------------------------------------------

@app.get("/api/profiles/{profile_id}")
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


# --------------------------------------------------
# CREATE PROFILE
# --------------------------------------------------

@app.post(
    "/api/profiles",
    status_code=201
)
def profile_create(
    request: ProfileCreateRequest
):
    return create_profile(
        name=request.name,
        description=request.description,
        system_instruction=(
            request.system_instruction
        )
    )


# --------------------------------------------------
# SAVE NEW PROFILE VERSION
# --------------------------------------------------

@app.post(
    "/api/profiles/{profile_id}/versions",
    status_code=201
)
def profile_version_create(
    profile_id: int,
    request: ProfileVersionRequest
):
    profile = create_profile_version(
        profile_id=profile_id,
        system_instruction=(
            request.system_instruction
        )
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile
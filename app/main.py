from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form
)
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

from app.job_store import (
    MAX_IMAGE_BYTES,
    detect_image_type,
    create_prepared_job,
    get_job,
    get_reference_file
)

from app.gemini_service import (
    get_gemini_status,
    test_gemini_connection
)

from app.planner_service import (
    plan_job
)


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


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


def normalize_requested_count(
    value: str
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
            )
        )

    if number < 1 or number > 16:
        raise HTTPException(
            status_code=422,
            detail=(
                "requested_count must be "
                "between 1 and 16."
            )
        )

    return str(
        number
    )


@asynccontextmanager
async def lifespan(
    app: FastAPI
):
    init_database()
    seed_default_profiles()
    yield


app = FastAPI(
    title="Image Agent",
    description=(
        "Custom AI product image generation agent"
    ),
    version="0.7.0",
    lifespan=lifespan,
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static",
)


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


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get(
    "/api/database/status"
)
def database_status():
    return get_database_status()


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
    result = test_gemini_connection()

    if not result["ok"]:
        raise HTTPException(
            status_code=503,
            detail=(
                result.get("error")
                or
                "Gemini connection test failed."
            )
        )

    return result


# ============================================================
# PROFILES
# ============================================================

@app.get(
    "/api/profiles"
)
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
        request.system_instruction
        .strip()
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

        "versions":
            list_profile_versions(
                profile_id
            )
    }


@app.get(
    "/api/profiles/{profile_id}"
    "/versions/{version_number}"
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
        request.system_instruction
        .strip()
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
    "/api/profiles/{profile_id}"
    "/versions/{version_number}"
    "/activate"
)
def profile_version_activate(
    profile_id: int,
    version_number: int
):
    result = activate_profile_version(
        profile_id,
        version_number
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
    "/api/profiles/{profile_id}"
    "/versions/{version_number}"
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
                "This version is currently "
                "used for Generate. Activate "
                "another version first."
            )
        )

    if status == "used_by_jobs":
        raise HTTPException(
            status_code=409,
            detail=(
                "This version is used by "
                "generation history and "
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


# ============================================================
# GENERATION JOBS
# ============================================================

@app.post(
    "/api/jobs",
    status_code=201
)
async def job_create(
    profile_id: int = Form(...),
    description: str = Form(""),
    requested_count: str = Form("auto"),
    files: list[UploadFile] = File(...)
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
            )
        )

    clean_description = (
        description.strip()
    )

    if len(clean_description) > 5000:
        raise HTTPException(
            status_code=422,
            detail=(
                "Creative direction must be "
                "5000 characters or fewer."
            )
        )

    clean_requested_count = (
        normalize_requested_count(
            requested_count
        )
    )

    validated_uploads = []

    for position, upload in enumerate(
        files,
        start=1
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
                )
            )

        if len(data) > MAX_IMAGE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"Image {position} is larger "
                    "than 20 MB."
                )
            )

        detected = detect_image_type(
            data
        )

        if detected is None:
            raise HTTPException(
                status_code=415,
                detail=(
                    f"Image {position} is not a "
                    "valid PNG, JPG or WEBP file."
                )
            )

        original_filename = (
            upload.filename
            or
            f"reference_{position}"
        )

        validated_uploads.append(
            {
                "original_filename":
                    original_filename,

                "data":
                    data,

                "extension":
                    detected[
                        "extension"
                    ],

                "media_type":
                    detected[
                        "media_type"
                    ]
            }
        )

    result = create_prepared_job(
        profile_id=profile_id,
        description=clean_description,
        requested_count=
            clean_requested_count,
        uploads=validated_uploads
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
            )
        )

    return result["job"]


@app.post(
    "/api/jobs/{job_id}/plan"
)
def job_plan(
    job_id: int
):
    result = plan_job(
        job_id
    )

    if result["ok"]:
        return result["job"]

    code = result.get(
        "code"
    )

    if code == "job_not_found":
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    if code == "no_references":
        raise HTTPException(
            status_code=409,
            detail=result["error"]
        )

    if code == "gemini_not_configured":
        raise HTTPException(
            status_code=503,
            detail=result["error"]
        )

    raise HTTPException(
        status_code=502,
        detail=(
            result.get("error")
            or
            "Gemini prompt planning failed."
        )
    )


@app.get(
    "/api/jobs/{job_id}"
)
def job_details(
    job_id: int
):
    job = get_job(
        job_id
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return job


@app.get(
    "/api/jobs/{job_id}"
    "/references/{reference_id}"
    "/file",
    include_in_schema=False
)
def reference_image_file(
    job_id: int,
    reference_id: int
):
    reference = get_reference_file(
        job_id,
        reference_id
    )

    if reference is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Reference image not found."
            )
        )

    return FileResponse(
        path=str(
            reference["path"]
        ),
        media_type=
            reference["media_type"]
    )

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.database import (
    init_database,
    get_database_status,
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
    seed_default_profiles()
    yield


app = FastAPI(
    title="Image Agent",
    description=(
        "Custom AI product image generation agent"
    ),
    version="0.11.0",
    lifespan=lifespan,
)


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


@app.get(
    "/api/database/status"
)
def database_status():
    return get_database_status()


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
# PROFILES
# ============================================================

@app.get(
    "/api/profiles"
)
def profiles_list(
    include_archived: bool = False,
):
    return {
        "profiles":
            list_profiles(
                include_inactive=
                    include_archived
            )
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

    return profile


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

    return create_profile(
        name=name,
        description=
            request
            .description
            .strip(),
        system_instruction=
            instruction,
    )


@app.patch(
    "/api/profiles/{profile_id}"
)
def profile_update(
    profile_id: int,
    request: ProfileUpdateRequest,
):
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
            ),
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

    return profile


@app.post(
    "/api/profiles/{profile_id}/versions",
    status_code=201,
)
def profile_version_create(
    profile_id: int,
    request: ProfileVersionRequest,
):
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

    return result["job"]


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

    return FileResponse(
        path=str(
            reference["path"]
        ),
        media_type=
            reference[
                "media_type"
            ],
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
        return result["job"]

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
    result = (
        generate_prompt_image(
            job_id,
            prompt_id,
        )
    )

    if result["ok"]:
        return result

    code = result.get(
        "code"
    )

    if code == "job_not_found":
        status_code = 404
    elif code in {
        "package_invalid",
        "no_references",
    }:
        status_code = 409
    elif code == "provider_not_configured":
        status_code = 503
    else:
        status_code = 502

    raise HTTPException(
        status_code=status_code,
        detail=result.get(
            "error",
            "Image generation failed.",
        ),
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
    result = (
        generate_prompt_image(
            job_id,
            prompt_id,
            extra_direction=
                request
                .extra_direction
                .strip(),
        )
    )

    if result["ok"]:
        return result

    code = result.get(
        "code"
    )

    if code == "job_not_found":
        status_code = 404
    elif code in {
        "package_invalid",
        "no_references",
    }:
        status_code = 409
    elif code == "provider_not_configured":
        status_code = 503
    else:
        status_code = 502

    raise HTTPException(
        status_code=status_code,
        detail=result.get(
            "error",
            "Image regeneration failed.",
        ),
    )


@app.post(
    "/api/jobs/{job_id}/generate-all-images"
)
def job_generate_all_images(
    job_id: int,
    regenerate_completed: bool = False,
):
    result = generate_all_prompt_images(
        job_id=job_id,
        regenerate_completed=regenerate_completed,
    )

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
            detail=result.get(
                "error",
                "Batch image generation failed.",
            ),
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

    return FileResponse(
        path=str(
            image["path"]
        ),
        media_type=
            image[
                "media_type"
            ],
        filename=
            filename,
    )


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

    return FileResponse(
        path=str(
            image["path"]
        ),
        media_type=
            image[
                "media_type"
            ],
    )

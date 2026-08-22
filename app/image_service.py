import base64
import os

from google.genai import types

from app.database import get_connection
from app.gemini_service import (
    create_gemini_client,
    get_api_key,
    safe_error_message,
)
from app.job_store import (
    BASE_DIR,
    get_job_for_planning,
)
from app.normalizer_service import (
    get_prompt_packages,
)


DEFAULT_IMAGE_MODEL = "gemini-3.1-flash-image"
DEFAULT_IMAGE_SIZE = "1K"
DEFAULT_ASPECT_RATIO = "1:1"

SUPPORTED_IMAGE_SIZES = {
    "1K",
    "2K",
    "4K",
}

SUPPORTED_ASPECT_RATIOS = {
    "1:1",
    "1:4",
    "1:8",
    "2:3",
    "3:2",
    "3:4",
    "4:1",
    "4:3",
    "4:5",
    "5:4",
    "8:1",
    "9:16",
    "16:9",
    "21:9",
}

OUTPUTS_DIR = (
    BASE_DIR /
    "data" /
    "outputs"
)


def get_image_model():
    return (
        os.getenv(
            "GEMINI_IMAGE_MODEL",
            DEFAULT_IMAGE_MODEL,
        )
        .strip()
        or DEFAULT_IMAGE_MODEL
    )


def get_image_size():
    value = (
        os.getenv(
            "GEMINI_IMAGE_SIZE",
            DEFAULT_IMAGE_SIZE,
        )
        .strip()
        .upper()
    )

    if value not in SUPPORTED_IMAGE_SIZES:
        return DEFAULT_IMAGE_SIZE

    return value


def get_image_aspect_ratio():
    value = (
        os.getenv(
            "GEMINI_IMAGE_ASPECT_RATIO",
            DEFAULT_ASPECT_RATIO,
        )
        .strip()
    )

    if value not in SUPPORTED_ASPECT_RATIOS:
        return DEFAULT_ASPECT_RATIO

    return value


def get_image_provider_status():
    api_key, key_source = get_api_key()

    return {
        "provider": "gemini",
        "configured": bool(api_key),
        "model": get_image_model(),
        "image_size": get_image_size(),
        "aspect_ratio":
            get_image_aspect_ratio(),
        "key_source": key_source,
        "billing_required": True,
        "free_tier_available": False,
    }


def _create_image_record(
    job_id: int,
    prompt_id: int,
):
    connection = get_connection()

    try:
        provider_label = (
            "gemini:"
            f"{get_image_model()}:"
            f"{get_image_size()}:"
            f"{get_image_aspect_ratio()}"
        )

        cursor = connection.execute(
            """
            INSERT INTO generated_images (
                job_id,
                prompt_id,
                provider,
                status
            )
            VALUES (?, ?, ?, 'generating')
            """,
            (
                job_id,
                prompt_id,
                provider_label,
            ),
        )

        image_id = cursor.lastrowid
        connection.commit()
        return image_id

    finally:
        connection.close()


def _mark_image_complete(
    image_id: int,
    relative_path: str,
):
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generated_images
            SET
                file_path = ?,
                status = 'complete',
                error_message = NULL
            WHERE id = ?
            """,
            (
                relative_path,
                image_id,
            ),
        )
        connection.commit()

    finally:
        connection.close()


def _mark_image_failed(
    image_id: int,
    error_message: str,
):
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generated_images
            SET
                status = 'failed',
                error_message = ?
            WHERE id = ?
            """,
            (
                error_message[:2000],
                image_id,
            ),
        )
        connection.commit()

    finally:
        connection.close()


def get_job_images(
    job_id: int,
):
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                gi.id,
                gi.job_id,
                gi.prompt_id,
                gi.provider,
                gi.file_path,
                gi.status,
                gi.error_message,
                gi.created_at,
                gp.position AS prompt_position,
                gp.title AS prompt_title
            FROM generated_images gi
            LEFT JOIN generated_prompts gp
                ON gp.id = gi.prompt_id
            WHERE gi.job_id = ?
            ORDER BY
                gi.created_at ASC,
                gi.id ASC
            """,
            (job_id,),
        ).fetchall()

        images = []

        for row in rows:
            item = dict(row)

            if (
                item["status"] == "complete"
                and item["file_path"]
            ):
                item["file_url"] = (
                    f"/api/images/"
                    f"{item['id']}/file"
                )
            else:
                item["file_url"] = None

            images.append(item)

        return {
            "job_id": job_id,
            "image_count": len(images),
            "images": images,
        }

    finally:
        connection.close()


def get_generated_image_file(
    image_id: int,
):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                file_path,
                status
            FROM generated_images
            WHERE id = ?
            """,
            (image_id,),
        ).fetchone()

        if (
            row is None
            or row["status"] != "complete"
            or not row["file_path"]
        ):
            return None

        path = (
            BASE_DIR /
            row["file_path"]
        ).resolve()

        outputs_root = (
            OUTPUTS_DIR
        ).resolve()

        if (
            path != outputs_root
            and outputs_root not in path.parents
        ):
            return None

        if not path.exists():
            return None

        _, media_type = (
            _media_type_from_bytes(
                path.read_bytes()
            )
        )

        return {
            "path": path,
            "media_type": media_type,
        }

    finally:
        connection.close()


def _find_verified_package(
    job_id: int,
    prompt_id: int,
):
    packages = get_prompt_packages(
        job_id
    )

    if packages is None:
        return None, "Job not found."

    if not packages.get(
        "source_verified"
    ):
        return None, (
            "This job does not have "
            "source-verified prompt packages."
        )

    for package in packages.get(
        "packages",
        []
    ):
        if (
            int(
                package[
                    "prompt_id"
                ]
            )
            ==
            int(prompt_id)
        ):
            if not package.get(
                "positive_lossless_verified"
            ):
                return None, (
                    "Positive prompt failed "
                    "source verification."
                )

            shared_negative = (
                package.get(
                    "shared_negative_text"
                )
                or ""
            )

            if (
                shared_negative
                and not package.get(
                    "shared_negative_lossless_verified"
                )
            ):
                return None, (
                    "Shared negative constraints "
                    "failed source verification."
                )

            return package, None

    return None, (
        "Prompt package not found "
        "for this job."
    )


def _build_image_contents(
    job: dict,
    package: dict,
):
    contents = []

    for reference in job[
        "references"
    ]:
        contents.append(
            (
                f"Reference Image "
                f"{reference['position']} "
                f"({reference['original_filename']}):"
            )
        )

        image_bytes = (
            reference[
                "absolute_path"
            ]
            .read_bytes()
        )

        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=
                    reference[
                        "media_type"
                    ],
            )
        )

    contents.append(
        (
            "Generate one image from the exact "
            "source-verified image prompt below. "
            "Use the ordered reference images above "
            "where the prompt refers to Reference/Image 1, "
            "Reference/Image 2, and so on.\n\n"
            "EXACT IMAGE PROMPT:\n"
            f"{package['final_input']}"
        )
    )

    return contents


def _media_type_from_bytes(
    data: bytes,
):
    if data.startswith(
        b"\x89PNG\r\n\x1a\n"
    ):
        return (
            ".png",
            "image/png",
        )

    if data.startswith(
        b"\xff\xd8\xff"
    ):
        return (
            ".jpg",
            "image/jpeg",
        )

    if (
        len(data) >= 12
        and data[0:4] == b"RIFF"
        and data[8:12] == b"WEBP"
    ):
        return (
            ".webp",
            "image/webp",
        )

    return (
        ".png",
        "image/png",
    )


def _extract_generated_image_bytes(
    response,
):
    for part in (
        response.parts
        or []
    ):
        inline_data = getattr(
            part,
            "inline_data",
            None,
        )

        if (
            inline_data is None
            or not inline_data.data
        ):
            continue

        data = inline_data.data

        if isinstance(
            data,
            str,
        ):
            try:
                data = (
                    base64.b64decode(
                        data
                    )
                )
            except Exception:
                data = (
                    data.encode(
                        "utf-8"
                    )
                )

        return bytes(data)

    return None


def generate_prompt_image(
    job_id: int,
    prompt_id: int,
):
    api_key, _ = get_api_key()

    if not api_key:
        return {
            "ok": False,
            "code":
                "gemini_not_configured",
            "error":
                "Gemini API key is not configured.",
        }

    package, package_error = (
        _find_verified_package(
            job_id,
            prompt_id,
        )
    )

    if package is None:
        return {
            "ok": False,
            "code":
                "package_invalid",
            "error":
                package_error,
        }

    job = get_job_for_planning(
        job_id
    )

    if job is None:
        return {
            "ok": False,
            "code":
                "job_not_found",
            "error":
                "Job not found.",
        }

    if not job.get(
        "references"
    ):
        return {
            "ok": False,
            "code":
                "no_references",
            "error":
                "This job has no reference images.",
        }

    image_id = (
        _create_image_record(
            job_id,
            prompt_id,
        )
    )

    model = get_image_model()

    try:
        client = (
            create_gemini_client()
        )

        response = (
            client.models.generate_content(
                model=model,

                contents=
                    _build_image_contents(
                        job,
                        package,
                    ),

                config=
                    types.GenerateContentConfig(
                        response_modalities=[
                            "IMAGE"
                        ],

                        image_config=
                            types.ImageConfig(
                                aspect_ratio=
                                    get_image_aspect_ratio(),

                                image_size=
                                    get_image_size(),
                            ),
                    ),
            )
        )

        image_bytes = (
            _extract_generated_image_bytes(
                response
            )
        )

        if not image_bytes:
            raise RuntimeError(
                "Gemini returned no image data."
            )

        extension, _ = (
            _media_type_from_bytes(
                image_bytes
            )
        )

        output_dir = (
            OUTPUTS_DIR /
            f"job_{job_id:06d}"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            output_dir /
            (
                f"prompt_"
                f"{package['position']:02d}_"
                f"image_{image_id:06d}"
                f"{extension}"
            )
        )

        output_path.write_bytes(
            image_bytes
        )

        relative_path = (
            output_path
            .relative_to(
                BASE_DIR
            )
            .as_posix()
        )

        _mark_image_complete(
            image_id,
            relative_path,
        )

        images = get_job_images(
            job_id
        )["images"]

        generated = next(
            (
                item
                for item in images
                if int(item["id"])
                == int(image_id)
            ),
            None,
        )

        return {
            "ok": True,
            "image": generated,
            "package": {
                "prompt_id":
                    package[
                        "prompt_id"
                    ],
                "position":
                    package[
                        "position"
                    ],
                "title":
                    package[
                        "title"
                    ],
                "source_verified":
                    True,
            },
            "model": model,
            "image_size":
                get_image_size(),
            "aspect_ratio":
                get_image_aspect_ratio(),
        }

    except Exception as error:
        safe_message = (
            safe_error_message(
                error,
                api_key,
            )
        )

        _mark_image_failed(
            image_id,
            safe_message,
        )

        return {
            "ok": False,
            "code":
                "image_generation_failed",
            "error":
                safe_message,
            "image_id":
                image_id,
            "model":
                model,
        }

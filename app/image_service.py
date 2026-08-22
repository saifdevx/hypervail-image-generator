import base64
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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
DEFAULT_BATCH_CONCURRENCY = 2
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_BASE_SECONDS = 2.0

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


def get_batch_concurrency():
    raw = os.getenv(
        "IMAGE_BATCH_CONCURRENCY",
        str(DEFAULT_BATCH_CONCURRENCY),
    )

    try:
        value = int(raw)
    except ValueError:
        value = DEFAULT_BATCH_CONCURRENCY

    return max(
        1,
        min(value, 4),
    )


def get_retry_attempts():
    raw = os.getenv(
        "IMAGE_GENERATION_RETRY_ATTEMPTS",
        str(DEFAULT_RETRY_ATTEMPTS),
    )

    try:
        value = int(raw)
    except ValueError:
        value = DEFAULT_RETRY_ATTEMPTS

    return max(
        1,
        min(value, 5),
    )


def get_retry_base_seconds():
    raw = os.getenv(
        "IMAGE_GENERATION_RETRY_BASE_SECONDS",
        str(DEFAULT_RETRY_BASE_SECONDS),
    )

    try:
        value = float(raw)
    except ValueError:
        value = DEFAULT_RETRY_BASE_SECONDS

    return max(
        0.5,
        min(value, 10.0),
    )


def get_image_provider_status():
    api_key, key_source = get_api_key()

    return {
        "provider": "gemini",
        "configured": bool(api_key),
        "model": get_image_model(),
        "image_size": get_image_size(),
        "aspect_ratio": get_image_aspect_ratio(),
        "key_source": key_source,
        "billing_required": True,
        "free_tier_available": False,
        "batch_concurrency": get_batch_concurrency(),
        "retry_attempts": get_retry_attempts(),
    }


def _provider_label():
    return (
        "gemini:"
        f"{get_image_model()}:"
        f"{get_image_size()}:"
        f"{get_image_aspect_ratio()}"
    )


def _create_image_record(
    job_id: int,
    prompt_id: int,
    status: str = "queued",
):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO generated_images (
                job_id,
                prompt_id,
                provider,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                job_id,
                prompt_id,
                _provider_label(),
                status,
            ),
        )

        image_id = cursor.lastrowid
        connection.commit()
        return image_id

    finally:
        connection.close()


def _set_image_status(
    image_id: int,
    status: str,
):
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generated_images
            SET status = ?
            WHERE id = ?
            """,
            (
                status,
                image_id,
            ),
        )
        connection.commit()

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


def _set_job_status(
    job_id: int,
    status: str,
):
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                status,
                job_id,
            ),
        )
        connection.commit()

    finally:
        connection.close()


def _all_image_rows(
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
            ORDER BY gi.id ASC
            """,
            (job_id,),
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()


def _decorate_image_row(
    item: dict,
):
    result = dict(item)

    if (
        result.get("status") == "complete"
        and result.get("file_path")
    ):
        result["file_url"] = (
            f"/api/images/"
            f"{result['id']}/file"
        )
    else:
        result["file_url"] = None

    return result


def get_job_images(
    job_id: int,
):
    rows = _all_image_rows(
        job_id
    )

    return {
        "job_id": job_id,
        "image_count": len(rows),
        "images": [
            _decorate_image_row(row)
            for row in rows
        ],
    }


def _best_row_for_prompt(
    rows: list[dict],
):
    if not rows:
        return None

    # A successful older image is still valid even if a later
    # experimental regeneration failed. Prefer the newest complete
    # image before falling back to the newest attempt.
    complete_rows = [
        row
        for row in rows
        if row.get("status") == "complete"
    ]

    if complete_rows:
        return max(
            complete_rows,
            key=lambda row: int(row["id"]),
        )

    return max(
        rows,
        key=lambda row: int(row["id"]),
    )


def get_image_batch_status(
    job_id: int,
):
    packages = get_prompt_packages(
        job_id
    )

    if packages is None:
        return None

    rows = _all_image_rows(
        job_id
    )

    rows_by_prompt = {}

    for row in rows:
        rows_by_prompt.setdefault(
            int(row["prompt_id"]),
            [],
        ).append(row)

    items = []

    counts = {
        "pending": 0,
        "queued": 0,
        "generating": 0,
        "complete": 0,
        "failed": 0,
    }

    for package in packages.get(
        "packages",
        []
    ):
        prompt_id = int(
            package["prompt_id"]
        )

        row = _best_row_for_prompt(
            rows_by_prompt.get(
                prompt_id,
                [],
            )
        )

        if row is None:
            status = "pending"
            image = None
        else:
            status = row.get(
                "status",
                "pending",
            )
            image = _decorate_image_row(
                row
            )

        if status not in counts:
            status = "pending"

        counts[status] += 1

        items.append(
            {
                "prompt_id": prompt_id,
                "position": package["position"],
                "title": package.get("title") or f"Prompt {package['position']}",
                "status": status,
                "image": image,
            }
        )

    total = len(items)

    if total == 0:
        overall = "no_prompts"
    elif counts["complete"] == total:
        overall = "complete"
    elif (
        counts["queued"]
        or counts["generating"]
    ):
        overall = "generating"
    elif (
        counts["failed"]
        and counts["complete"]
    ):
        overall = "partial_failed"
    elif counts["failed"] == total:
        overall = "failed"
    else:
        overall = "ready"

    return {
        "job_id": job_id,
        "status": overall,
        "source_verified": bool(
            packages.get(
                "source_verified"
            )
        ),
        "total_prompts": total,
        "complete_count": counts["complete"],
        "failed_count": counts["failed"],
        "generating_count": counts["generating"],
        "queued_count": counts["queued"],
        "pending_count": counts["pending"],
        "items": items,
    }


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
            int(package["prompt_id"])
            == int(prompt_id)
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
                mime_type=reference[
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
                data = base64.b64decode(
                    data
                )
            except Exception:
                data = data.encode(
                    "utf-8"
                )

        return bytes(data)

    return None


def _is_retryable_error(
    message: str,
):
    lower = message.lower()

    # Do not repeatedly retry hard billing/free-tier quota failures.
    if (
        "limit: 0" in lower
        or "billing" in lower
        or "free_tier" in lower
    ):
        return False

    return any(
        marker in lower
        for marker in (
            "503",
            "unavailable",
            "high demand",
            "temporarily",
            "timeout",
            "timed out",
            "deadline exceeded",
            "internal error",
            "500 internal",
        )
    )


def _generate_into_record(
    image_id: int,
    job: dict,
    package: dict,
):
    api_key, _ = get_api_key()
    model = get_image_model()

    _set_image_status(
        image_id,
        "generating",
    )

    last_error = None
    attempts = get_retry_attempts()
    base_seconds = get_retry_base_seconds()

    for attempt in range(
        1,
        attempts + 1,
    ):
        try:
            client = create_gemini_client()

            response = (
                client.models.generate_content(
                    model=model,
                    contents=_build_image_contents(
                        job,
                        package,
                    ),
                    config=types.GenerateContentConfig(
                        response_modalities=[
                            "IMAGE"
                        ],
                        image_config=types.ImageConfig(
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
                f"job_{job['id']:06d}"
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

            return {
                "ok": True,
                "image_id": image_id,
                "prompt_id": package[
                    "prompt_id"
                ],
                "position": package[
                    "position"
                ],
                "attempts": attempt,
            }

        except Exception as error:
            safe_message = safe_error_message(
                error,
                api_key,
            )

            last_error = safe_message

            if (
                attempt < attempts
                and _is_retryable_error(
                    safe_message
                )
            ):
                time.sleep(
                    base_seconds
                    * (2 ** (attempt - 1))
                )
                continue

            break

    _mark_image_failed(
        image_id,
        last_error
        or
        "Image generation failed.",
    )

    return {
        "ok": False,
        "image_id": image_id,
        "prompt_id": package[
            "prompt_id"
        ],
        "position": package[
            "position"
        ],
        "error": last_error,
        "attempts": attempts,
    }


def generate_prompt_image(
    job_id: int,
    prompt_id: int,
):
    api_key, _ = get_api_key()

    if not api_key:
        return {
            "ok": False,
            "code": "gemini_not_configured",
            "error": "Gemini API key is not configured.",
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
            "code": "package_invalid",
            "error": package_error,
        }

    job = get_job_for_planning(
        job_id
    )

    if job is None:
        return {
            "ok": False,
            "code": "job_not_found",
            "error": "Job not found.",
        }

    if not job.get(
        "references"
    ):
        return {
            "ok": False,
            "code": "no_references",
            "error": "This job has no reference images.",
        }

    image_id = _create_image_record(
        job_id,
        prompt_id,
        status="queued",
    )

    result = _generate_into_record(
        image_id,
        job,
        package,
    )

    if not result["ok"]:
        return {
            "ok": False,
            "code": "image_generation_failed",
            "error": result.get(
                "error"
            ),
            "image_id": image_id,
            "model": get_image_model(),
        }

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
            "prompt_id": package[
                "prompt_id"
            ],
            "position": package[
                "position"
            ],
            "title": package[
                "title"
            ],
            "source_verified": True,
        },
        "model": get_image_model(),
        "image_size": get_image_size(),
        "aspect_ratio": get_image_aspect_ratio(),
    }


def generate_all_prompt_images(
    job_id: int,
    regenerate_completed: bool = False,
):
    api_key, _ = get_api_key()

    if not api_key:
        return {
            "ok": False,
            "code": "gemini_not_configured",
            "error": "Gemini API key is not configured.",
        }

    packages = get_prompt_packages(
        job_id
    )

    if packages is None:
        return {
            "ok": False,
            "code": "job_not_found",
            "error": "Job not found.",
        }

    if not packages.get(
        "source_verified"
    ):
        return {
            "ok": False,
            "code": "package_invalid",
            "error": (
                "This job does not have source-verified "
                "prompt packages."
            ),
        }

    prompt_packages = packages.get(
        "packages",
        []
    )

    if not prompt_packages:
        return {
            "ok": False,
            "code": "package_invalid",
            "error": "No prompt packages were found.",
        }

    job = get_job_for_planning(
        job_id
    )

    if job is None:
        return {
            "ok": False,
            "code": "job_not_found",
            "error": "Job not found.",
        }

    if not job.get(
        "references"
    ):
        return {
            "ok": False,
            "code": "no_references",
            "error": "This job has no reference images.",
        }

    current_status = get_image_batch_status(
        job_id
    )

    if current_status is not None:
        if (
            current_status["queued_count"]
            or current_status["generating_count"]
        ):
            return {
                "ok": False,
                "code": "batch_in_progress",
                "error": "Image generation is already running for this job.",
                "batch": current_status,
            }

    existing_rows = _all_image_rows(
        job_id
    )

    rows_by_prompt = {}

    for row in existing_rows:
        rows_by_prompt.setdefault(
            int(row["prompt_id"]),
            [],
        ).append(row)

    tasks = []
    skipped = []

    for package in prompt_packages:
        prompt_id = int(
            package["prompt_id"]
        )

        existing_for_prompt = rows_by_prompt.get(
            prompt_id,
            [],
        )

        has_complete = any(
            row.get("status") == "complete"
            for row in existing_for_prompt
        )

        if (
            has_complete
            and not regenerate_completed
        ):
            skipped.append(
                prompt_id
            )
            continue

        image_id = _create_image_record(
            job_id,
            prompt_id,
            status="queued",
        )

        tasks.append(
            (
                image_id,
                package,
            )
        )

    if not tasks:
        summary = get_image_batch_status(
            job_id
        )

        if summary and summary["status"] == "complete":
            _set_job_status(
                job_id,
                "images_complete",
            )

        return {
            "ok": True,
            "status": "nothing_to_generate",
            "skipped_prompt_ids": skipped,
            "batch": summary,
            "results": [],
        }

    _set_job_status(
        job_id,
        "images_generating",
    )

    concurrency = min(
        get_batch_concurrency(),
        len(tasks),
    )

    results = []

    with ThreadPoolExecutor(
        max_workers=concurrency
    ) as executor:
        future_map = {
            executor.submit(
                _generate_into_record,
                image_id,
                job,
                package,
            ): (
                image_id,
                package,
            )
            for image_id, package in tasks
        }

        for future in as_completed(
            future_map
        ):
            try:
                results.append(
                    future.result()
                )
            except Exception as error:
                image_id, package = future_map[
                    future
                ]

                safe_message = safe_error_message(
                    error,
                    api_key,
                )

                _mark_image_failed(
                    image_id,
                    safe_message,
                )

                results.append(
                    {
                        "ok": False,
                        "image_id": image_id,
                        "prompt_id": package[
                            "prompt_id"
                        ],
                        "position": package[
                            "position"
                        ],
                        "error": safe_message,
                    }
                )

    summary = get_image_batch_status(
        job_id
    )

    if summary is not None:
        if summary["status"] == "complete":
            job_status = "images_complete"
        elif summary["status"] == "partial_failed":
            job_status = "images_partial_failed"
        elif summary["status"] == "failed":
            job_status = "images_failed"
        else:
            job_status = "images_ready"

        _set_job_status(
            job_id,
            job_status,
        )

    return {
        "ok": bool(
            summary
            and summary["failed_count"] == 0
        ),
        "status": (
            summary["status"]
            if summary
            else "unknown"
        ),
        "concurrency": concurrency,
        "retry_attempts": get_retry_attempts(),
        "skipped_prompt_ids": skipped,
        "batch": summary,
        "results": sorted(
            results,
            key=lambda item: int(
                item.get("position", 0)
            ),
        ),
    }

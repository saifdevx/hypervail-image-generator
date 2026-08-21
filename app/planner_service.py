from google.genai import types

from app.gemini_service import (
    create_gemini_client,
    get_api_key,
    get_prompt_model,
    safe_error_message,
)

from app.job_store import (
    get_job,
    get_job_for_planning,
    mark_job_planning,
    mark_job_planned,
    mark_job_planning_failed,
)


def build_runtime_instruction(job: dict):
    creative_direction = (
        job.get("description")
        or ""
    ).strip()

    requested_count = (
        job.get("requested_count")
        or "auto"
    ).strip()

    if requested_count == "auto":
        count_instruction = (
            "Output count setting: AUTO. "
            "Use the prompt-count and variation rules "
            "defined by the system instruction."
        )
    else:
        count_instruction = (
            f"Output count setting: {requested_count}. "
            f"The user is requesting {requested_count} outputs. "
            "Apply this as a current user request while still "
            "following the system instruction's own priority "
            "and conflict rules."
        )

    if creative_direction:
        direction_instruction = (
            "Additional user creative direction:\n"
            f"{creative_direction}"
        )
    else:
        direction_instruction = (
            "Additional user creative direction: none."
        )

    return f"""
Generate the image-generation prompt plan now.

The reference images are supplied in exact order and are explicitly
labeled Image 1, Image 2, Image 3, and Image 4 where present.
Preserve that ordering when applying the reference-role rules in
the system instruction.

{count_instruction}

{direction_instruction}

Follow the system instruction as the authoritative creative workflow.
Do not generate images in this step. Generate the prompts, analysis,
QA, or other text that the selected system instruction requires.

Return the response in the output format requested by the system
instruction. Do not convert the response to JSON yet unless the
system instruction itself explicitly requires JSON. Structured JSON
normalization is handled by the next stage of this application.
""".strip()


def build_contents(job: dict):
    contents = []

    for reference in job["references"]:
        contents.append(
            (
                f"Reference Image {reference['position']} "
                f"({reference['original_filename']}):"
            )
        )

        image_bytes = (
            reference["absolute_path"]
            .read_bytes()
        )

        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=reference["media_type"],
            )
        )

    contents.append(
        build_runtime_instruction(job)
    )

    return contents


def plan_job(job_id: int):
    job = get_job_for_planning(job_id)

    if job is None:
        return {
            "ok": False,
            "code": "job_not_found",
            "error": "Job not found.",
        }

    if not job["references"]:
        return {
            "ok": False,
            "code": "no_references",
            "error": "The job has no reference images.",
        }

    api_key, _ = get_api_key()

    if not api_key:
        return {
            "ok": False,
            "code": "gemini_not_configured",
            "error": (
                "Gemini is not configured. "
                "Open Settings and configure the API key."
            ),
        }

    model = get_prompt_model()

    mark_job_planning(
        job_id,
        model,
    )

    try:
        client = create_gemini_client()

        response = client.models.generate_content(
            model=model,
            contents=build_contents(job),
            config=types.GenerateContentConfig(
                system_instruction=(
                    job["system_instruction_snapshot"]
                )
            ),
        )

        raw_output = (
            response.text
            or ""
        ).strip()

        if not raw_output:
            raise RuntimeError(
                "Gemini returned an empty prompt-planning response."
            )

        mark_job_planned(
            job_id,
            model,
            raw_output,
        )

        return {
            "ok": True,
            "job": get_job(job_id),
        }

    except Exception as error:
        safe_message = safe_error_message(
            error,
            api_key,
        )

        mark_job_planning_failed(
            job_id,
            model,
            safe_message,
        )

        return {
            "ok": False,
            "code": "planner_failed",
            "error": safe_message,
            "job": get_job(job_id),
        }

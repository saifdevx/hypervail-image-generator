from google.genai import types

from app.gemini_service import (
    create_gemini_client,
    get_api_key,
    safe_error_message,
)
from app.job_store import (
    get_job,
    get_job_for_planning,
    mark_job_planning,
    mark_job_planned,
    mark_job_planning_failed,
)
from app.normalizer_service import (
    invalidate_structured_prompts,
)
from app.openai_planner_service import (
    run_openai_planner,
    test_openai_planner_connection,
)
from app.settings_store import (
    get_runtime_settings,
)


def build_runtime_instruction(
    job: dict,
):
    creative_direction = (
        job.get(
            "description"
        )
        or
        ""
    ).strip()

    requested_count = (
        job.get(
            "requested_count"
        )
        or
        "auto"
    ).strip()

    aspect_ratio = (
        job.get(
            "aspect_ratio"
        )
        or
        "1:1"
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
            "following the system instruction's priority and "
            "conflict rules."
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

Output aspect ratio: {aspect_ratio}.
Treat this as an explicit user lock for every generated prompt.

{direction_instruction}

Follow the system instruction as the authoritative creative workflow.
Do not generate images in this step. Generate the prompts, analysis,
QA, or other text that the selected system instruction requires.

Return the response in the output format requested by the system
instruction. Do not convert the response to JSON yet unless the
system instruction itself explicitly requires JSON. Structured JSON
normalization is handled by the next local stage of this application.
""".strip()


def _build_gemini_contents(
    job: dict,
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
        build_runtime_instruction(
            job
        )
    )

    return contents


def _run_gemini_planner(
    job: dict,
    model: str | None = None,
):
    settings = (
        get_runtime_settings()
    )

    api_key, _ = get_api_key()

    if not api_key:
        return {
            "ok": False,
            "code":
                "gemini_not_configured",
            "provider":
                "gemini",
            "model":
                settings[
                    "gemini_planner_model"
                ],
            "error":
                (
                    "Gemini is selected as the prompt "
                    "planner but GEMINI_API_KEY is not configured."
                ),
        }

    model = (
        model
        or
        settings[
            "gemini_planner_model"
        ]
    )

    try:
        client = (
            create_gemini_client()
        )

        response = (
            client.models.generate_content(
                model=model,
                contents=
                    _build_gemini_contents(
                        job
                    ),
                config=
                    types.GenerateContentConfig(
                        system_instruction=
                            job[
                                "system_instruction_snapshot"
                            ]
                    ),
            )
        )

        raw_output = (
            response.text
            or
            ""
        ).strip()

        if not raw_output:
            raise RuntimeError(
                "Gemini returned an empty prompt-planning response."
            )

        return {
            "ok": True,
            "provider":
                "gemini",
            "model":
                model,
            "raw_output":
                raw_output,
        }

    except Exception as error:
        return {
            "ok": False,
            "code":
                "planner_failed",
            "provider":
                "gemini",
            "model":
                model,
            "error":
                safe_error_message(
                    error,
                    api_key,
                ),
        }


def get_planner_status():
    settings = (
        get_runtime_settings()
    )

    gemini_key, _ = get_api_key()

    from app.openai_image_service import (
        get_openai_api_key,
    )

    selected = settings[
        "planner_provider"
    ]

    model = (
        settings[
            "gemini_planner_model"
        ]
        if selected
        ==
        "gemini"
        else settings[
            "openai_planner_model"
        ]
    )

    configured = (
        bool(gemini_key)
        if selected
        ==
        "gemini"
        else bool(
            get_openai_api_key()
        )
    )

    return {
        "selected_provider":
            selected,
        "configured":
            configured,
        "model":
            model,
        "providers": {
            "gemini": {
                "configured":
                    bool(
                        gemini_key
                    ),
                "model":
                    settings[
                        "gemini_planner_model"
                    ],
            },
            "openai": {
                "configured":
                    bool(
                        get_openai_api_key()
                    ),
                "model":
                    settings[
                        "openai_planner_model"
                    ],
                "reasoning_effort":
                    settings[
                        "openai_planner_reasoning"
                    ],
            },
        },
    }


def test_selected_planner():
    settings = (
        get_runtime_settings()
    )

    if (
        settings[
            "planner_provider"
        ]
        ==
        "openai"
    ):
        return (
            test_openai_planner_connection()
        )

    api_key, _ = get_api_key()

    if not api_key:
        return {
            "ok": False,
            "provider": "gemini",
            "model":
                settings[
                    "gemini_planner_model"
                ],
            "error":
                "GEMINI_API_KEY is not configured.",
        }

    model = (
        settings[
            "gemini_planner_model"
        ]
    )

    try:
        client = (
            create_gemini_client()
        )

        response = (
            client.models.generate_content(
                model=model,
                contents=(
                    "Reply with exactly: "
                    "IMAGE_AGENT_PLANNER_OK"
                ),
            )
        )

        text = (
            response.text
            or
            ""
        ).strip()

        return {
            "ok":
                "IMAGE_AGENT_PLANNER_OK"
                in text,
            "provider":
                "gemini",
            "model":
                model,
            "response":
                text[:200],
        }

    except Exception as error:
        return {
            "ok": False,
            "provider":
                "gemini",
            "model":
                model,
            "error":
                safe_error_message(
                    error,
                    api_key,
                ),
        }


def plan_job(
    job_id: int,
):
    job = (
        get_job_for_planning(
            job_id
        )
    )

    if job is None:
        return {
            "ok": False,
            "code":
                "job_not_found",
            "error":
                "Job not found.",
        }

    if not job[
        "references"
    ]:
        return {
            "ok": False,
            "code":
                "no_references",
            "error":
                (
                    "The job has no reference images."
                ),
        }

    settings = (
        get_runtime_settings()
    )

    provider = (
        job.get(
            "planner_provider_snapshot"
        )
        or
        settings[
            "planner_provider"
        ]
    )

    # A new creative pass invalidates any old structured package.
    invalidate_structured_prompts(
        job_id
    )

    if provider == "openai":
        preliminary_model = (
            job.get(
                "planner_model_snapshot"
            )
            or
            settings[
                "openai_planner_model"
            ]
        )
    else:
        preliminary_model = (
            job.get(
                "planner_model_snapshot"
            )
            or
            settings[
                "gemini_planner_model"
            ]
        )

    mark_job_planning(
        job_id,
        preliminary_model,
        provider=provider,
    )

    if provider == "openai":
        result = (
            run_openai_planner(
                job,
                build_runtime_instruction(
                    job
                ),
                model=
                    preliminary_model,
                reasoning=
                    (
                        job.get(
                            "planner_reasoning_snapshot"
                        )
                        or
                        settings[
                            "openai_planner_reasoning"
                        ]
                    ),
            )
        )
    else:
        result = (
            _run_gemini_planner(
                job,
                model=
                    preliminary_model,
            )
        )

    if result["ok"]:
        mark_job_planned(
            job_id,
            result[
                "model"
            ],
            result[
                "raw_output"
            ],
            provider=
                result[
                    "provider"
                ],
        )

        return {
            "ok": True,
            "job":
                get_job(
                    job_id
                ),
        }

    mark_job_planning_failed(
        job_id,
        result.get(
            "model",
            preliminary_model,
        ),
        result.get(
            "error",
            "Prompt planning failed.",
        ),
        provider=
            result.get(
                "provider",
                provider,
            ),
    )

    return {
        "ok": False,
        "code":
            result.get(
                "code",
                "planner_failed",
            ),
        "error":
            result.get(
                "error",
                "Prompt planning failed.",
            ),
        "job":
            get_job(
                job_id
            ),
    }

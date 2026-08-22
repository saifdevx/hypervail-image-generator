import base64

from app.openai_image_service import (
    create_openai_client,
    get_openai_api_key,
    safe_openai_error_message,
)
from app.settings_store import (
    get_runtime_settings,
)


def get_openai_planner_model():
    return (
        get_runtime_settings()[
            "openai_planner_model"
        ]
    )


def get_openai_planner_reasoning():
    return (
        get_runtime_settings()[
            "openai_planner_reasoning"
        ]
    )


def _data_url(
    media_type: str,
    data: bytes,
):
    encoded = base64.b64encode(
        data
    ).decode(
        "ascii"
    )

    return (
        f"data:{media_type};base64,"
        f"{encoded}"
    )


def build_openai_content(
    job: dict,
    runtime_instruction: str,
):
    content = []

    for reference in job[
        "references"
    ]:
        content.append(
            {
                "type":
                    "input_text",
                "text":
                    (
                        f"Reference Image "
                        f"{reference['position']} "
                        f"({reference['original_filename']}):"
                    ),
            }
        )

        image_bytes = (
            reference[
                "absolute_path"
            ]
            .read_bytes()
        )

        content.append(
            {
                "type":
                    "input_image",
                "image_url":
                    _data_url(
                        reference[
                            "media_type"
                        ],
                        image_bytes,
                    ),
                # Product-detail fidelity matters more than
                # token-minimization for the planner.
                "detail":
                    "high",
            }
        )

    content.append(
        {
            "type":
                "input_text",
            "text":
                runtime_instruction,
        }
    )

    return content


def run_openai_planner(
    job: dict,
    runtime_instruction: str,
):
    api_key = get_openai_api_key()

    if not api_key:
        return {
            "ok": False,
            "code":
                "openai_not_configured",
            "error":
                (
                    "OpenAI is selected as the prompt "
                    "planner but OPENAI_API_KEY is not configured."
                ),
        }

    model = (
        get_openai_planner_model()
    )

    try:
        client = (
            create_openai_client()
        )

        response = (
            client.responses.create(
                model=model,
                instructions=
                    job[
                        "system_instruction_snapshot"
                    ],
                input=[
                    {
                        "role":
                            "user",
                        "content":
                            build_openai_content(
                                job,
                                runtime_instruction,
                            ),
                    }
                ],
                reasoning={
                    "effort":
                        get_openai_planner_reasoning()
                },
                store=False,
            )
        )

        raw_output = (
            response.output_text
            or
            ""
        ).strip()

        if not raw_output:
            raise RuntimeError(
                "OpenAI returned an empty prompt-planning response."
            )

        return {
            "ok": True,
            "provider":
                "openai",
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
                "openai",
            "model":
                model,
            "error":
                safe_openai_error_message(
                    error
                ),
        }


def test_openai_planner_connection():
    api_key = get_openai_api_key()

    if not api_key:
        return {
            "ok": False,
            "error":
                "OPENAI_API_KEY is not configured.",
        }

    model = (
        get_openai_planner_model()
    )

    try:
        client = (
            create_openai_client()
        )

        response = (
            client.responses.create(
                model=model,
                input=(
                    "Reply with exactly: IMAGE_AGENT_PLANNER_OK"
                ),
                reasoning={
                    "effort":
                        "none"
                },
                store=False,
            )
        )

        text = (
            response.output_text
            or
            ""
        ).strip()

        return {
            "ok":
                "IMAGE_AGENT_PLANNER_OK"
                in text,
            "provider":
                "openai",
            "model":
                model,
            "response":
                text[:200],
        }

    except Exception as error:
        return {
            "ok": False,
            "provider":
                "openai",
            "model":
                model,
            "error":
                safe_openai_error_message(
                    error
                ),
        }

import hashlib
import json
from typing import List

from google.genai import types
from pydantic import BaseModel, Field

from app.database import get_connection
from app.gemini_service import (
    create_gemini_client,
    get_api_key,
    get_prompt_model,
    safe_error_message,
)


class ExtractedPrompt(BaseModel):
    position: int = Field(
        description="1-based prompt order from the raw planner output."
    )
    title: str = Field(
        default="",
        description="Short prompt title copied or minimally derived from the raw output."
    )
    prompt_text: str = Field(
        description=(
            "Exact contiguous substring copied from the raw planner output. "
            "Do not rewrite, paraphrase, shorten, expand, clean, or improve it."
        )
    )
    scene_type: str = Field(
        default="",
        description="Optional scene/type label explicitly available in the raw output."
    )
    angle: str = Field(
        default="",
        description="Optional angle label explicitly available in the raw output."
    )


class StructuredPromptPlan(BaseModel):
    prompts: List[ExtractedPrompt]
    shared_negative: str = Field(
        default="",
        description=(
            "Shared negative block if one exists outside the individual prompts. "
            "Metadata only; it is not automatically appended to prompt_text."
        )
    )
    analysis_summary: str = Field(
        default="",
        description="Optional summary metadata. Not used for image generation."
    )
    qa_notes: List[str] = Field(
        default_factory=list,
        description="Optional QA/checklist metadata."
    )


def _column_exists(connection, table_name: str, column_name: str) -> bool:
    rows = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()
    return any(row["name"] == column_name for row in rows)


def ensure_step8_schema():
    connection = get_connection()

    try:
        columns = {
            "normalizer_model": "TEXT",
            "structured_output_json": "TEXT",
            "normalizer_error": "TEXT",
            "normalized_at": "TEXT",
        }

        for column_name, column_type in columns.items():
            if not _column_exists(
                connection,
                "generation_jobs",
                column_name,
            ):
                connection.execute(
                    f"""
                    ALTER TABLE generation_jobs
                    ADD COLUMN {column_name} {column_type}
                    """
                )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_generated_prompts_job
            ON generated_prompts(job_id)
            """
        )

        connection.commit()

    finally:
        connection.close()


def get_job_for_normalization(job_id: int):
    ensure_step8_schema()
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                status,
                planner_model,
                planner_raw_output,
                planner_error,
                normalizer_model,
                structured_output_json,
                normalizer_error,
                normalized_at
            FROM generation_jobs
            WHERE id = ?
            """,
            (job_id,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def get_structured_prompts(job_id: int):
    ensure_step8_schema()
    connection = get_connection()

    try:
        job = connection.execute(
            """
            SELECT
                id,
                status,
                normalizer_model,
                structured_output_json,
                normalizer_error,
                normalized_at
            FROM generation_jobs
            WHERE id = ?
            """,
            (job_id,),
        ).fetchone()

        if job is None:
            return None

        rows = connection.execute(
            """
            SELECT
                id,
                position,
                title,
                prompt_text,
                metadata_json,
                status,
                created_at
            FROM generated_prompts
            WHERE job_id = ?
            ORDER BY position ASC
            """,
            (job_id,),
        ).fetchall()

        prompts = []

        for row in rows:
            item = dict(row)
            metadata = {}

            if item.get("metadata_json"):
                try:
                    metadata = json.loads(item["metadata_json"])
                except json.JSONDecodeError:
                    metadata = {}

            item["metadata"] = metadata
            item["lossless_verified"] = bool(
                metadata.get("lossless_verified")
            )
            prompts.append(item)

        result = dict(job)
        result["prompts"] = prompts
        result["prompt_count"] = len(prompts)
        return result

    finally:
        connection.close()


def mark_job_normalizing(job_id: int, model: str):
    ensure_step8_schema()
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'normalizing',
                normalizer_model = ?,
                normalizer_error = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (model, job_id),
        )
        connection.commit()

    finally:
        connection.close()


def save_structured_prompts(
    job_id: int,
    model: str,
    structured_json: str,
    prompts: list[dict],
):
    ensure_step8_schema()
    connection = get_connection()

    try:
        connection.execute(
            "DELETE FROM generated_prompts WHERE job_id = ?",
            (job_id,),
        )

        for prompt in prompts:
            connection.execute(
                """
                INSERT INTO generated_prompts (
                    job_id,
                    position,
                    title,
                    prompt_text,
                    metadata_json,
                    status
                )
                VALUES (?, ?, ?, ?, ?, 'ready')
                """,
                (
                    job_id,
                    prompt["position"],
                    prompt["title"],
                    prompt["prompt_text"],
                    prompt["metadata_json"],
                ),
            )

        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'structured',
                normalizer_model = ?,
                structured_output_json = ?,
                normalizer_error = NULL,
                normalized_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (model, structured_json, job_id),
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def mark_job_normalization_failed(
    job_id: int,
    model: str,
    error_message: str,
):
    ensure_step8_schema()
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE generation_jobs
            SET
                status = 'normalization_failed',
                normalizer_model = ?,
                normalizer_error = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (model, error_message[:2000], job_id),
        )
        connection.commit()

    finally:
        connection.close()


def build_normalizer_prompt(raw_output: str) -> str:
    return f"""You are a LOSSLESS EXTRACTION ENGINE, not a prompt writer.

Your only job is to convert the RAW PLANNER OUTPUT below into structured data.

CRITICAL RULES:
1. Do NOT rewrite, improve, shorten, expand, paraphrase, clean up, normalize, or creatively modify any image-generation prompt.
2. For every prompts[].prompt_text field, copy an EXACT CONTIGUOUS SUBSTRING from RAW PLANNER OUTPUT.
3. Preserve all wording, punctuation, capitalization, camera instructions, product details, negative constraints, and prompt content.
4. Do not merge two prompts.
5. Do not split one prompt into multiple prompts.
6. Extract every actual image-generation prompt present in the raw output, in the same order.
7. Exclude section headings, analysis text, QA checklists, and markdown code-fence markers from prompt_text unless those characters genuinely belong to the prompt itself.
8. If the raw output contains a shared negative section outside the individual prompts, copy it into shared_negative. Do NOT automatically append it to prompt_text.
9. title, scene_type, and angle are metadata only. They may be copied or minimally derived, but prompt_text must remain lossless.
10. The application will REJECT the entire result if any prompt_text is not found verbatim inside RAW PLANNER OUTPUT.

RAW PLANNER OUTPUT START
<<<RAW_OUTPUT>>>
{raw_output}
<<<END_RAW_OUTPUT>>>
"""


def normalize_job(job_id: int):
    job = get_job_for_normalization(job_id)

    if job is None:
        return {
            "ok": False,
            "code": "job_not_found",
            "error": "Job not found.",
        }

    raw_output = (
        job.get("planner_raw_output")
        or ""
    ).strip()

    if not raw_output:
        return {
            "ok": False,
            "code": "missing_raw_plan",
            "error": (
                "This job has no raw planner output yet. "
                "Run the Step 7 planner first."
            ),
        }

    api_key, _ = get_api_key()

    if not api_key:
        return {
            "ok": False,
            "code": "gemini_not_configured",
            "error": "Gemini is not configured.",
        }

    model = get_prompt_model()
    mark_job_normalizing(job_id, model)

    try:
        client = create_gemini_client()

        response = client.models.generate_content(
            model=model,
            contents=build_normalizer_prompt(raw_output),
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=StructuredPromptPlan,
            ),
        )

        structured = StructuredPromptPlan.model_validate_json(
            response.text
        )

        if not structured.prompts:
            raise RuntimeError(
                "Normalizer returned zero prompts."
            )

        ordered = sorted(
            structured.prompts,
            key=lambda item: item.position,
        )

        positions = [
            item.position
            for item in ordered
        ]

        expected_positions = list(
            range(1, len(ordered) + 1)
        )

        if positions != expected_positions:
            raise RuntimeError(
                "Prompt positions must be sequential starting at 1. "
                f"Got: {positions}"
            )

        raw_hash = hashlib.sha256(
            raw_output.encode("utf-8")
        ).hexdigest()

        stored_prompts = []

        for item in ordered:
            prompt_text = item.prompt_text

            if not prompt_text:
                raise RuntimeError(
                    f"Prompt {item.position} is empty."
                )

            if prompt_text not in raw_output:
                raise RuntimeError(
                    f"Lossless verification failed for prompt {item.position}. "
                    "The structured prompt was not an exact substring of the "
                    "raw planner output. Nothing was saved, so the original "
                    "prompt quality is preserved."
                )

            metadata = {
                "title": item.title,
                "scene_type": item.scene_type,
                "angle": item.angle,
                "source": "planner_raw_output",
                "source_sha256": raw_hash,
                "lossless_verified": True,
            }

            stored_prompts.append(
                {
                    "position": item.position,
                    "title": item.title,
                    "prompt_text": prompt_text,
                    "metadata_json": json.dumps(
                        metadata,
                        ensure_ascii=False,
                    ),
                }
            )

        structured_payload = structured.model_dump()
        structured_payload["source_sha256"] = raw_hash
        structured_payload["lossless_verified"] = True

        structured_json = json.dumps(
            structured_payload,
            ensure_ascii=False,
            indent=2,
        )

        save_structured_prompts(
            job_id,
            model,
            structured_json,
            stored_prompts,
        )

        return {
            "ok": True,
            "result": get_structured_prompts(job_id),
        }

    except Exception as error:
        safe_message = safe_error_message(
            error,
            api_key,
        )

        mark_job_normalization_failed(
            job_id,
            model,
            safe_message,
        )

        return {
            "ok": False,
            "code": "normalizer_failed",
            "error": safe_message,
            "result": get_structured_prompts(job_id),
        }

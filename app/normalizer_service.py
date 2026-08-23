import hashlib
import json
import re
import time
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


# ============================================================
# NORMALIZER STRATEGY
# ============================================================
#
# Primary path:
#   LOCAL deterministic extraction.
#   No Gemini request, no extra API cost, no 503 dependency.
#
# Fallback path:
#   Gemini structured extraction ONLY if a future profile uses
#   an unfamiliar output format that the local parser cannot
#   identify. The result is still rejected unless every prompt
#   is an exact substring of planner_raw_output.
#
# Image generation NEVER uses scene_type / angle metadata.
# It uses only:
#   exact prompt_text
#   + exact shared_negative (when present)
# ============================================================

LOCAL_NORMALIZER_NAME = "local-lossless-parser-v2"


# ============================================================
# OPTIONAL GEMINI FALLBACK SCHEMA
# ============================================================

class ExtractedPrompt(BaseModel):
    position: int = Field(
        description="1-based prompt order from the raw planner output."
    )

    title: str = Field(
        default="",
        description=(
            "Prompt title copied or minimally derived from the raw output. "
            "Metadata only; never used to generate the image."
        )
    )

    prompt_text: str = Field(
        description=(
            "Exact contiguous substring copied from the raw planner output. "
            "Never rewrite, paraphrase, shorten, expand, or improve it."
        )
    )

    scene_type: str = Field(
        default="",
        description=(
            "Optional scene label explicitly present in the source. "
            "Metadata only."
        )
    )

    angle: str = Field(
        default="",
        description=(
            "Optional angle label explicitly present in the source. "
            "Metadata only."
        )
    )


class StructuredPromptPlan(BaseModel):
    prompts: List[ExtractedPrompt]

    shared_negative: str = Field(
        default="",
        description=(
            "Exact contiguous substring copied from the raw planner output "
            "when a shared negative block exists outside the prompts."
        )
    )

    analysis_summary: str = Field(
        default="",
        description="Metadata only. Never used for image generation."
    )

    qa_notes: List[str] = Field(
        default_factory=list,
        description="Metadata only. Never used for image generation."
    )


# ============================================================
# DATABASE SCHEMA SAFETY
# ============================================================

def _column_exists(
    connection,
    table_name: str,
    column_name: str
) -> bool:
    rows = connection.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    return any(
        row["name"] == column_name
        for row in rows
    )


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


# ============================================================
# DATABASE READ / WRITE
# ============================================================

def get_job_for_normalization(
    job_id: int
):
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


def get_structured_prompts(
    job_id: int
):
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

            if item.get(
                "metadata_json"
            ):
                try:
                    metadata = json.loads(
                        item["metadata_json"]
                    )
                except json.JSONDecodeError:
                    metadata = {}

            item["metadata"] = metadata

            item["lossless_verified"] = bool(
                metadata.get(
                    "lossless_verified"
                )
            )

            prompts.append(
                item
            )

        result = dict(job)
        result["prompts"] = prompts
        result["prompt_count"] = len(
            prompts
        )

        return result

    finally:
        connection.close()


def mark_job_normalizing(
    job_id: int,
    model: str
):
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
            (
                model,
                job_id
            ),
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
            """
            DELETE FROM generated_prompts
            WHERE job_id = ?
            """,
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
            (
                model,
                structured_json,
                job_id
            ),
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
            (
                model,
                error_message[:2000],
                job_id
            ),
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# LOCAL LOSSLESS PARSER
# ============================================================

# Supports:
#   PROMPT 1 — TITLE
#   **PROMPT 1 — TITLE**
#   ### PROMPT 1 — TITLE
#   ### **PROMPT 1 — TITLE**
#   Prompt 1: Title
#   - Prompt 1: Title
#   > Prompt 1: Title
#   FINAL PROMPT 1 - Title
#   IMAGE PROMPT 1: Title
#
# Step 13's universal workflow instructions can cause planners
# to use richer Markdown headings.  v2 accepts those headings
# while still preserving prompt text losslessly.

MARKDOWN_PREFIX = r"""
    [ \t]*
    (?:\#{1,6}[ \t]+)?
    (?:>[ \t]*)?
    (?:[-*+][ \t]+)?
    (?:\*\*)?
    [ \t]*
"""


PROMPT_HEADING_RE = re.compile(
    rf"""
    ^
    {MARKDOWN_PREFIX}
    (?:(?:FINAL|IMAGE)[ \t]+)?
    PROMPT
    [ \t]+
    (?P<number>\d+)
    [ \t]*
    (?:
        (?:—|–|-|:)
        [ \t]*
        (?P<title>.*?)
    )?
    [ \t]*
    (?:\*\*)?
    [ \t]*$
    """,
    re.IGNORECASE
    | re.MULTILINE
    | re.VERBOSE,
)


FINAL_PROMPTS_HEADING_RE = re.compile(
    rf"""
    ^
    {MARKDOWN_PREFIX}
    (?:\d+[.)][ \t]*)?
    FINAL
    [ \t]+
    PROMPTS?
    [ \t]*
    (?:\*\*)?
    [ \t]*$
    """,
    re.IGNORECASE
    | re.MULTILINE
    | re.VERBOSE,
)


SHARED_NEGATIVE_HEADING_RE = re.compile(
    rf"""
    ^
    {MARKDOWN_PREFIX}
    (?:\d+[.)][ \t]*)?
    (?:
        UNIVERSAL[ \t]+NEGATIVE(?:[ \t]+CONSTRAINTS)?
        |
        SHARED[ \t]+NEGATIVE(?:[ \t]+CONSTRAINTS)?
        |
        NEGATIVE[ \t]+CONSTRAINTS
        |
        UNIVERSAL[ \t]+NEGATIVE[ \t]+LINE
        |
        NEGATIVE[ \t]+LINE
    )
    [ \t]*
    (?:\*\*)?
    [ \t]*$
    """,
    re.IGNORECASE
    | re.MULTILINE
    | re.VERBOSE,
)


TAIL_SECTION_HEADING_RE = re.compile(
    rf"""
    ^
    {MARKDOWN_PREFIX}
    (?:\d+[.)][ \t]*)?
    (?:
        UNIVERSAL[ \t]+NEGATIVE(?:[ \t]+CONSTRAINTS)?
        |
        SHARED[ \t]+NEGATIVE(?:[ \t]+CONSTRAINTS)?
        |
        NEGATIVE[ \t]+CONSTRAINTS
        |
        UNIVERSAL[ \t]+NEGATIVE[ \t]+LINE
        |
        NEGATIVE[ \t]+LINE
        |
        REGEN[ \t]+FIX[ \t]+LIBRARY
        |
        FINAL[ \t]+QA[ \t]+CHECKLIST
        |
        QA[ \t]+CHECKLIST
        |
        FINAL[ \t]+QUESTION
    )
    [ \t]*
    (?:\*\*)?
    [ \t]*$
    """,
    re.IGNORECASE
    | re.MULTILINE
    | re.VERBOSE,
)


CODE_FENCE_RE = re.compile(
    r"""
    ```(?:text|txt|prompt)?
    [ \t]*\r?\n
    (?P<body>.*?)
    \r?\n```
    """,
    re.IGNORECASE
    | re.DOTALL
    | re.VERBOSE,
)


SEPARATOR_RE = re.compile(
    r"(?m)^[ \t]*---[ \t]*$"
)


def _clean_heading_title(
    number: int,
    raw_title: str | None
) -> str:
    title = (
        raw_title
        or ""
    ).strip()

    title = re.sub(
        r"\*+$",
        "",
        title
    ).strip()

    if title:
        return (
            f"PROMPT {number} — {title}"
        )

    return (
        f"PROMPT {number}"
    )


def _extract_explicit_field(
    block: str,
    field_name: str
) -> str:
    match = re.search(
        rf"""
        ^[ \t]*
        (?:[-*][ \t]*)?
        {re.escape(field_name)}
        [ \t]*:
        [ \t]*
        (?P<value>.+?)
        [ \t]*$
        """,
        block,
        re.IGNORECASE
        | re.MULTILINE
        | re.VERBOSE,
    )

    if not match:
        return ""

    return match.group(
        "value"
    ).strip()


def _extract_prompt_text_from_block(
    block: str
) -> str:
    # UGC-style profiles often provide metadata lines followed
    # by a ```text ... ``` block. In that case the fenced body
    # is the actual paste-ready image prompt.
    fence = CODE_FENCE_RE.search(
        block
    )

    if fence:
        return fence.group(
            "body"
        ).strip()

    # Hero-style profiles place the prompt directly under the
    # PROMPT N heading. Remove only a trailing markdown section
    # separator; do not rewrite any prompt wording.
    prompt_text = (
        block
        .strip()
    )

    prompt_text = re.sub(
        r"\n[ \t]*---[ \t]*$",
        "",
        prompt_text
    ).strip()

    return prompt_text


def _get_final_prompt_search_region(
    raw_output: str
) -> tuple[str, int]:
    """
    Prefer parsing only inside the planner's FINAL PROMPTS section.

    This prevents lines from SHORT ANALYSIS / Angle Plan such as
    "Prompt 2: side angle" from being mistaken for a real final prompt.

    Returns:
        (region_text, region_start_offset)
    """
    section = (
        FINAL_PROMPTS_HEADING_RE.search(
            raw_output
        )
    )

    if not section:
        return (
            raw_output,
            0,
        )

    start = section.end()

    tail = (
        TAIL_SECTION_HEADING_RE.search(
            raw_output,
            start,
        )
    )

    end = (
        tail.start()
        if tail
        else
        len(
            raw_output
        )
    )

    return (
        raw_output[
            start:end
        ],
        start,
    )


def _extract_local_prompts(
    raw_output: str
) -> list[dict]:
    (
        search_region,
        region_offset,
    ) = (
        _get_final_prompt_search_region(
            raw_output
        )
    )

    matches = list(
        PROMPT_HEADING_RE.finditer(
            search_region
        )
    )

    if not matches:
        return []

    prompts = []

    for index, match in enumerate(
        matches
    ):
        number = int(
            match.group(
                "number"
            )
        )

        # Work with absolute source indexes so every extracted
        # string remains an exact slice of planner_raw_output.
        start = (
            region_offset
            +
            match.end()
        )

        if (
            index + 1
            <
            len(matches)
        ):
            end = (
                region_offset
                +
                matches[
                    index + 1
                ].start()
            )

        else:
            if region_offset:
                # When a FINAL PROMPTS section was isolated,
                # its region already ends before negative / QA.
                end = (
                    region_offset
                    +
                    len(
                        search_region
                    )
                )

            else:
                tail_match = (
                    TAIL_SECTION_HEADING_RE.search(
                        raw_output,
                        start
                    )
                )

                end = (
                    tail_match.start()
                    if tail_match
                    else
                    len(
                        raw_output
                    )
                )

        block = raw_output[
            start:end
        ].strip()

        prompt_text = (
            _extract_prompt_text_from_block(
                block
            )
        )

        if not prompt_text:
            continue

        # Hard source guarantee.
        if prompt_text not in raw_output:
            raise RuntimeError(
                f"Local lossless verification failed for prompt {number}."
            )

        title = _clean_heading_title(
            number,
            match.group(
                "title"
            )
        )

        scene_type = (
            _extract_explicit_field(
                block,
                "Scene Type"
            )
            or
            _extract_explicit_field(
                block,
                "Mode"
            )
        )

        angle = (
            _extract_explicit_field(
                block,
                "Angle"
            )
        )

        prompts.append(
            {
                "position":
                    number,
                "title":
                    title,
                "prompt_text":
                    prompt_text,
                "scene_type":
                    scene_type,
                "angle":
                    angle,
            }
        )

    prompts.sort(
        key=lambda item:
            item["position"]
    )

    positions = [
        item["position"]
        for item in prompts
    ]

    # Duplicate prompt IDs are never safe.
    if (
        len(
            positions
        )
        !=
        len(
            set(
                positions
            )
        )
    ):
        return []

    expected = list(
        range(
            1,
            len(
                prompts
            )
            +
            1
        )
    )

    # v1 raised here immediately.  v2 returns zero prompts instead,
    # which safely activates the existing structured-extraction
    # fallback instead of failing the user's job with a 502.
    if positions != expected:
        return []

    return prompts


def _extract_shared_negative(
    raw_output: str
) -> str:
    match = (
        SHARED_NEGATIVE_HEADING_RE.search(
            raw_output
        )
    )

    if not match:
        return ""

    start = match.end()

    separator = (
        SEPARATOR_RE.search(
            raw_output,
            start
        )
    )

    next_tail = (
        TAIL_SECTION_HEADING_RE.search(
            raw_output,
            start
        )
    )

    candidates = [
        candidate
        for candidate in (
            separator.start()
            if separator
            else None,

            next_tail.start()
            if next_tail
            else None,

            len(raw_output),
        )
        if candidate is not None
        and candidate >= start
    ]

    end = min(
        candidates
    )

    shared_negative = (
        raw_output[
            start:end
        ]
        .strip()
    )

    if (
        shared_negative
        and
        shared_negative
        not in raw_output
    ):
        raise RuntimeError(
            "Local shared-negative verification failed."
        )

    return shared_negative


def _build_verified_payload(
    raw_output: str,
    extracted_prompts: list[dict],
    shared_negative: str,
    normalizer_name: str
) -> tuple[str, list[dict]]:
    if not extracted_prompts:
        raise RuntimeError(
            "Normalizer returned zero prompts."
        )

    raw_hash = hashlib.sha256(
        raw_output.encode(
            "utf-8"
        )
    ).hexdigest()

    stored_prompts = []

    for item in extracted_prompts:
        prompt_text = (
            item[
                "prompt_text"
            ]
        )

        if (
            not prompt_text
            or prompt_text
            not in raw_output
        ):
            raise RuntimeError(
                f"Lossless verification failed for prompt "
                f"{item['position']}. Nothing was saved."
            )

        metadata = {
            "title":
                item.get(
                    "title",
                    ""
                ),

            "scene_type":
                item.get(
                    "scene_type",
                    ""
                ),

            "angle":
                item.get(
                    "angle",
                    ""
                ),

            "source":
                "planner_raw_output",

            "source_sha256":
                raw_hash,

            "lossless_verified":
                True,

            "normalizer":
                normalizer_name,
        }

        stored_prompts.append(
            {
                "position":
                    item["position"],

                "title":
                    item.get(
                        "title",
                        ""
                    ),

                "prompt_text":
                    prompt_text,

                "metadata_json":
                    json.dumps(
                        metadata,
                        ensure_ascii=False,
                    ),
            }
        )

    if (
        shared_negative
        and shared_negative
        not in raw_output
    ):
        raise RuntimeError(
            "Lossless verification failed for shared negative constraints."
        )

    payload = {
        "prompts": [
            {
                "position":
                    item["position"],

                "title":
                    item.get(
                        "title",
                        ""
                    ),

                "prompt_text":
                    item["prompt_text"],

                "scene_type":
                    item.get(
                        "scene_type",
                        ""
                    ),

                "angle":
                    item.get(
                        "angle",
                        ""
                    ),
            }
            for item in extracted_prompts
        ],

        "shared_negative":
            shared_negative,

        # Metadata intentionally left empty rather than generated
        # or summarized. It is not needed for image generation.
        "analysis_summary":
            "",

        "qa_notes":
            [],

        "source_sha256":
            raw_hash,

        "lossless_verified":
            True,

        "shared_negative_lossless_verified":
            (
                True
                if shared_negative
                else None
            ),

        "normalizer":
            normalizer_name,
    }

    structured_json = (
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        )
    )

    return (
        structured_json,
        stored_prompts
    )


# ============================================================
# GEMINI FALLBACK — ONLY FOR UNKNOWN FUTURE FORMATS
# ============================================================

def build_normalizer_prompt(
    raw_output: str
) -> str:
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
8. If the raw output contains a shared negative section outside the individual prompts, shared_negative must be an EXACT CONTIGUOUS SUBSTRING copied from RAW PLANNER OUTPUT.
9. title, scene_type, and angle are metadata only and are NEVER used to generate the image.
10. The application rejects the entire result if any prompt_text is not found verbatim inside RAW PLANNER OUTPUT.

RAW PLANNER OUTPUT START
<<<RAW_OUTPUT>>>
{raw_output}
<<<END_RAW_OUTPUT>>>
"""


def _is_retryable_gemini_error(
    message: str
) -> bool:
    lower = message.lower()

    return any(
        marker in lower
        for marker in (
            "503",
            "unavailable",
            "high demand",
            "resource exhausted",
            "429",
            "temporarily",
        )
    )


def _gemini_fallback_extract(
    raw_output: str
) -> tuple[
    list[dict],
    str,
    str
]:
    api_key, _ = get_api_key()

    if not api_key:
        raise RuntimeError(
            "Local parser could not identify this profile format, "
            "and Gemini fallback is not configured."
        )

    model = get_prompt_model()
    client = create_gemini_client()

    last_error = None

    # Rare fallback only. A few short retries handle temporary
    # high-demand responses without slowing the normal local path.
    for attempt in range(1, 4):
        try:
            response = (
                client.models.generate_content(
                    model=model,

                    contents=
                        build_normalizer_prompt(
                            raw_output
                        ),

                    config=
                        types.GenerateContentConfig(
                            temperature=0,
                            response_mime_type=
                                "application/json",
                            response_schema=
                                StructuredPromptPlan,
                        ),
                )
            )

            structured = (
                StructuredPromptPlan
                .model_validate_json(
                    response.text
                )
            )

            prompts = [
                {
                    "position":
                        item.position,

                    "title":
                        item.title,

                    "prompt_text":
                        item.prompt_text,

                    "scene_type":
                        item.scene_type,

                    "angle":
                        item.angle,
                }
                for item in sorted(
                    structured.prompts,
                    key=lambda value:
                        value.position
                )
            ]

            shared_negative = (
                structured.shared_negative
                or ""
            ).strip()

            return (
                prompts,
                shared_negative,
                f"{model}-fallback"
            )

        except Exception as error:
            last_error = error

            safe_message = (
                safe_error_message(
                    error,
                    api_key
                )
            )

            if (
                attempt >= 3
                or not _is_retryable_gemini_error(
                    safe_message
                )
            ):
                raise

            time.sleep(
                1.5 * attempt
            )

    raise last_error


# ============================================================
# NORMALIZE JOB
# ============================================================

def normalize_job(
    job_id: int
):
    job = get_job_for_normalization(
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

    raw_output = (
        job.get(
            "planner_raw_output"
        )
        or
        ""
    ).strip()

    if not raw_output:
        return {
            "ok": False,
            "code":
                "missing_raw_plan",
            "error":
                (
                    "This job has no raw planner output yet. "
                    "Run the planner first."
                ),
        }

    normalizer_name = (
        LOCAL_NORMALIZER_NAME
    )

    mark_job_normalizing(
        job_id,
        normalizer_name
    )

    try:
        # ----------------------------------------------------
        # 1. FAST LOCAL LOSSLESS PARSER
        # ----------------------------------------------------
        prompts = (
            _extract_local_prompts(
                raw_output
            )
        )

        shared_negative = (
            _extract_shared_negative(
                raw_output
            )
        )

        # ----------------------------------------------------
        # 2. FALLBACK ONLY FOR UNFAMILIAR FUTURE FORMATS
        # ----------------------------------------------------
        if not prompts:
            (
                prompts,
                shared_negative,
                normalizer_name
            ) = _gemini_fallback_extract(
                raw_output
            )

        # ----------------------------------------------------
        # 3. HARD PYTHON SOURCE VERIFICATION
        # ----------------------------------------------------
        (
            structured_json,
            stored_prompts
        ) = _build_verified_payload(
            raw_output=
                raw_output,

            extracted_prompts=
                prompts,

            shared_negative=
                shared_negative,

            normalizer_name=
                normalizer_name,
        )

        save_structured_prompts(
            job_id=
                job_id,

            model=
                normalizer_name,

            structured_json=
                structured_json,

            prompts=
                stored_prompts,
        )

        return {
            "ok": True,
            "result":
                get_structured_prompts(
                    job_id
                ),
        }

    except Exception as error:
        api_key, _ = get_api_key()

        safe_message = (
            safe_error_message(
                error,
                api_key
            )
        )

        mark_job_normalization_failed(
            job_id=
                job_id,

            model=
                normalizer_name,

            error_message=
                safe_message,
        )

        return {
            "ok": False,
            "code":
                "normalizer_failed",
            "error":
                safe_message,
            "result":
                get_structured_prompts(
                    job_id
                ),
        }


# ============================================================
# INVALIDATE STRUCTURED DATA WHEN RAW PLAN CHANGES
# ============================================================

def invalidate_structured_prompts(
    job_id: int
):
    ensure_step8_schema()
    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM generated_prompts
            WHERE job_id = ?
            """,
            (job_id,),
        )

        connection.execute(
            """
            UPDATE generation_jobs

            SET
                structured_output_json = NULL,
                normalizer_model = NULL,
                normalizer_error = NULL,
                normalized_at = NULL

            WHERE id = ?
            """,
            (job_id,),
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# SOURCE-VERIFIED STEP 9 PACKAGES
# ============================================================

def get_prompt_packages(
    job_id: int
):
    ensure_step8_schema()
    connection = get_connection()

    try:
        job = connection.execute(
            """
            SELECT
                id,
                status,
                planner_raw_output,
                structured_output_json,
                normalizer_model,
                normalizer_error,
                normalized_at

            FROM generation_jobs

            WHERE id = ?
            """,
            (job_id,),
        ).fetchone()

        if job is None:
            return None

        raw_output = (
            job[
                "planner_raw_output"
            ]
            or
            ""
        )

        structured_json = (
            job[
                "structured_output_json"
            ]
            or
            ""
        )

        result = {
            "id":
                job_id,

            "status":
                job["status"],

            "normalizer_model":
                job["normalizer_model"],

            "normalizer_error":
                job["normalizer_error"],

            "normalized_at":
                job["normalized_at"],

            "source_verified":
                False,

            "shared_negative":
                "",

            "shared_negative_lossless_verified":
                None,

            "package_count":
                0,

            "packages":
                [],
        }

        if (
            not raw_output
            or not structured_json
        ):
            return result

        try:
            payload = json.loads(
                structured_json
            )
        except json.JSONDecodeError:
            result["status"] = (
                "structured_invalid"
            )
            return result

        raw_hash = hashlib.sha256(
            raw_output.encode(
                "utf-8"
            )
        ).hexdigest()

        if (
            payload.get(
                "source_sha256"
            )
            !=
            raw_hash
        ):
            result["status"] = (
                "structured_stale"
            )
            return result

        shared_negative = (
            payload.get(
                "shared_negative"
            )
            or
            ""
        ).strip()

        if (
            shared_negative
            and shared_negative
            not in raw_output
        ):
            result["status"] = (
                "structured_invalid"
            )
            return result

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

        packages = []

        for row in rows:
            metadata = {}

            if row[
                "metadata_json"
            ]:
                try:
                    metadata = json.loads(
                        row[
                            "metadata_json"
                        ]
                    )
                except json.JSONDecodeError:
                    metadata = {}

            prompt_text = (
                row[
                    "prompt_text"
                ]
            )

            prompt_verified = (
                bool(
                    metadata.get(
                        "lossless_verified"
                    )
                )
                and
                metadata.get(
                    "source_sha256"
                )
                ==
                raw_hash
                and
                prompt_text
                in
                raw_output
            )

            if not prompt_verified:
                result["status"] = (
                    "structured_invalid"
                )
                return result

            final_input = (
                prompt_text
            )

            shared_negative_applied = (
                False
            )

            if (
                shared_negative
                and shared_negative
                not in prompt_text
            ):
                final_input = (
                    f"{prompt_text}\n\n"
                    f"Avoid:\n"
                    f"{shared_negative}"
                )

                shared_negative_applied = (
                    True
                )

            packages.append(
                {
                    "prompt_id":
                        row["id"],

                    "position":
                        row["position"],

                    "title":
                        row["title"],

                    "positive_prompt_text":
                        prompt_text,

                    "positive_lossless_verified":
                        True,

                    "shared_negative_text":
                        shared_negative,

                    "shared_negative_lossless_verified":
                        (
                            True
                            if shared_negative
                            else None
                        ),

                    "shared_negative_applied":
                        shared_negative_applied,

                    "final_input":
                        final_input,

                    "final_input_strategy":
                        (
                            "positive_exact + deterministic Avoid label + shared_negative_exact"
                            if shared_negative_applied
                            else
                            "positive_exact"
                        ),

                    "source_sha256":
                        raw_hash,
                }
            )

        result["source_verified"] = (
            True
        )

        result["shared_negative"] = (
            shared_negative
        )

        result[
            "shared_negative_lossless_verified"
        ] = (
            True
            if shared_negative
            else None
        )

        result["packages"] = (
            packages
        )

        result["package_count"] = (
            len(packages)
        )

        return result

    finally:
        connection.close()

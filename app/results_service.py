import io
import json
import re
import zipfile

from app.database import get_connection
from app.image_service import (
    get_generated_image_file,
    get_image_batch_status,
)
from app.job_store import get_job
from app.normalizer_service import get_prompt_packages


def _slug(
    value: str,
):
    value = (
        value
        .strip()
        .lower()
    )

    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value,
    )

    return (
        value.strip("-")
        or
        "image"
    )


def get_download_name(
    image_id: int,
):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                gi.id,
                gi.job_id,
                gp.position,
                gp.title
            FROM generated_images gi
            LEFT JOIN generated_prompts gp
                ON gp.id = gi.prompt_id
            WHERE gi.id = ?
            """,
            (image_id,)
        ).fetchone()

        if row is None:
            return None

        title = (
            row["title"]
            or
            f"prompt-{row['position'] or 1}"
        )

        return (
            f"{int(row['position'] or 1):02d}-"
            f"{_slug(title)}.jpg"
        )

    finally:
        connection.close()


def build_job_zip(
    job_id: int,
):
    job = get_job(
        job_id
    )

    if job is None:
        return None

    batch = (
        get_image_batch_status(
            job_id
        )
    )

    if batch is None:
        return None

    memory = io.BytesIO()

    packages = (
        get_prompt_packages(
            job_id
        )
        or
        {}
    )

    prompt_lookup = {
        int(
            item["prompt_id"]
        ):
            item
        for item in packages.get(
            "packages",
            []
        )
    }

    with zipfile.ZipFile(
        memory,
        mode="w",
        compression=
            zipfile.ZIP_DEFLATED,
    ) as archive:
        prompt_export = []

        for item in batch.get(
            "items",
            []
        ):
            image = (
                item.get(
                    "image"
                )
                or
                {}
            )

            if (
                item.get(
                    "status"
                )
                !=
                "complete"
                or
                not image.get(
                    "id"
                )
            ):
                continue

            generated = (
                get_generated_image_file(
                    int(
                        image["id"]
                    )
                )
            )

            if generated is None:
                continue

            suffix = (
                generated[
                    "path"
                ].suffix.lower()
                or
                ".jpg"
            )

            filename = (
                f"{int(item['position']):02d}-"
                f"{_slug(item['title'])}"
                f"{suffix}"
            )

            archive.writestr(
                filename,
                generated[
                    "path"
                ].read_bytes(),
            )

            package = (
                prompt_lookup.get(
                    int(
                        item[
                            "prompt_id"
                        ]
                    )
                )
            )

            if package:
                prompt_export.append(
                    {
                        "position":
                            item[
                                "position"
                            ],
                        "title":
                            item[
                                "title"
                            ],
                        "prompt_id":
                            item[
                                "prompt_id"
                            ],
                        "final_input":
                            package.get(
                                "final_input"
                            ),
                    }
                )

        archive.writestr(
            "prompts.json",
            json.dumps(
                {
                    "job_id":
                        job_id,
                    "profile":
                        job.get(
                            "profile_name"
                        ),
                    "planner_provider":
                        job.get(
                            "planner_provider"
                        ),
                    "planner_model":
                        job.get(
                            "planner_model"
                        ),
                    "prompts":
                        prompt_export,
                },
                ensure_ascii=False,
                indent=2,
            ),
        )

    memory.seek(0)

    zip_name = (
        f"job-{job_id:04d}-"
        f"{_slug(job.get('profile_name') or 'images')}"
        f".zip"
    )

    return {
        "bytes":
            memory.getvalue(),
        "filename":
            zip_name,
    }

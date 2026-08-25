import os
from pathlib import Path
from typing import Protocol


class StorageBackend(Protocol):
    name: str

    def job_upload_dir(
        self,
        job_id: int,
    ) -> Path:
        ...

    def job_output_dir(
        self,
        job_id: int,
    ) -> Path:
        ...


class LocalStorageBackend:
    name = "local"

    def __init__(
        self,
        base_dir: Path,
    ):
        self.base_dir = (
            base_dir
        )

        self.data_dir = (
            base_dir
            /
            "data"
        )

        self.uploads_dir = (
            self.data_dir
            /
            "uploads"
        )

        self.outputs_dir = (
            self.data_dir
            /
            "outputs"
        )

    def ensure(self):
        self.uploads_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.outputs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def job_upload_dir(
        self,
        job_id: int,
    ):
        self.ensure()

        return (
            self.uploads_dir
            /
            f"job_{job_id:06d}"
        )

    def job_output_dir(
        self,
        job_id: int,
    ):
        self.ensure()

        return (
            self.outputs_dir
            /
            f"job_{job_id:06d}"
        )


class R2StorageBackend:
    """
    Phase 2 adapter target.

    Keeping the interface here means generation/business logic does
    not need to know whether files live locally or in Cloudflare R2.
    """

    name = "r2"

    def job_upload_dir(
        self,
        job_id: int,
    ):
        raise RuntimeError(
            "Cloudflare R2 storage becomes active in "
            "Hyperex Step 14 Phase 2."
        )

    def job_output_dir(
        self,
        job_id: int,
    ):
        raise RuntimeError(
            "Cloudflare R2 storage becomes active in "
            "Hyperex Step 14 Phase 2."
        )


def get_storage_backend(
    base_dir: Path,
):
    provider = (
        os.getenv(
            "STORAGE_PROVIDER",
            "local",
        )
        or
        "local"
    ).strip().lower()

    if provider == "r2":
        return R2StorageBackend()

    return LocalStorageBackend(
        base_dir
    )

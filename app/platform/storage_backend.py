import os
import mimetypes
from pathlib import Path
from typing import Protocol


R2_PREFIX = "r2://"


class StorageBackend(Protocol):
    name: str

    def write_reference(self, owner_id, job_id, filename, data, media_type):
        ...

    def write_output(self, owner_id, job_id, filename, data, media_type):
        ...

    def read_bytes(self, storage_ref: str) -> bytes:
        ...

    def delete(self, storage_ref: str) -> bool:
        ...

    def signed_get_url(self, storage_ref: str, download_name: str | None = None):
        ...


class LocalStorageBackend:
    name = "local"

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.data_dir = base_dir / "data"
        self.uploads_dir = self.data_dir / "uploads"
        self.outputs_dir = self.data_dir / "outputs"

    def ensure(self):
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

    def job_upload_dir(self, job_id: int):
        self.ensure()
        return self.uploads_dir / f"job_{job_id:06d}"

    def job_output_dir(self, job_id: int):
        self.ensure()
        return self.outputs_dir / f"job_{job_id:06d}"

    def _safe_path(self, storage_ref: str):
        path = (self.base_dir / storage_ref).resolve()
        data_root = self.data_dir.resolve()
        if path != data_root and data_root not in path.parents:
            raise RuntimeError("Storage path escaped Hyperex data directory.")
        return path

    def write_reference(self, owner_id, job_id, filename, data, media_type):
        directory = self.job_upload_dir(job_id)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / filename
        path.write_bytes(data)
        return path.relative_to(self.base_dir).as_posix()

    def write_output(self, owner_id, job_id, filename, data, media_type):
        directory = self.job_output_dir(job_id)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / filename
        path.write_bytes(data)
        return path.relative_to(self.base_dir).as_posix()

    def read_bytes(self, storage_ref: str):
        return self._safe_path(storage_ref).read_bytes()

    def exists(self, storage_ref: str):
        try:
            return self._safe_path(storage_ref).exists()
        except Exception:
            return False

    def delete(self, storage_ref: str):
        try:
            path = self._safe_path(storage_ref)
            if not path.exists():
                return False
            path.unlink()
            return True
        except Exception:
            return False

    def local_path(self, storage_ref: str):
        path = self._safe_path(storage_ref)
        return path if path.exists() else None

    def signed_get_url(self, storage_ref: str, download_name: str | None = None):
        return None

    def delete_job_objects(self, owner_id: str, job_id: int):
        import shutil
        shutil.rmtree(self.job_upload_dir(job_id), ignore_errors=True)
        shutil.rmtree(self.job_output_dir(job_id), ignore_errors=True)


class R2StorageBackend:
    name = "r2"

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        # Keep compatibility properties for maintenance code; these are temp/local only.
        self.data_dir = base_dir / "data"
        self.uploads_dir = self.data_dir / "uploads"
        self.outputs_dir = self.data_dir / "outputs"

        self.account_id = (os.getenv("R2_ACCOUNT_ID") or "").strip()
        self.access_key = (os.getenv("R2_ACCESS_KEY_ID") or "").strip()
        self.secret_key = (os.getenv("R2_SECRET_ACCESS_KEY") or "").strip()
        self.bucket = (os.getenv("R2_BUCKET") or "").strip()

        if not all([
            self.account_id,
            self.access_key,
            self.secret_key,
            self.bucket,
        ]):
            raise RuntimeError(
                "STORAGE_PROVIDER=r2 requires R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, "
                "R2_SECRET_ACCESS_KEY and R2_BUCKET."
            )

        try:
            import boto3
        except ImportError as error:
            raise RuntimeError(
                "R2 is selected but boto3 is not installed. Run: pip install boto3"
            ) from error

        self._client = boto3.client(
            service_name="s3",
            endpoint_url=f"https://{self.account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name="auto",
        )

    @staticmethod
    def _clean_owner(owner_id: str):
        return "".join(ch for ch in owner_id if ch.isalnum() or ch in "-_" )[:120] or "user"

    def _key(self, owner_id: str, job_id: int, kind: str, filename: str):
        owner = self._clean_owner(owner_id)
        return f"users/{owner}/jobs/{job_id:06d}/{kind}/{filename}"

    def _ref(self, key: str):
        return f"{R2_PREFIX}{key}"

    def _parse(self, storage_ref: str):
        if not storage_ref.startswith(R2_PREFIX):
            raise ValueError("Not an R2 storage reference.")
        key = storage_ref[len(R2_PREFIX):]
        if not key or ".." in key.split("/"):
            raise ValueError("Invalid R2 object key.")
        return key

    def _put(self, key, data, media_type):
        self._client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            ContentType=media_type or "application/octet-stream",
            CacheControl="private, max-age=300",
        )
        return self._ref(key)

    def write_reference(self, owner_id, job_id, filename, data, media_type):
        return self._put(
            self._key(owner_id, job_id, "references", filename),
            data,
            media_type,
        )

    def write_output(self, owner_id, job_id, filename, data, media_type):
        return self._put(
            self._key(owner_id, job_id, "outputs", filename),
            data,
            media_type,
        )

    def read_bytes(self, storage_ref: str):
        response = self._client.get_object(
            Bucket=self.bucket,
            Key=self._parse(storage_ref),
        )
        return response["Body"].read()

    def exists(self, storage_ref: str):
        try:
            self._client.head_object(Bucket=self.bucket, Key=self._parse(storage_ref))
            return True
        except Exception:
            return False

    def delete(self, storage_ref: str):
        try:
            self._client.delete_object(Bucket=self.bucket, Key=self._parse(storage_ref))
            return True
        except Exception:
            return False

    def local_path(self, storage_ref: str):
        return None

    def signed_get_url(self, storage_ref: str, download_name: str | None = None):
        params = {
            "Bucket": self.bucket,
            "Key": self._parse(storage_ref),
        }
        if download_name:
            params["ResponseContentDisposition"] = f'attachment; filename="{download_name}"'

        return self._client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=900,
        )

    def delete_job_objects(self, owner_id: str, job_id: int):
        prefix = f"users/{self._clean_owner(owner_id)}/jobs/{job_id:06d}/"
        continuation = None
        while True:
            kwargs = {"Bucket": self.bucket, "Prefix": prefix}
            if continuation:
                kwargs["ContinuationToken"] = continuation
            response = self._client.list_objects_v2(**kwargs)
            objects = response.get("Contents", [])
            if objects:
                self._client.delete_objects(
                    Bucket=self.bucket,
                    Delete={"Objects": [{"Key": item["Key"]} for item in objects]},
                )
            if not response.get("IsTruncated"):
                break
            continuation = response.get("NextContinuationToken")


def get_storage_provider():
    provider = (os.getenv("STORAGE_PROVIDER", "local") or "local").strip().lower()
    return provider if provider in {"local", "r2"} else "local"


def storage_is_configured():
    if get_storage_provider() == "local":
        return True
    return all((os.getenv(key) or "").strip() for key in [
        "R2_ACCOUNT_ID",
        "R2_ACCESS_KEY_ID",
        "R2_SECRET_ACCESS_KEY",
        "R2_BUCKET",
    ])


def get_storage_backend(base_dir: Path):
    if get_storage_provider() == "r2":
        return R2StorageBackend(base_dir)
    return LocalStorageBackend(base_dir)


def media_type_for_filename(filename: str):
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"

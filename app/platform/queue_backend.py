import os
from typing import Callable, Protocol

import httpx


class GenerationQueueBackend(Protocol):
    name: str
    asynchronous: bool

    def dispatch(self, task: dict, local_callable: Callable | None = None):
        ...


class LocalGenerationQueue:
    name = "local"
    asynchronous = False

    def dispatch(self, task: dict, local_callable: Callable | None = None):
        if local_callable is None:
            raise RuntimeError("Local queue dispatch requires a callable.")
        return {
            "queued": False,
            "result": local_callable(),
        }


class CloudflareQueueBackend:
    name = "cloudflare"
    asynchronous = True

    def __init__(self):
        self.account_id = (os.getenv("CLOUDFLARE_ACCOUNT_ID") or "").strip()
        self.queue_id = (os.getenv("CLOUDFLARE_QUEUE_ID") or "").strip()
        self.api_token = (os.getenv("CLOUDFLARE_QUEUE_API_TOKEN") or "").strip()

        if not all([self.account_id, self.queue_id, self.api_token]):
            raise RuntimeError(
                "QUEUE_PROVIDER=cloudflare requires CLOUDFLARE_ACCOUNT_ID, "
                "CLOUDFLARE_QUEUE_ID and CLOUDFLARE_QUEUE_API_TOKEN."
            )

    def dispatch(self, task: dict, local_callable: Callable | None = None):
        url = (
            f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}"
            f"/queues/{self.queue_id}/messages"
        )

        response = httpx.post(
            url,
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            },
            json={"body": task},
            timeout=20.0,
        )

        if response.status_code >= 400:
            raise RuntimeError(
                f"Cloudflare Queue publish failed ({response.status_code}): "
                f"{response.text[:500]}"
            )

        payload = response.json()
        if not payload.get("success"):
            raise RuntimeError("Cloudflare Queue rejected the generation task.")

        return {
            "queued": True,
            "task": task,
        }


def get_queue_provider():
    provider = (os.getenv("QUEUE_PROVIDER", "local") or "local").strip().lower()
    return provider if provider in {"local", "cloudflare"} else "local"


def queue_is_configured():
    if get_queue_provider() == "local":
        return True
    return all((os.getenv(key) or "").strip() for key in [
        "CLOUDFLARE_ACCOUNT_ID",
        "CLOUDFLARE_QUEUE_ID",
        "CLOUDFLARE_QUEUE_API_TOKEN",
        "HYPEREX_QUEUE_SHARED_SECRET",
    ])


def get_generation_queue():
    if get_queue_provider() == "cloudflare":
        return CloudflareQueueBackend()
    return LocalGenerationQueue()

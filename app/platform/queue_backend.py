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
    """
    Render cannot publish directly to a Cloudflare Queue binding.

    Cloudflare Queues are published through a small producer Worker. Render
    sends the task to that authenticated Worker endpoint; the Worker writes the
    task to the Queue, and the Queue consumer later calls Hyperex's protected
    internal consume endpoint.
    """

    name = "cloudflare"
    asynchronous = True

    def __init__(self):
        self.producer_url = (
            os.getenv("CLOUDFLARE_QUEUE_PRODUCER_URL")
            or
            ""
        ).strip().rstrip("/")

        self.shared_secret = (
            os.getenv("HYPEREX_QUEUE_SHARED_SECRET")
            or
            ""
        ).strip()

        if not self.producer_url or not self.shared_secret:
            raise RuntimeError(
                "QUEUE_PROVIDER=cloudflare requires "
                "CLOUDFLARE_QUEUE_PRODUCER_URL and "
                "HYPEREX_QUEUE_SHARED_SECRET."
            )

    def dispatch(self, task: dict, local_callable: Callable | None = None):
        try:
            response = httpx.post(
                self.producer_url,
                headers={
                    "X-Hyperex-Queue-Secret": self.shared_secret,
                    "Content-Type": "application/json",
                },
                json=task,
                timeout=httpx.Timeout(
                    15.0,
                    connect=5.0,
                ),
            )
        except httpx.RequestError as error:
            raise RuntimeError(
                "Could not reach the Hyperex Cloudflare Queue producer."
            ) from error

        if response.status_code < 200 or response.status_code >= 300:
            raise RuntimeError(
                "Cloudflare Queue producer rejected the task "
                f"({response.status_code}): {response.text[:500]}"
            )

        try:
            payload = response.json()
        except ValueError as error:
            raise RuntimeError(
                "Cloudflare Queue producer returned an invalid response."
            ) from error

        if not payload.get("queued"):
            raise RuntimeError(
                "Cloudflare Queue producer did not confirm the task was queued."
            )

        return {
            "queued": True,
            "task": task,
            "producer": self.producer_url,
        }


def get_queue_provider():
    provider = (
        os.getenv(
            "QUEUE_PROVIDER",
            "local",
        )
        or
        "local"
    ).strip().lower()

    return (
        provider
        if provider in {
            "local",
            "cloudflare",
        }
        else
        "local"
    )


def queue_is_configured():
    if get_queue_provider() == "local":
        return True

    return all(
        (
            os.getenv(key)
            or
            ""
        ).strip()
        for key in [
            "CLOUDFLARE_QUEUE_PRODUCER_URL",
            "HYPEREX_QUEUE_SHARED_SECRET",
        ]
    )


def get_generation_queue():
    if get_queue_provider() == "cloudflare":
        return CloudflareQueueBackend()

    return LocalGenerationQueue()

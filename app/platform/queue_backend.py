import os
from typing import Callable, Protocol


class GenerationQueueBackend(
    Protocol
):
    name: str

    def run(
        self,
        function: Callable,
        *args,
        **kwargs,
    ):
        ...


class LocalGenerationQueue:
    name = "local"

    def run(
        self,
        function: Callable,
        *args,
        **kwargs,
    ):
        return function(
            *args,
            **kwargs,
        )


class CloudflareQueueBackend:
    name = "cloudflare"

    def run(
        self,
        function: Callable,
        *args,
        **kwargs,
    ):
        raise RuntimeError(
            "Cloudflare Queues become active in "
            "Hyperex Step 14 Phase 2."
        )


def get_generation_queue():
    provider = (
        os.getenv(
            "QUEUE_PROVIDER",
            "local",
        )
        or
        "local"
    ).strip().lower()

    if provider == "cloudflare":
        return CloudflareQueueBackend()

    return LocalGenerationQueue()

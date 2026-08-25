from typing import Protocol


class PlannerProviderAdapter(
    Protocol
):
    provider_id: str

    def plan(
        self,
        job: dict,
    ) -> dict:
        ...


class ImageProviderAdapter(
    Protocol
):
    provider_id: str

    def generate(
        self,
        job: dict,
        package: dict,
    ) -> bytes:
        ...


# Existing OpenAI and Gemini services already satisfy the provider
# boundary conceptually. Phase 1 formalizes the interface; Phase 2 can
# add more providers without changing jobs/history/model-registry tables.

const ALLOWED_TASKS = new Set([
    "generate_all",
    "generate_one",
    "regenerate_one",
]);

function jsonResponse(payload, status = 200) {
    return new Response(
        JSON.stringify(payload),
        {
            status,
            headers: {
                "content-type": "application/json; charset=utf-8",
                "cache-control": "no-store",
            },
        },
    );
}

function cleanRenderUrl(value) {
    return String(value || "").trim().replace(/\/+$/, "");
}

function validateTask(task) {
    if (!task || typeof task !== "object" || Array.isArray(task)) {
        return "Request body must be a queue task object.";
    }

    if (!task.task_id || typeof task.task_id !== "string") {
        return "task_id is required.";
    }

    if (!ALLOWED_TASKS.has(String(task.task || ""))) {
        return "Unsupported task type.";
    }

    if (!Number.isInteger(Number(task.job_id)) || Number(task.job_id) < 1) {
        return "job_id must be a positive integer.";
    }

    if (!task.user_id || typeof task.user_id !== "string") {
        return "user_id is required.";
    }

    if (
        task.task !== "generate_all"
        &&
        (!Number.isInteger(Number(task.prompt_id)) || Number(task.prompt_id) < 1)
    ) {
        return "prompt_id is required for single-image tasks.";
    }

    return null;
}

function retryDelay(attempts) {
    const n = Math.max(1, Number(attempts || 1));
    return Math.min(60, 5 * (2 ** (n - 1)));
}

export default {
    async fetch(request, env) {
        const url = new URL(request.url);

        if (request.method === "GET" && url.pathname === "/health") {
            return jsonResponse({
                ok: true,
                service: "hyperex-queue-worker",
            });
        }

        if (request.method !== "POST" || url.pathname !== "/enqueue") {
            return jsonResponse(
                {
                    ok: false,
                    error: "Not found.",
                },
                404,
            );
        }

        const expected = String(
            env.HYPEREX_QUEUE_SHARED_SECRET || "",
        ).trim();

        const supplied = String(
            request.headers.get("X-Hyperex-Queue-Secret") || "",
        ).trim();

        if (!expected) {
            return jsonResponse(
                {
                    ok: false,
                    error: "Worker queue secret is not configured.",
                },
                503,
            );
        }

        if (!supplied || supplied !== expected) {
            return jsonResponse(
                {
                    ok: false,
                    error: "Unauthorized.",
                },
                401,
            );
        }

        let task;

        try {
            task = await request.json();
        } catch {
            return jsonResponse(
                {
                    ok: false,
                    error: "Invalid JSON body.",
                },
                400,
            );
        }

        const validationError = validateTask(task);

        if (validationError) {
            return jsonResponse(
                {
                    ok: false,
                    error: validationError,
                },
                422,
            );
        }

        await env.GENERATION_QUEUE.send(task);

        return jsonResponse(
            {
                ok: true,
                queued: true,
                task_id: task.task_id,
            },
            202,
        );
    },

    async queue(batch, env) {
        const renderUrl = cleanRenderUrl(
            env.HYPEREX_RENDER_URL,
        );

        const secret = String(
            env.HYPEREX_QUEUE_SHARED_SECRET || "",
        ).trim();

        if (!renderUrl || !secret) {
            for (const message of batch.messages) {
                message.retry({ delaySeconds: 60 });
            }
            return;
        }

        for (const message of batch.messages) {
            try {
                const response = await fetch(
                    `${renderUrl}/api/internal/queue/consume`,
                    {
                        method: "POST",
                        headers: {
                            "content-type": "application/json",
                            "X-Hyperex-Queue-Secret": secret,
                            "X-Hyperex-Queue-Attempt": String(
                                message.attempts || 1,
                            ),
                        },
                        body: JSON.stringify(message.body),
                    },
                );

                if (response.ok) {
                    message.ack();
                    continue;
                }

                // A second delivery can arrive while an earlier attempt is
                // still running. Retry it; once the first attempt finishes,
                // Hyperex's task-id guard will acknowledge the duplicate.
                if (response.status === 409) {
                    message.retry({
                        delaySeconds: retryDelay(message.attempts),
                    });
                    continue;
                }

                // Authentication/configuration or Render/server failures can
                // become healthy without changing the queue message.
                if (
                    response.status === 401
                    || response.status === 403
                    || response.status >= 500
                ) {
                    message.retry({
                        delaySeconds: retryDelay(message.attempts),
                    });
                    continue;
                }

                // 404/422 and other client errors are permanent for this task.
                // Hyperex has already recorded the task failure where possible.
                message.ack();

            } catch (error) {
                console.error(
                    "Hyperex queue delivery failed",
                    message.id,
                    error,
                );

                message.retry({
                    delaySeconds: retryDelay(message.attempts),
                });
            }
        }
    },
};

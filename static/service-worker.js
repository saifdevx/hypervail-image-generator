const CACHE_NAME = "hyperex-shell-v14";

const SHELL = [
    "/",
    "/static/styles.css",
    "/static/app.js",
    "/static/manifest.webmanifest",
    "/static/icons/hyperex-logo.png",
    "/static/icons/favicon-32.png",
    "/static/icons/icon-192.png",
    "/static/icons/icon-512.png",
];

self.addEventListener(
    "install",
    event => {
        event.waitUntil(
            caches
                .open(
                    CACHE_NAME
                )
                .then(
                    cache =>
                        cache.addAll(
                            SHELL
                        )
                )
        );

        self.skipWaiting();
    }
);

self.addEventListener(
    "activate",
    event => {
        event.waitUntil(
            caches
                .keys()
                .then(
                    keys =>
                        Promise.all(
                            keys
                                .filter(
                                    key =>
                                        key
                                        !==
                                        CACHE_NAME
                                )
                                .map(
                                    key =>
                                        caches.delete(
                                            key
                                        )
                                )
                        )
                )
        );

        self.clients.claim();
    }
);

self.addEventListener(
    "fetch",
    event => {
        const request =
            event.request;

        const url =
            new URL(
                request.url
            );

        if (
            request.method
            !==
            "GET"
            ||
            url.origin
            !==
            self.location.origin
        ) {
            return;
        }

        // Never cache API calls or generated image responses.
        if (
            url.pathname.startsWith(
                "/api/"
            )
        ) {
            return;
        }

        event.respondWith(
            fetch(
                request
            )
            .then(
                response => {
                    const copy =
                        response.clone();

                    caches
                        .open(
                            CACHE_NAME
                        )
                        .then(
                            cache =>
                                cache.put(
                                    request,
                                    copy
                                )
                        );

                    return response;
                }
            )
            .catch(
                () =>
                    caches.match(
                        request
                    )
            )
        );
    }
);

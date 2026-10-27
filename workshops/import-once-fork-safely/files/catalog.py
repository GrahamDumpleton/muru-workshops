"""A catalogue service that counts its requests with the metrics client."""

import os

import metrics

# Open the socket to the metrics agent and start the thread that sends
# the counts, as soon as this module is imported.
metrics.client.start()


def application(environ, start_response):
    metrics.client.increment()

    body = f"The catalogue, served by worker process {os.getpid()}.\n".encode()

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]

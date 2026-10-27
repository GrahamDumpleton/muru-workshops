"""Version 3 of the greeter, which has a bug: one request in five fails.

Every response names the release that served it, from muru.context(),
and the worker process that ran it.
"""

import os
import random

import muru

GREETING = "Good evening"


def application(environ, start_response):
    release = muru.context().release

    if random.random() < 0.2:
        status = "500 Internal Server Error"
        body = f"Something broke. Served by release {release}, worker {os.getpid()}.\n"

    else:
        status = "200 OK"
        body = f"{GREETING}. Served by release {release}, worker {os.getpid()}.\n"

    body = body.encode()

    start_response(
        status,
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]

"""Version 1 of the greeter, a WSGI application deployed to the Muru daemon.

Every response names the release that served it, from muru.context(),
and the worker process that ran it.
"""

import os

import muru

GREETING = "Hello"


def application(environ, start_response):
    release = muru.context().release
    body = f"{GREETING}. Served by release {release}, worker {os.getpid()}.\n".encode()

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]

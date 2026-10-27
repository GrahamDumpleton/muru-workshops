"""A WSGI application of one function, to serve under muructl run.

Every response says which process served it, so you can see the
workers Muru runs. Two paths fail on purpose: /boom raises an
exception, and /crash ends the worker process outright.
"""

import os


def application(environ, start_response):
    path = environ["PATH_INFO"]

    if path == "/boom":
        raise RuntimeError("the application failed, on purpose")

    if path == "/crash":
        os._exit(1)

    body = (
        "Hello from Muru.\n"
        "\n"
        f"Served by worker process {os.getpid()}, "
        f"forked from host process {os.getppid()}.\n"
        f"Request {environ['muru.request_id']} for "
        f"{environ['REQUEST_METHOD']} {path}\n"
    ).encode()

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]

"""A WSGI application that says how it was reached.

The first line of every response carries the greeting and the process
id of the host the worker was forked from, which changes with each
release. The second says whether the request came over HTTP or HTTPS,
which version of HTTP it used, and the TLS details when there are any.
"""

import os

GREETING = "Hello"


def application(environ, start_response):
    tls = environ.get("muru.tls")

    connection = (
        f"Scheme {environ['wsgi.url_scheme']}, protocol {environ['SERVER_PROTOCOL']}"
    )

    if tls:
        connection += f", {tls['version']}, ALPN {tls['alpn']}"

    body = (
        f"{GREETING}, from the release whose host is process {os.getppid()}.\n"
        f"{connection}.\n"
    ).encode()

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]

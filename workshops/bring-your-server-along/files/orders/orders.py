"""An orders service: an ordinary WSGI application, deployed today with

    gunicorn --workers 2 --bind 127.0.0.1:8000 orders:application

Every response says which server ran it, from SERVER_SOFTWARE, and
which process.
"""

import os


def application(environ, start_response):
    server = environ["SERVER_SOFTWARE"]
    body = f"Orders. Served by {server}, process {os.getpid()}.\n".encode()

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]

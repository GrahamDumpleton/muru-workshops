"""A WSGI application with two kinds of work.

/wait spends a tenth of a second waiting, as a view does while a
database or another service answers. /compute spends a tenth of a
second of CPU time running Python, as a view does that renders,
parses or calculates.
"""

import time


def wait():
    time.sleep(0.1)
    return b"Waited for 0.1s.\n"


def compute():
    start = time.thread_time()

    while time.thread_time() - start < 0.1:
        sum(range(1000))

    return b"Computed for 0.1s of CPU time.\n"


def application(environ, start_response):
    path = environ["PATH_INFO"]

    if path == "/wait":
        body = wait()

    elif path == "/compute":
        body = compute()

    else:
        body = b"Try /wait or /compute.\n"

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]

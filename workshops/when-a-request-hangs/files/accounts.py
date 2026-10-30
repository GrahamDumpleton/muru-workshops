"""An accounts service with three ways for a request to hang.

/report waits for a file that never appears, in Python code that the
soft timeout can interrupt. /sync retries an upstream that always
refuses, in a loop whose bare except also catches the soft timeout's
exception. /check validates a user name with a regular expression that,
on some inputs, backtracks for longer than anyone will wait, inside the
re module's C code, which holds the GIL and cannot be interrupted.
"""

import re
import time
from pathlib import Path
from urllib.parse import parse_qs

# One or more runs of letters: the nested + makes the matcher try every
# way of splitting a long name that ends in something other than a letter.
USER_NAME = re.compile(r"^([a-z]+)+$")

REPORT_READY = Path("report.ready")


def fetch_upstream():
    time.sleep(0.5)
    raise ConnectionError("the upstream did not answer")


def application(environ, start_response):
    path = environ["PATH_INFO"]
    status = "200 OK"

    if path == "/health":
        body = "ok\n"
    elif path == "/report":
        while not REPORT_READY.exists():
            time.sleep(0.1)
        body = "the report is ready\n"
    elif path == "/sync":
        # Retry until the upstream answers. The bare except catches
        # everything, the soft timeout's muru.RequestTimeout included.
        while True:
            try:
                fetch_upstream()
                break
            except:  # noqa: E722
                pass
        body = "synchronised\n"
    elif path == "/check":
        name = parse_qs(environ.get("QUERY_STRING", "")).get("name", [""])[0]
        valid = USER_NAME.match(name) is not None
        body = f"{name!r} is {'a valid' if valid else 'not a valid'} user name\n"
    elif path == "/export":
        time.sleep(1.5)
        body = "exported\n"
    else:
        status = "404 Not Found"
        body = "not found\n"

    start_response(status, [("Content-Type", "text/plain")])
    return [body.encode()]

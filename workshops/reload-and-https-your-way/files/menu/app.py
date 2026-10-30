"""The menu of the day, from a template and a data file.

Each request records when it came in data/last-visit.json, and /slow
takes three seconds to answer.
"""

import json
import os
import time
from pathlib import Path

HERE = Path(__file__).parent

TEMPLATE = (HERE / "templates" / "page.html").read_text()
MENU = json.loads((HERE / "data" / "menu.json").read_text())


def application(environ, start_response):
    if environ["PATH_INFO"] == "/slow":
        time.sleep(3)

    (HERE / "data" / "last-visit.json").write_text(json.dumps({"time": time.time()}))

    body = TEMPLATE.format(
        items=", ".join(MENU),
        pid=os.getpid(),
        scheme=environ["wsgi.url_scheme"],
        protocol=environ["SERVER_PROTOCOL"],
    )
    start_response("200 OK", [("Content-Type", "text/html")])
    return [body.encode()]

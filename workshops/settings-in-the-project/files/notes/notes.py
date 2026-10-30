"""A small WSGI application that says how it is being served.

The title comes from the NOTES_TITLE environment variable, and the rest
from the worker answering: its index and process id.
"""

import json
import os

import muru


def application(environ, start_response):
    context = muru.context()
    body = json.dumps(
        {
            "title": os.environ.get("NOTES_TITLE", "(not set)"),
            "worker": context.worker_id,
            "worker process": os.getpid(),
        }
    )
    start_response("200 OK", [("Content-Type", "application/json")])
    return [body.encode()]

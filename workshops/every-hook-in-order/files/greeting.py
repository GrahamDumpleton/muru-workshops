"""A WSGI application that says which worker process answered."""

import os

GREETING = "Hello"


def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [f"{GREETING} from worker process {os.getpid()}\n".encode()]

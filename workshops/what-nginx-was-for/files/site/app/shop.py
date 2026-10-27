"""The shop's application, served by Muru workers behind the edge.

/ answers with the catalogue as JSON, which the edge compresses. /report
hands the edge a file to send in its place, with X-Muru-Sendfile. Any
other path is the application's own 404.
"""

import json
import os

REPORTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")


def catalogue(start_response):
    products = [
        {"id": number, "name": f"product {number}", "description": "A fine thing to own. " * 3}
        for number in range(1, 41)
    ]
    body = json.dumps(products, indent=1).encode()

    start_response(
        "200 OK",
        [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]


def report(start_response):
    # The application decides whether the client may have the report,
    # then names the file for the edge to send. The body is empty: the
    # edge replaces it with the file.
    start_response(
        "200 OK",
        [
            ("Content-Type", "text/csv; charset=utf-8"),
            ("X-Muru-Sendfile", os.path.join(REPORTS, "sales.csv")),
        ],
    )

    return [b""]


def application(environ, start_response):
    path = environ["PATH_INFO"]

    if path == "/":
        return catalogue(start_response)

    if path == "/report":
        return report(start_response)

    body = b"No such page.\n"

    start_response(
        "404 Not Found",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
        ],
    )

    return [body]

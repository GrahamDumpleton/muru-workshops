"""Send a mix of requests to the shop and count the answers.

Usage: python send_requests.py PORT [ROUNDS]

Each round asks for the home page, the three products, a product that
does not exist, a page that does not exist and the slow report, one
after another. The last line counts the responses by status.
"""

import collections
import sys
import urllib.error
import urllib.request

PATHS = [
    "/",
    "/products/1",
    "/products/2",
    "/products/3",
    "/products/9",
    "/nothing",
    "/report",
]


def fetch(url: str) -> int:
    """Return the status of a GET, whatever it is."""

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            response.read()
            return response.status

    except urllib.error.HTTPError as error:
        error.read()
        return error.code


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: python send_requests.py PORT [ROUNDS]")
        return 2

    port = sys.argv[1]
    rounds = int(sys.argv[2]) if len(sys.argv) == 3 else 1
    statuses = collections.Counter()

    for _ in range(rounds):
        for path in PATHS:
            statuses[fetch(f"http://127.0.0.1:{port}{path}")] += 1

    total = sum(statuses.values())
    counts = ", ".join(
        f"{count} x {status}" for status, count in sorted(statuses.items())
    )

    print(f"{total} requests: {counts}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

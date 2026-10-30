"""Send a morning's mix of requests and print the status of each.

Usage: python mixed.py PORT
"""

import sys
import urllib.error
import urllib.request

PATHS = ["/health"] * 5 + ["/check?name=ada", "/export", "/missing", "/health"]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python mixed.py PORT")
        return 2

    for path in PATHS:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}{path}", timeout=30) as response:
                status = response.status
        except urllib.error.HTTPError as error:
            status = error.code

        print(f"{status} {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

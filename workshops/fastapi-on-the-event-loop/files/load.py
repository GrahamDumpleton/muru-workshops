"""Send many requests to one path at once and say how long they took.

Usage: python load.py PORT PATH COUNT
"""

import concurrent.futures
import sys
import time
import urllib.request


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: python load.py PORT PATH COUNT")
        return 2

    port, path, count = sys.argv[1], sys.argv[2], int(sys.argv[3])

    def get(_):
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=60) as response:
            response.read()

    start = time.monotonic()

    with concurrent.futures.ThreadPoolExecutor(count) as pool:
        list(pool.map(get, range(count)))

    print(f"{count} requests to {path} at once took {time.monotonic() - start:.2f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())

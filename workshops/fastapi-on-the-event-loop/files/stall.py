"""Ask for /stall, and a second later for /where/async, and report both.

Usage: python stall.py PORT
"""

import concurrent.futures
import sys
import time
import urllib.error
import urllib.request


def get(port, path, delay):
    time.sleep(delay)
    start = time.monotonic()

    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=60) as response:
            status = response.status
    except urllib.error.HTTPError as error:
        status = error.code

    return f"{path}: {status} after {time.monotonic() - start:.1f} s"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python stall.py PORT")
        return 2

    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        stalled = pool.submit(get, sys.argv[1], "/stall", 0)
        innocent = pool.submit(get, sys.argv[1], "/where/async", 1)

        print(stalled.result())
        print(innocent.result())

    return 0


if __name__ == "__main__":
    sys.exit(main())

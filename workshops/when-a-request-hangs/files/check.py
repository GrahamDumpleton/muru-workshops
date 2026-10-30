"""Ask /check about a long user name, and a second later ask /health.

Usage: python check.py PORT
"""

import concurrent.futures
import sys
import time
import urllib.error
import urllib.request

NAME = "a" * 34 + "!"


def get(port, path, delay):
    time.sleep(delay)
    start = time.monotonic()

    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=120) as response:
            status = response.status
    except urllib.error.HTTPError as error:
        status = error.code

    return f"{path.split('?')[0]}: {status} after {time.monotonic() - start:.1f} s"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python check.py PORT")
        return 2

    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        check = pool.submit(get, sys.argv[1], f"/check?name={NAME}", 0)
        health = pool.submit(get, sys.argv[1], "/health", 1)

        print(check.result())
        print(health.result())

    return 0


if __name__ == "__main__":
    sys.exit(main())

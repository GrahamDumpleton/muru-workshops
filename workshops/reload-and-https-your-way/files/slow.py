"""Ask for /slow, which takes three seconds, and print the answer.

Usage: python slow.py PORT
"""

import sys
import time
import urllib.request


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python slow.py PORT")
        return 2

    start = time.monotonic()

    with urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/slow", timeout=30) as response:
        body = response.read().decode()
        status = response.status

    print(f"/slow answered {status} after {time.monotonic() - start:.1f} s:")
    print(body, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())

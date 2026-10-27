"""Ask for a page ten times a second until what it says changes.

Usage: python watch.py PORT

Prints the first line of the page when it starts and again each time
it changes, with the seconds since it started. One second after the
first change, or after two minutes with none, it stops and prints how
many requests it sent and how many failed. The summary also goes to
watch.log.
"""

import sys
import time
import urllib.error
import urllib.request

LIMIT = 120.0


def first_line(url: str) -> str | None:
    """Return the first line of the page, or None when the request fails."""

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.read().decode().splitlines()[0]

    except (urllib.error.URLError, OSError):
        return None


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python watch.py PORT")
        return 2

    url = f"http://127.0.0.1:{sys.argv[1]}/"
    start = time.monotonic()
    stop_at = start + LIMIT
    sent = failed = 0
    last = None

    while time.monotonic() < stop_at:
        line = first_line(url)
        sent += 1
        elapsed = time.monotonic() - start

        if line is None:
            failed += 1
            print(f"{elapsed:5.1f}s  request failed")

        elif line != last:
            print(f"{elapsed:5.1f}s  {line}")

            if last is not None:
                stop_at = min(stop_at, time.monotonic() + 1.0)

            last = line

        time.sleep(0.1)

    summary = f"{sent} requests in {time.monotonic() - start:.1f}s, {failed} failed"

    print(summary)

    with open("watch.log", "w") as log:
        log.write(summary + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

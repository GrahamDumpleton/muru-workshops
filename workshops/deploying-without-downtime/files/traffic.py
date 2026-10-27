"""Send a steady stream of requests and count the answers by who served them.

Usage: python traffic.py PORT

Four clients ask for the page over and over, without cookies, so the
edge sees every request as a new client. Every two seconds a line
counts the answers in that time by what the page says served it (the
text after "Served by", up to a comma), with errors, a 4xx or 5xx
status, beside each, and the requests that got no answer at all. Stop
it with Ctrl-C, which prints the totals and writes them to
traffic.log.
"""

import collections
import re
import sys
import threading
import time
import urllib.error
import urllib.request

CLIENTS = 4
INTERVAL = 2.0
SERVED_BY = re.compile(r"Served by ([^,\n]+)")

lock = threading.Lock()
answers = collections.Counter()
errors = collections.Counter()
unanswered = 0


def client(url: str, stop: threading.Event) -> None:
    """Ask for the page until told to stop, counting what comes back."""

    global unanswered

    while not stop.is_set():
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                body, status = response.read().decode(), response.status

        except urllib.error.HTTPError as error:
            body, status = error.read().decode(errors="replace"), error.code

        except OSError:
            with lock:
                unanswered += 1

            time.sleep(0.1)
            continue

        match = SERVED_BY.search(body)
        server = match.group(1) if match else f"the edge ({status})"

        with lock:
            answers[server] += 1

            if status >= 400:
                errors[server] += 1

        time.sleep(0.02)


def describe(counts, error_counts, no_answer) -> str:
    parts = []

    for server in sorted(counts):
        part = f"{server}: {counts[server]}"

        if error_counts[server]:
            part += f" ({error_counts[server]} errors)"

        parts.append(part)

    parts.append(f"no answer: {no_answer}")

    return "   ".join(parts)


def main() -> int:
    global unanswered

    if len(sys.argv) != 2:
        print("Usage: python traffic.py PORT")
        return 2

    url = f"http://127.0.0.1:{sys.argv[1]}/"
    stop = threading.Event()
    totals, total_errors, total_unanswered = (
        collections.Counter(),
        collections.Counter(),
        0,
    )
    start = time.monotonic()

    for _ in range(CLIENTS):
        threading.Thread(target=client, args=(url, stop), daemon=True).start()

    try:
        while True:
            time.sleep(INTERVAL)

            with lock:
                counts, error_counts = answers.copy(), errors.copy()
                no_answer, unanswered = unanswered, 0
                answers.clear()
                errors.clear()

            totals.update(counts)
            total_errors.update(error_counts)
            total_unanswered += no_answer

            elapsed = time.monotonic() - start
            print(f"{elapsed:4.0f}s   {describe(counts, error_counts, no_answer)}")

    except KeyboardInterrupt:
        stop.set()

    with lock:
        totals.update(answers)
        total_errors.update(errors)
        total_unanswered += unanswered

    summary = f"total   {describe(totals, total_errors, total_unanswered)}"

    print(f"\n{summary}")

    with open("traffic.log", "w") as log:
        log.write(summary + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

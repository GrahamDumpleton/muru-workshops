"""Ask the application which worker answers, and send that worker SIGUSR1.

Usage: python reopen.py PORT
"""

import os
import signal
import sys
import urllib.request


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python reopen.py PORT")
        return 2

    with urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/", timeout=5) as response:
        pid = int(response.read().decode().split()[-1])

    os.kill(pid, signal.SIGUSR1)
    print(f"sent SIGUSR1 to worker process {pid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

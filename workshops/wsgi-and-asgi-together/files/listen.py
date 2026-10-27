"""Open WebSockets to the orders site and keep them open until Ctrl-C.

Each socket sends one message and prints the reply. Ctrl-C closes them
all normally, with code 1000.

Usage: python listen.py PORT COUNT
"""

import contextlib
import sys
import threading

from websockets.sync.client import connect


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python listen.py PORT COUNT")
        return 2

    count = int(sys.argv[2])

    with contextlib.ExitStack() as sockets:
        for number in range(1, count + 1):
            websocket = sockets.enter_context(connect(f"ws://127.0.0.1:{sys.argv[1]}/api/echo"))
            websocket.send(f"listener {number} is here")
            print(websocket.recv(timeout=5))

        print(f"{count} sockets open; press Ctrl-C to close them")

        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            pass

    print(f"closed {count} sockets")
    return 0


if __name__ == "__main__":
    sys.exit(main())

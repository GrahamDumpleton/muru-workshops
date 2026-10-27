"""Send one message over the orders site's WebSocket and print the reply.

Usage: python say.py PORT MESSAGE
"""

import sys

from websockets.sync.client import connect


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python say.py PORT MESSAGE")
        return 2

    with connect(f"ws://127.0.0.1:{sys.argv[1]}/api/echo") as websocket:
        websocket.send(sys.argv[2])
        print(websocket.recv(timeout=5))

    return 0


if __name__ == "__main__":
    sys.exit(main())

"""A small metrics client, of the kind that counts requests and sends
the counts to a statsd agent.

start() opens a UDP socket to the agent and starts a thread that sends
the counts every five seconds. No agent needs to be listening: what
matters here is the socket and the thread, and the line printed each
time the thread sends.
"""

import os
import socket
import threading
import time


class Metrics:
    def __init__(self, host: str, port: int, interval: float = 5.0):
        self.address = (host, port)
        self.interval = interval
        self.count = 0
        self.lock = threading.Lock()
        self.sock = None

    def start(self) -> None:
        """Open the socket to the agent and start the sending thread."""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect(self.address)

        threading.Thread(
            target=self._send_forever, name="metrics-sender", daemon=True
        ).start()

    def increment(self) -> None:
        with self.lock:
            self.count += 1

    def _send_forever(self) -> None:
        while True:
            time.sleep(self.interval)

            with self.lock:
                count, self.count = self.count, 0

            if not count:
                continue

            try:
                self.sock.send(f"catalog.requests:{count}|c".encode())

            except OSError:
                pass

            print(f"metrics: process {os.getpid()} sent a count of {count} requests")


client = Metrics("127.0.0.1", 8125)

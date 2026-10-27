"""Import the catalogue, then fork, as a preforking server does.

Usage: python fork_demo.py

Prints the threads and the metrics socket in the process that imported
the catalogue, and again in a child forked from it. Nothing checks the
import first, as nothing does under gunicorn --preload.
"""

import os
import sys
import threading

import catalog  # noqa: F401, imported for what it does at import
import metrics


def describe(who: str) -> None:
    threads = ", ".join(thread.name for thread in threading.enumerate())
    _, port = metrics.client.sock.getsockname()

    print(f"{who} (pid {os.getpid()})")
    print(f"  threads: {threads}")
    print(f"  metrics socket: descriptor {metrics.client.sock.fileno()}, from port {port}")


describe("Process that imported the catalogue")
sys.stdout.flush()

pid = os.fork()

if pid == 0:
    describe("Child forked from it")
    sys.stdout.flush()
    os._exit(0)

os.waitpid(pid, 0)

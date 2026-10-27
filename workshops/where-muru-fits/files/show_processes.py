"""Show the processes serving the muructl run listening on a port.

Usage: python show_processes.py PORT

Finds the muructl run started with --port PORT, then every process
below it, and prints them as a tree with what each one does. The last
line counts the workers.
"""

import os
import subprocess
import sys


def process_table() -> dict[int, tuple[int, str]]:
    """Return every process as pid -> (parent pid, command line)."""

    output = subprocess.run(
        ["ps", "-e", "-o", "pid=,ppid=,args="],
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    table = {}

    for line in output.splitlines():
        fields = line.split(None, 2)

        if len(fields) == 3:
            table[int(fields[0])] = (int(fields[1]), fields[2])

    return table


def is_muructl_run(args: str, port: str) -> bool:
    """Say whether a command line is a muructl run on the port."""

    words = args.split()

    if len(words) < 2 or os.path.basename(words[0]) != "muructl":
        return False

    if words[1] != "run":
        return False

    return any(
        word == "--port" and following == port
        for word, following in zip(words, words[1:])
    ) or f"--port={port}" in words


def short(args: str) -> str:
    """Shorten a command line to the part worth reading."""

    words = args.split()
    words[0] = os.path.basename(words[0])

    if "--socket-dir" in words:
        words = words[: words.index("--socket-dir")]

    return " ".join(words)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python show_processes.py PORT")
        return 2

    port = sys.argv[1]
    table = process_table()

    roots = [pid for pid, (_, args) in table.items() if is_muructl_run(args, port)]

    if not roots:
        print(f"No muructl run is serving port {port}. Start the server first.")
        return 1

    root = roots[0]

    children: dict[int, list[int]] = {}

    for pid, (ppid, _) in table.items():
        children.setdefault(ppid, []).append(pid)

    print(f"pid {root:<7} {short(table[root][1])}")
    print(f"{'':12}the edge and the controller, written in Rust")

    hosts = sorted(children.get(root, []))
    workers = []

    for host in hosts:
        print(f"  pid {host:<7} {short(table[host][1])}")
        print(f"{'':14}the host: imported hello.py once, forks the workers")

        for worker in sorted(children.get(host, [])):
            workers.append(worker)
            print(f"    pid {worker:<7} {short(table[worker][1])}")
            print(f"{'':16}a worker: a fork of the host, runs your code")

    print()

    if hosts:
        print(f"{len(workers)} workers, forked from host {hosts[0]}")
    else:
        print("0 workers: the host has not started yet")

    return 0


if __name__ == "__main__":
    sys.exit(main())

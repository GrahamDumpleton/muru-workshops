"""All seven of Muru's lifecycle hooks, each saying where it ran.

Each hook gets the context: worker_id is None in the host, and the
worker's index in a worker.
"""

import os


def report(hook, context):
    where = "host" if context.worker_id is None else f"worker {context.worker_id}"
    print(f"hook {hook:<15} in {where:<8} process {os.getpid()}")


def on_load(context):
    report("on_load", context)


def pre_fork(context):
    report("pre_fork", context)


def post_fork(context):
    report("post_fork", context)


def on_ready(context):
    report("on_ready", context)


def on_drain(context):
    report("on_drain", context)


def on_exit(context):
    report("on_exit", context)


def on_reopen_logs(context):
    report("on_reopen_logs", context)

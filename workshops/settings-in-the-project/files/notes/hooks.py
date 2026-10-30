"""Lifecycle hooks for the notes project."""


def post_fork(context):
    print(f"worker {context.worker_id} is starting")

"""Lifecycle hooks, named to muructl run with --hooks hooks."""

import metrics


def post_fork(context):
    """Run in each worker, right after it is forked from the host."""

    print(f"post_fork: starting the metrics client in worker {context.worker_id}")
    metrics.client.start()

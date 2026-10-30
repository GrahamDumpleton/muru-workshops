---
title: Finish
---

# Finish

You have watched all seven hooks run.

- `on_load` and `pre_fork` run once in the host, after the import and
  before the fork. `post_fork` and `on_ready` run in each worker as it
  starts, `on_drain` and `on_exit` as it stops.

- `post_fork` is where a worker opens what it must own, such as a
  database pool.

- A reload runs the new release's hooks first, and only once its
  workers serve are the old ones drained.

- `on_reopen_logs` runs in a worker sent `SIGUSR1`; the daemon sends
  it to every worker with `muructl logs reopen --workers`.

- Without an import in the host, each worker runs `on_load` and
  `pre_fork` itself, still before `post_fork`.

- An ASGI lifespan starts between `post_fork` and `on_ready`, and
  shuts down between `on_drain` and `on_exit`.

Click Finish below for where to go next.

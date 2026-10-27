---
title: Finish
---

# Finish

You have sprung the preload trap and seen what Muru does about it.

- A fork copies a process's memory, but only the thread that called
  fork runs in the child, and sockets are shared rather than copied.
  A thread or a connection opened at import does not survive a fork as
  you would expect, and nothing says so.

- Muru's host records what the import opened before it forks. Under
  `--preload auto`, the default, it says what it found and has each
  worker import the application itself. Under `--preload true` it
  refuses to start.

- A `post_fork` hook opens what each worker needs of its own after the
  fork, so the application can be preloaded and the workers forked
  from it again.

Click Finish below for where to go next.

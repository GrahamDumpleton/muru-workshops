---
title: Finish
---

# Finish

You have stopped a request at a breakpoint and attached to it.

- In a worker of `muructl run`, `breakpoint()` stops the request where
  it is and waits for a debugger, for 60 seconds or the `timeout` the
  call gives. The terminal names the worker, the line and the command
  to run, and `muructl debug status` and `muructl debug stacks` find
  the request.

- `muructl debug attach` opens pdb on the waiting request from any
  other terminal, through the run's admin socket. The frame's
  variables can be read and changed, and `continue` or the end of
  input lets the request go on.

- A request waiting at a breakpoint is exempt from the soft and hard
  timeouts, and the worker is not replaced while a session is open.

- A breakpoint nobody attaches to expires, and the request goes on as
  if the call were not there.

- With no breakpoint waiting, a session runs on a thread of its own in
  the worker, and what it changes is changed in that worker alone;
  `muructl debug exec` runs an expression in every worker.

Click Finish below for where to go next.

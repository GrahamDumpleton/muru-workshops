---
title: Finish
---

# Finish

You have measured what processes and threads buy on a regular CPython
interpreter.

- With one thread, every request but one waited in the edge's queue,
  for both views alike.

- Eight threads emptied the queue. The view that waits served eight
  times as many requests; the view that computes served the same, and
  spent the time waiting for the GIL instead, which showed as `app`
  time.

- Two processes let the computing view use two CPUs, and doubled what
  it could serve where there were two to use.

- The edge's `queue` and `app` times told the two problems apart:
  time in `queue` means every thread was busy, time in `app` beyond
  the view's own means waiting inside Python.

Click Finish below for where to go next.

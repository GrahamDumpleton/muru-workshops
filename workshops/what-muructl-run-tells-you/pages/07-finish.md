---
title: Finish
---

# Finish

You have read what `muructl run` reports while you develop.

- The startup lines come from the host, which imports your code once
  and forks the workers, and from `muructl`, which says where it
  serves and what development mode changes.

- The edge writes an access log line for every request, with the time
  it waited for a worker thread and the time your code took.
  `--access-log errors` keeps only failures and slow requests.

- Your code's output arrives tagged with the worker that wrote it,
  `.stdout` for what it prints, and nothing to configure for
  `logging`.

- When your code raises, the edge answers with the traceback, as HTML
  for a browser and as a problem document for an API client, and the
  access log line says `reason=app_error`. A reason appears only on a
  response Muru made itself. One request id ties the page, the log
  line and the `X-Request-ID` header together.

- The dashboard shows the workers, rates, latency, and recent requests
  and output, refreshed every two seconds.

Click Finish below for where to go next.

---
title: Finish
---

# Finish

You have seen where Muru fits among Python web servers.

- Apache with mod_wsgi, gunicorn, uvicorn and Granian each serve one
  version of your code at a time, and in most of them the process that
  reads a client's request also runs your code.

- Muru splits that work. The edge, in Rust, talks to clients, queues
  requests and writes the access log. The host imports your code once
  and forks the workers. The workers run your code and only ever talk
  to the edge.

- An exception in your code is a 500, and the worker carries on. A
  worker that dies is a 502 from the edge, and the host forks a
  replacement.

- Under the daemon, the edge can route to several releases at once,
  which is what makes deploys, canaries and rollbacks changes of
  routing rather than restarts.

Click Finish below for where to go next.

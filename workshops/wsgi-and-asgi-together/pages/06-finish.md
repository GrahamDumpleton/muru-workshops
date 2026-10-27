---
title: Finish
---

# Finish

You have served WSGI and ASGI from one server.

- Most servers take one interface, so a site with a Flask application
  and a FastAPI application usually runs two servers with a proxy in
  front that routes between them and passes WebSocket upgrades on.

- Muru's mounts, declared in `pyproject.toml`, put both applications
  in the same worker processes, from one preload: Flask on the
  workers' threads at `/`, FastAPI on their event loops at `/api`.

- Each application saw the mount's path where its interface expects
  it: `SCRIPT_NAME` for WSGI, `root_path` for ASGI.

- The edge handled the WebSocket protocol, for a browser behind
  JupyterLab's proxy and for a client in the terminal alike.

- Each socket had an access log line when FastAPI accepted it and a
  second, with the same request id, when it closed, saying how long it
  was open, who closed it and with what code.

- The dashboard counted the sockets open and listed each one, apart
  from the requests in flight.

- Stopping the site closed the socket still open with 1001, "going
  away", instead of waiting for it or cutting it off.

Click Finish below for where to go next.

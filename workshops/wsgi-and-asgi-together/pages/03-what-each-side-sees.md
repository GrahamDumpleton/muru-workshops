---
title: What each side sees
requires: [quiz:where-fastapi-runs, verify:both-sides]
---

# What each side sees

Each application has an `/about` path that describes the request as
it saw it. Ask Flask first.

```{execute}
:id: about-flask
:session: client
:wait: prompt
curl -s http://127.0.0.1:{{ app_port }}/about; echo
```

Flask answered, over WSGI, with an empty `SCRIPT_NAME`: it is mounted
at the root, so the whole path is its `PATH_INFO`.

```{quiz}
:id: where-fastapi-runs
question: A request for `/api/about` goes to FastAPI. Where does FastAPI run it?
options:
  - { text: "In a separate uvicorn process that muructl started for it", explanation: "There is no other server. The mounts are served by the same workers, which the host forked from one preload." }
  - { text: "In one of the same two worker processes, on that worker's event loop", correct: true }
  - { text: "In one of the same two worker processes, on one of its WSGI threads", explanation: "ASGI applications run on the worker's event loop, not its threads. FastAPI hands only plain `def` path operations to threads." }
explanation: "A worker with an ASGI mount runs an event loop beside its threads. The edge sends `/api` requests to a worker and the worker runs them on its loop."
```

```{execute}
:id: about-fastapi
:session: client
:wait: prompt
curl -s http://127.0.0.1:{{ app_port }}/api/about; echo
```

FastAPI answered, over ASGI, on the thread `muru-loop`, from one of
the same worker processes Flask's answers come from. Its `root_path`
is `/api`, the mount's path, and `path` is the whole path, as the ASGI
specification asks, so FastAPI matched its own `/about` route.

In the terminal on the left, the access log line for this request ends
`mount=api` before the worker: the edge picked the mount from the
path, then a worker.

```{verify}
:id: both-sides
:label: Flask answers at / and FastAPI at /api
:substrate: shell
:trigger: after:about-fastapi
flask=$(curl -s http://127.0.0.1:{{ app_port }}/about); fastapi=$(curl -s http://127.0.0.1:{{ app_port }}/api/about); case "$flask$fastapi" in *'"framework":"Flask"'*'"framework":"FastAPI"'*) echo "Flask at /, FastAPI at /api";; *) printf '%s\n%s\n' "$flask" "$fastapi"; exit 1;; esac
```

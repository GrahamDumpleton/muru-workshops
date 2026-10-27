---
title: A WebSocket
requires: [verify:websocket-echo]
---

# A WebSocket

The page at `/` comes from Flask. Its script opens a WebSocket to
`api/echo`, relative to the page, which is FastAPI's echo endpoint,
and sends a message as soon as it connects. Open it.

```{url-open}
:title: Open the site
:when: web_proxy
:url: {{ jupyter_url }}proxy/{{ app_port }}/
:pane: site
:area: viewer
```

```{url-open}
:title: Open the site
:when: not web_proxy
:url: http://127.0.0.1:{{ app_port }}/
:pane: site
:area: viewer
```

The page says which worker Flask served it from, then shows FastAPI's
reply to its first message, from a worker process of the same
`muructl run`. Click "Send a message" for more. Behind JupyterLab's
proxy the socket goes through JupyterLab first, and the edge still
handles the WebSocket protocol itself.

In the terminal on the left there are two lines for the page: `200
GET /` for the page itself, and `101 GET /api/echo` for its socket, 101
being the status of a successful WebSocket upgrade. The socket's line
is written when FastAPI accepts the socket, with the time the handshake
took, about a millisecond. The socket stays open for as long as the
page does.

`say.py` in your workspace does the same from the terminal, and then
closes its socket: it opens it, sends one message, prints the reply
and stops.

```{execute}
:id: say-hello
:session: client
:wait: prompt
python say.py {{ app_port }} "hello from the terminal"
```

```{verify}
:id: websocket-echo
:label: FastAPI echoes over the WebSocket
:substrate: shell
:trigger: after:say-hello
out=$(python say.py {{ app_port }} "checking" 2>&1); printf '%s\n' "$out" | grep 'got: checking' || { printf '%s\n' "$out"; exit 1; }
```

Two lines appeared for `say.py`'s socket, ending in the same `id=`.
The first is the handshake, like the page's. The second was written
when the socket closed, a few milliseconds later. Its time is how long
the socket was open, and the fields after it say how it ended:

- `websocket=closed by=client`: the client closed it first.

- `code=1000`: the close code, 1000 being a normal close.

- `received=1 sent=1`: the messages from the client and back to it.

Under gunicorn and uvicorn this site would be two servers, and the
proxy in front would need to be told to pass WebSocket upgrades to the
second. Here it is one release, one process tree and one set of logs,
with the sockets in them.

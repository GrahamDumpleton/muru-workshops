---
title: Sockets on the dashboard
requires: [verify:listeners-open, verify:dashboard-up, verify:listeners-closed, quiz:stop-with-socket-open, verify:site-stopped]
---

# Sockets on the dashboard

The page's socket is still open. `listen.py` in your workspace opens
five more, sends a message on each and keeps them open until you press
Ctrl-C. Start it in the terminal on the right.

```{execute}
:id: start-listeners
:session: client
:wait: 3s
python listen.py {{ app_port }} 5
```

```{verify}
:id: listeners-open
:label: The five sockets are open
:substrate: shell
:trigger: after:start-listeners
n=$(curl -s --max-time 2 http://127.0.0.1:{{ dashboard_port }}/v1/websockets | python -c 'import json, sys; print(json.load(sys.stdin)["open"])'); echo "WebSockets open: $n"; [ "${n:-0}" -ge 5 ]
```

Each has its handshake line in the terminal on the left, and no other
line yet. The startup lines gave the dashboard's address; open it.

```{url-open}
:title: Open the dashboard
:when: web_proxy
:url: {{ jupyter_url }}proxy/{{ dashboard_port }}/
:pane: dashboard
:area: viewer
```

```{url-open}
:title: Open the dashboard in a new browser tab
:when: not web_proxy
:url: http://127.0.0.1:{{ dashboard_port }}/
```

```{verify}
:id: dashboard-up
:label: The dashboard answers on port {{ dashboard_port }}
:substrate: shell
:trigger: page-enter
curl -sS --max-time 2 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:{{ dashboard_port }}/ | grep '^200$'
```

The page refreshes every two seconds. Look for:

- the "WebSockets open" tile, which counts six: the five from
  `listen.py` and the page's, if it is still open in its pane;

- the WebSockets table below the workers, which counts the open
  sockets by endpoint, all six at `/api/echo`, and then lists each
  one: when it opened, how long it has been open, the messages each
  way, the worker holding it, and the request id its handshake line
  in the terminal ends with;

- the chart of requests in flight and WebSockets open, under "Over
  time".

A socket is not a request in flight. Its request ended when FastAPI
accepted it, so the "In flight" tile stays at 0 while the sockets stay
open, and a socket held open for an hour does not show up in the
latency figures as an hour-long request.

Stop `listen.py`, which closes its five sockets normally.

```{interrupt}
:id: stop-listeners
:session: client
```

```{verify}
:id: listeners-closed
:label: The five sockets have closed
:substrate: shell
:trigger: after:stop-listeners
n=$(curl -s --max-time 2 http://127.0.0.1:{{ dashboard_port }}/v1/websockets | python -c 'import json, sys; print(json.load(sys.stdin)["open"])'); echo "WebSockets open: $n"; [ -n "$n" ] && [ "$n" -le 1 ]
```

Five closing lines appear in the terminal on the left, each `by=client
code=1000`, and within two seconds the dashboard counts one socket
open again: the page's.

That one is still open. What happens to it when the site stops?

```{quiz}
:id: stop-with-socket-open
question: You stop the site with Ctrl-C while the page's WebSocket is open. What happens to the socket?
options:
  - { text: "The worker closes it with code 1001, \"going away\", and the site stops at once", correct: true }
  - { text: "The site waits for the page to close the socket before it stops", explanation: "A WebSocket can stay open for hours, so a server that waited for its sockets might never stop. A stopping worker closes them itself." }
  - { text: "The connection is cut with no close, and the page sees an error", explanation: "The worker closes each open socket with a proper close frame, so the client can tell the server went away and reconnect." }
explanation: "A worker told to stop closes its open WebSockets with 1001, which means the server is going away. The application sees a disconnect, and the client sees a close it can reconnect after. `websocket_drain_grace` can give sockets time to finish first; by default it is nothing."
```

Stop the site in the terminal on the left.

```{interrupt}
:id: stop-site
:session: server
```

```{verify}
:id: site-stopped
:label: Nothing answers on port {{ app_port }}
:substrate: shell
:trigger: after:stop-site
for i in 1 2 3 4 5; do curl -s -o /dev/null --max-time 1 http://127.0.0.1:{{ app_port }}/ || { echo "The site has stopped."; exit 0; }; sleep 1; done; echo "The site still answers on port {{ app_port }}. Stop it with the action above."; exit 1
```

The last line before the site stopped is the closing line for the
page's socket: `websocket=closed by=edge code=1001`, with however long
the page was open. The page in its pane now says "closed".

Under the daemon, a deploy drains the old release the same way: its
workers close their sockets with 1001, and a client that reconnects
reaches the new release.

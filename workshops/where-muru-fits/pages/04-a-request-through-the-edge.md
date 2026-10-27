---
title: A request through the edge
requires: [verify:edge-answered, quiz:who-logs]
---

# A request through the edge

Open the application in a pane. The page comes from the worker, and it
tells you the worker's process id.

```{url-open}
:title: Open the application
:when: web_proxy
:url: {{ jupyter_url }}proxy/{{ app_port }}/
:pane: app
:area: viewer
```

```{url-open}
:title: Open the application
:when: not web_proxy
:url: http://127.0.0.1:{{ app_port }}/
:pane: app
:area: viewer
```

Look at the terminal on the left. A line appeared for the request,
like this one:

```
05:42:22.836 200 GET / 116B 0.7ms queue=0.0ms app=0.3ms worker=0 id=01M5XD1DB32J7V0PF09NA9AQZV
```

That is the time, the status, the method and path, the size of the
response and the total time taken. Then `queue` is how long the
request waited for a free worker thread, `app` is how long your code
took, `worker` is which worker served it, and `id` is the request's
id. Click the action above again to load the page afresh, and another
line appears.

Now send a request with curl, which shows the response headers.

```{execute}
:id: curl-headers
:session: client
:wait: prompt
curl -i http://127.0.0.1:{{ app_port }}/
```

The `server: muru` header comes from the edge, and so does
`x-request-id`: every response carries the same id that the access log
line and the body show, so a report from a user can be matched to the
log.

```{verify}
:id: edge-answered
:label: The response carries a request id
:substrate: shell
:trigger: after:curl-headers
curl -sS -D - -o /dev/null --max-time 2 http://127.0.0.1:{{ app_port }}/ | grep -i '^x-request-id'
```

```{quiz}
:id: who-logs
question: Which process wrote the access log line in the terminal on the left?
options:
  - { text: "The worker, once your code returned", explanation: "The worker only has the request from the moment a thread takes it. It cannot measure the time the request spent waiting for one." }
  - { text: "The host, which watches its workers", explanation: "The host imports the code and forks workers. Requests never pass through it." }
  - { text: "The edge, inside the muructl process", correct: true }
explanation: "The access log is the edge's. It has the request from the moment the client sent it until the last byte of the response went out, which is why it can report `queue`, the time before a worker took the request, beside `app`, the time your code took."
```

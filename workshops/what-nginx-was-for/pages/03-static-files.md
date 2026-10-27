---
title: Static files
requires: [quiz:who-sent-the-css, verify:not-modified]
---

# Static files

The route for `/static/` names a directory rather than an application,
so the edge serves the files in it. Ask for the headers of the shop's
style sheet.

```{execute}
:id: css-headers
:session: client
:wait: prompt
curl -sI http://127.0.0.1:{{ app_port }}/static/app.css
```

The type comes from the name, `Cache-Control` from the route's
`cache` setting, and `ETag`, `Last-Modified` and `Accept-Ranges` from
the file, the headers nginx's `alias` and `expires` give you.

A browser that has the file already asks again with the `ETag` it was
given, and gets `304 Not Modified` with no body.

```{execute}
:id: css-conditional
:session: client
:wait: prompt
etag=$(curl -sI http://127.0.0.1:{{ app_port }}/static/app.css | grep -i '^etag:' | cut -d' ' -f2 | tr -d '\r'); curl -s -o /dev/null -w '%{http_code}\n' -H "If-None-Match: $etag" http://127.0.0.1:{{ app_port }}/static/app.css
```

```{verify}
:id: not-modified
:label: The edge answers a conditional request with 304
:substrate: shell
:trigger: after:css-conditional
etag=$(curl -sI http://127.0.0.1:{{ app_port }}/static/app.css | grep -i '^etag:' | cut -d' ' -f2 | tr -d '\r'); curl -s -o /dev/null -w '%{http_code}\n' -H "If-None-Match: $etag" http://127.0.0.1:{{ app_port }}/static/app.css | grep '^304$'
```

`site/static` also has `app.css.gz`, the same file compressed ahead of
time. A client that accepts gzip gets it, as nginx's `gzip_static`
would send it, with nothing to configure.

```{execute}
:id: css-gzip
:session: client
:wait: prompt
curl -sI -H 'Accept-Encoding: gzip' http://127.0.0.1:{{ app_port }}/static/app.css | grep -i -E '^(content-encoding|content-length|vary):'
```

The precompressed file is about a twentieth of the size of the one the
first request got.

```{quiz}
:id: who-sent-the-css
question: Which process read `app.css` from disk and sent it?
options:
  - { text: "A worker, through the application", explanation: "The route names a directory, not an application. The request never reaches a worker." }
  - { text: "The edge", correct: true }
  - { text: "The daemon", explanation: "The daemon is never on the request path. It told the edge about the route when the file was applied." }
explanation: "A static route is served by the edge itself. Python never sees the request, which the access log shows."
```

```{execute}
:id: access-log-static
:session: client
:wait: prompt
muructl logs --access --lines 3
```

The access log lines for the style sheet say `reason=static` and name
no release and no worker.

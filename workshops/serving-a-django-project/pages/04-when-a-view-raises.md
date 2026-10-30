---
title: When a view raises
requires: [verify:muru-error-page]
---

# When a view raises

`/stock` raises `RuntimeError` for a negative stock count. Open it.

```{url-open}
:title: Open /stock
:when: web_proxy
:url: {{ jupyter_url }}proxy/{{ app_port }}/stock
:pane: site
:area: viewer
```

```{url-open}
:title: Open /stock
:when: not web_proxy
:url: http://127.0.0.1:{{ app_port }}/stock
```

This is Django's debug page, since `DEBUG` is on: the traceback with
each frame's local variables, then the request and the settings.
Django made the page, so to Muru it was an ordinary response, and the
access log line in the terminal on the left, `500 GET /stock`, has no
`reason=`.

The document's section on a view that raises says what
`DEBUG_PROPAGATE_EXCEPTIONS` changes. Set it in the project's settings.

```{editor-insert}
:id: add-propagate
:title: Set DEBUG_PROPAGATE_EXCEPTIONS in mysite/mysite/settings.py
:path: mysite/mysite/settings.py
:match: # The project is reached through
# Let an unhandled exception reach the server, which answers for it.
DEBUG_PROPAGATE_EXCEPTIONS = True

```

`--reload` started a new release with the setting. Load `/stock`
again.

```{url-open}
:title: Load /stock again
:when: web_proxy
:url: {{ jupyter_url }}proxy/{{ app_port }}/stock
:pane: site
:area: viewer
```

```{url-open}
:title: Load /stock again
:when: not web_proxy
:url: http://127.0.0.1:{{ app_port }}/stock
```

```{verify}
:id: muru-error-page
:label: Muru answers for the failing view
:substrate: shell
:trigger: after:add-propagate
for i in 1 2 3 4 5 6 7 8 9 10; do out=$(curl -s --max-time 2 -H 'Accept: application/json' http://127.0.0.1:{{ app_port }}/stock); printf '%s\n' "$out" | grep -q '"reason": *"app_error"' && { echo "Muru answers with reason app_error."; exit 0; }; sleep 1; done; echo "Django still answers for /stock. Check that settings.py sets DEBUG_PROPAGATE_EXCEPTIONS and that the terminal on the left switched to a new release."; exit 1
```

Now the pane has Muru's error page, the traceback without the local
variables, and the access log line ends `reason=app_error`, as it
would for a Flask or FastAPI project. Django's page tells you more
about one failure; Muru's records every failure the same way, in the
access log, the metrics and the dashboard. Either is a sound choice in
development. Neither shows a traceback in production: Django's page
needs `DEBUG`, and Muru's error page has the traceback only under
`muructl run`.

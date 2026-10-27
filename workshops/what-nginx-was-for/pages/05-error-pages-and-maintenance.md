---
title: Error pages and maintenance
requires: [verify:maintenance-page, verify:daemon-stopped]
---

# Error pages and maintenance

The application answers paths it does not know with a plain 404 of its
own. The release's `error_override` replaces that with the site's page
for clients that ask for HTML, as nginx's `proxy_intercept_errors`
would, and leaves API clients the application's answer.

```{execute}
:id: not-found-html
:session: client
:wait: prompt
curl -s -H 'Accept: text/html' http://127.0.0.1:{{ app_port }}/nothing
```

```{execute}
:id: not-found-plain
:session: client
:wait: prompt
curl -s http://127.0.0.1:{{ app_port }}/nothing
```

Now put the shop into maintenance. Where nginx would check for a flag
file, the edge has a switch.

```{execute}
:id: maintenance-on
:session: client
:wait: prompt
muructl maintenance on shop
```

```{execute}
:id: during-maintenance
:session: client
:wait: prompt
curl -s -i -H 'Accept: text/html' http://127.0.0.1:{{ app_port }}/
```

Every request to the application gets `503`, with `Retry-After` and
the release's maintenance page, from the edge, without troubling the
workers. The static files are still served, since they never involved
the application:

```{execute}
:id: static-during-maintenance
:session: client
:wait: prompt
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:{{ app_port }}/static/app.css
```

```{verify}
:id: maintenance-page
:label: The edge serves the maintenance page
:substrate: shell
:trigger: after:during-maintenance
out=$(curl -s -H 'Accept: text/html' -w '\n%{http_code}' http://127.0.0.1:{{ app_port }}/); if printf '%s\n' "$out" | tail -n 1 | grep -q '^503$' && printf '%s\n' "$out" | grep -q 'closed for a few minutes'; then echo "503 with the maintenance page"; else printf '%s\n' "$out" | tail -n 5; exit 1; fi
```

Open the shop again.

```{execute}
:id: maintenance-off
:session: client
:wait: prompt
muructl maintenance off shop
```

You have finished with the daemon. `--shutdown` drains the release,
stops its host and the edge, then the daemon.

```{execute}
:id: stop-daemon
:session: client
:wait: prompt
muructl daemon stop --shutdown
```

```{verify}
:id: daemon-stopped
:label: Nothing answers on port {{ app_port }}
:substrate: shell
:trigger: after:stop-daemon
if curl -s -o /dev/null --max-time 2 http://127.0.0.1:{{ app_port }}/; then echo "Something still answers on port {{ app_port }}. Stop the daemon with the action above."; exit 1; fi; echo "The daemon and everything under it have stopped."
```

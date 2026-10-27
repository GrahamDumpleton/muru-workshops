---
title: Start the daemon
requires: [verify:daemon-up]
---

# Start the daemon

Open the document on deploying new code. It goes through what a
deploy looks like under gunicorn and mod_wsgi, and with two
deployments behind a load balancer, then what the Muru daemon does
instead.

```{file-open}
:title: Open the document on deploying new code
:path: docs/deploying.md
:factory: Markdown Preview
:area: viewer
```

Start the daemon in the terminal on the right. It starts in the
background, so the terminal comes back once it answers.

```{execute}
:id: start-daemon
:session: client
:wait: prompt
muructl daemon start --listen 127.0.0.1:{{ app_port }}
```

It serves on port {{ app_port }} already, with nothing deployed, so
every request gets a 503 from the edge.

```{execute}
:id: nothing-deployed
:session: client
:wait: prompt
curl -s -i http://127.0.0.1:{{ app_port }}/
```

The reason is `no_workers`: no release is serving. `muructl daemon
status` shows the daemon, its edge process and where it keeps
everything.

```{execute}
:id: daemon-status
:session: client
:wait: prompt
muructl daemon status
```

```{verify}
:id: daemon-up
:label: The daemon answers on port {{ app_port }}
:substrate: shell
:trigger: after:start-daemon
code=$(curl -s -o /dev/null --max-time 2 -w '%{http_code}' http://127.0.0.1:{{ app_port }}/); [ "$code" = 503 ] && echo "The daemon answers 503: nothing is deployed yet" || { echo "Expected a 503 from the daemon, got: ${code:-no answer}"; exit 1; }
```

```{hint}
:title: If the check fails
If `muructl daemon start` said the address was in use, change
`app_port` from the gear button in the header of this panel and start
it again. If it said the daemon did not answer, look at
`muru/logs/daemon.log` and `muru/logs/edge.log` in your workspace.
```

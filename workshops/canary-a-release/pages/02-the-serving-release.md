---
title: The serving release
requires: [verify:r1-serving]
---

# The serving release

Open the document on canary releases. It covers how a canary is
usually built around a server that knows only one version of the code,
and what a rollout under the Muru daemon does instead.

```{file-open}
:title: Open the document on canary releases
:path: docs/canary.md
:factory: Markdown Preview
:area: viewer
```

Start the daemon in the terminal on the right, then deploy the first
version of the application as `greeter`. Each release has a host that
imports its code and forks two workers, and every response names the
release that served it.

```{execute}
:id: start-daemon
:session: client
:wait: prompt
muructl daemon start --listen 127.0.0.1:{{ app_port }}
```

```{execute}
:id: deploy-v1
:session: client
:wait: prompt
muructl deploy greeter releases/v1
```

Then declare the site's virtual host and route, from `routes.toml`.
The comment at its top says why the previews on the next page need
them.

```{file-open}
:title: Open routes.toml
:path: routes.toml
:area: viewer
```

```{execute}
:id: apply-routes
:session: client
:wait: prompt
muructl apply -f routes.toml
```

```{execute}
:id: curl-r1
:session: client
:wait: prompt
curl -s http://127.0.0.1:{{ app_port }}/
```

```{verify}
:id: r1-serving
:label: Release r1 serves through the route
:substrate: shell
:trigger: after:curl-r1
out=$(curl -sS --max-time 2 http://127.0.0.1:{{ app_port }}/); printf '%s\n' "$out" | grep 'release r1' || { printf '%s\n' "$out"; exit 1; }
```

```{hint}
:title: If the check fails
If `muructl daemon start` said the address was in use, change
`app_port` from the gear button in the header of this panel and start
it again, then deploy and apply. If it said the daemon did not answer,
look at `muru/logs/daemon.log` and `muru/logs/edge.log` in your
workspace.
```

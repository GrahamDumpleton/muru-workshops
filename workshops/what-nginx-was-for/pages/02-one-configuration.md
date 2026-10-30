---
title: One configuration
requires: [verify:shop-up]
---

# One configuration

Open the document on what nginx was for. It shows a typical nginx
configuration for a shop like this one, and what in Muru takes the
place of each part of it.

```{file-open}
:title: Open the document on what nginx was for
:path: docs/nginx-and-the-edge.md
:factory: Markdown Preview
:area: viewer
```

The shop's whole configuration under Muru is one file. Read its
comments: the application and its release settings, the error pages,
the virtual host, and two routes, one to the static files and one to
the application. Every path in it is relative to the file, so the
site's directories are named as they lie beside it, except the
release's own error pages, which lie under its source.

```{file-open}
:title: Open site.toml
:path: site.toml
:area: viewer
```

Start the daemon, then apply the file, by its full path so the
daemon resolves the paths in it from where it is. `muructl apply`
creates the application and deploys its release, then creates the
host and the routes.

```{execute}
:id: start-daemon
:session: client
:wait: prompt
muructl daemon start --listen 127.0.0.1:{{ app_port }}
```

```{execute}
:id: apply-site
:session: client
:wait: prompt
muructl apply -f "$PWD/site.toml"
```

```{verify}
:id: shop-up
:label: The shop answers on port {{ app_port }}
:substrate: shell
:trigger: after:apply-site
curl -sS --max-time 2 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:{{ app_port }}/ | grep '^200$'
```

```{hint}
:title: If the check fails
If `muructl daemon start` said the address was in use, change
`app_port` from the gear button in the header of this panel, start it
again and apply the file. If `muructl apply` reported errors, read
them: each names the line of `site.toml` it could not take.
```

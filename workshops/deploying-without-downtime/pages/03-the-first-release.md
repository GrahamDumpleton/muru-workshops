---
title: The first release
requires: [verify:r1-serving]
---

# The first release

A release is a source directory and the settings it is deployed with.
The first version of the application is in `releases/v1`. Its
`pyproject.toml` names the entrypoint and asks for two worker
processes, exactly as it would for `muructl run`.

```{file-open}
:title: Open releases/v1/greeter.py
:path: releases/v1/greeter.py
:area: viewer
```

```{file-open}
:title: Open releases/v1/pyproject.toml
:path: releases/v1/pyproject.toml
:area: viewer
```

Deploy it as the application `greeter`.

```{execute}
:id: deploy-v1
:session: client
:wait: prompt
muructl deploy greeter releases/v1
```

The first deploy created the application and its first release, `r1`,
started a host for it that imported the code and forked two workers,
and told the edge to send requests to it once both were ready.

```{execute}
:id: curl-r1
:session: client
:wait: prompt
curl -s http://127.0.0.1:{{ app_port }}/
```

```{verify}
:id: r1-serving
:label: Release r1 serves
:substrate: shell
:trigger: after:curl-r1
out=$(curl -sS --max-time 2 http://127.0.0.1:{{ app_port }}/); printf '%s\n' "$out" | grep 'release r1' || { printf '%s\n' "$out"; exit 1; }
```

`muructl release list` shows the application's releases, which one
serves, and its workers as processes times threads.

```{execute}
:id: list-r1
:session: client
:wait: prompt
muructl release list greeter
```

---
title: Hold and preview
requires: [verify:r2-previewed]
---

# Hold and preview

The second version changes the greeting. Deploy it with `--hold`: the
daemon starts it beside `r1`, waits until its workers are ready, and
gives it no traffic.

```{file-open}
:title: Open releases/v2/greeter.py
:path: releases/v2/greeter.py
:area: viewer
```

```{execute}
:id: deploy-v2-held
:session: client
:wait: prompt
muructl deploy greeter releases/v2 --hold
```

```{execute}
:id: list-held
:session: client
:wait: prompt
muructl release list greeter
```

`r2` is `ready` and `held: not serving`. An ordinary request still
gets `r1`.

```{execute}
:id: curl-still-r1
:session: client
:wait: prompt
curl -s http://127.0.0.1:{{ app_port }}/
```

A request that names `r2` in the `Muru-Preview` header gets it, which
is how you check a release with real requests before any user sees
it. A browser does the same with a `muru_preview=r2` cookie.

```{execute}
:id: curl-preview
:session: client
:wait: prompt
curl -s -H 'Muru-Preview: r2' http://127.0.0.1:{{ app_port }}/
```

```{verify}
:id: r2-previewed
:label: A preview reaches the held release r2
:substrate: shell
:trigger: after:curl-preview
plain=$(curl -sS --max-time 2 http://127.0.0.1:{{ app_port }}/); preview=$(curl -sS --max-time 2 -H 'Muru-Preview: r2' http://127.0.0.1:{{ app_port }}/); case "$plain|$preview" in *'release r1'*'|'*'release r2'*) echo "r1 serves; the preview reaches r2";; *) printf 'without a preview: %s\nwith one: %s\n' "$plain" "$preview"; exit 1;; esac
```

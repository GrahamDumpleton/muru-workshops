---
title: From development to the daemon
requires: [verify:server-stopped]
---

# From development to the daemon

Back in the first document, every arrangement served new code by
replacing the processes that ran the old code. Open the last document,
which shows what Muru does instead when it runs as a daemon.

```{file-open}
:title: Open the document on the daemon and releases
:path: docs/releases.md
:factory: Markdown Preview
:area: viewer
```

The settings of a development run carry over to the daemon. Ask
`muructl run` to write them out as the configuration the daemon reads,
rather than serving.

```{execute}
:id: print-config
:session: client
:wait: prompt
muructl run hello:application --processes 3 --threads 2 --print-config
```

Scroll to the end of the output. The `[app.hello.release.r1]` table is
the application as a release: its source directory, its entrypoint,
the Python it runs on, and the three processes of two threads you
asked for. `muructl apply` takes a file like this one, and the
workshops on the daemon start from there.

You have finished with the server. Stop it in the terminal on the
left.

```{interrupt}
:id: stop-server
:session: server
```

On Ctrl-C, the workers finish the requests they are serving, then
everything exits.

```{verify}
:id: server-stopped
:label: Nothing answers on port {{ app_port }}
:substrate: shell
:trigger: after:stop-server
if curl -s -o /dev/null --max-time 2 http://127.0.0.1:{{ app_port }}/; then echo "The server still answers on port {{ app_port }}. Stop it with the action above."; exit 1; fi; echo "The server has stopped."
```

---
title: What the daemon gets
requires: [verify:config-written, verify:project-stopped]
---

# What the daemon gets

The table is not only for `muructl run`. Deploying the project
directory to Muru's daemon reads the same table, so the settings that
serve it on your laptop become its release's settings.

`--print-config` shows what a run amounts to in the daemon's terms
without serving anything. Stop the project and write it to a file.

```{interrupt}
:id: stop-project
:session: server
```

```{execute}
:id: print-config
:session: client
:wait: prompt
muructl run notes --port {{ app_port }} --print-config > notes-config.toml
```

```{file-open}
:title: Open notes-config.toml
:path: notes-config.toml
:area: viewer
```

```{verify}
:id: config-written
:label: The declarative configuration is written
:substrate: shell
:trigger: after:print-config
grep '^\[app.notes.release.r1\]' notes-config.toml || { echo "notes-config.toml has no release in it. Write it with the action above."; exit 1; }
```

It has three parts:

- `[[listener]]` and `[limits]`: the address from `--port` and the
  limits the edge applies. Under the daemon these belong to the
  daemon's own configuration file, since one daemon serves many
  applications.

- `[app.notes.release.r1]`: the release, named after the module of the
  entrypoint, with the entrypoint, processes, threads and hooks from
  the table, and the defaults `muructl run` filled in for the rest.

- `[app.notes.release.r1.timeouts]` and `[app.notes.release.r1.env]`:
  the soft timeout and the title from the table, beside the other
  timeouts at their defaults.

Nothing of `[tool.muru.run]` or `muru.local.toml` is in it: the
listener's port came from the `--port` flag here, and would come from
them otherwise, but how a checkout is served on a laptop is not the
daemon's business, and `muructl deploy` ignores both.

`muructl apply` takes a file like this one, and `muructl deploy` makes
the release from the project directory itself, so `[tool.muru]` is the
one place the application's settings live.

gunicorn has `--print-config` too, which prints the settings its five
sources add up to. Muru's is a step further on: the file it writes is
what the daemon runs.

```{verify}
:id: project-stopped
:label: Nothing answers on port {{ app_port }}
:substrate: shell
:trigger: after:stop-project
for i in 1 2 3 4 5; do curl -s -o /dev/null --max-time 1 http://127.0.0.1:{{ app_port }}/ || { echo "The project has stopped."; exit 0; }; sleep 1; done; echo "The project still answers on port {{ app_port }}. Stop it with the action above."; exit 1
```

---
title: A request in flight
requires: [verify:new-release-serves, verify:project-stopped]
---

# A request in flight

`/slow` takes three seconds to answer. `slow.py` asks for it and
prints the answer. Start it, and while it waits, change the template.

```{execute}
:id: start-slow
:session: client
:wait: 1s
python slow.py {{ app_port }}
```

```{editor-replace}
:id: change-while-slow
:title: Change "On the menu" to "Menu of the day"
:path: menu/templates/page.html
:match: On the menu
Menu of the day
```

```{verify}
:id: new-release-serves
:label: The new release serves the new heading
:substrate: shell
:trigger: after:change-while-slow
for i in 1 2 3 4 5 6 7 8 9 10; do out=$(curl -s --max-time 2 http://127.0.0.1:{{ app_port }}/); case "$out" in *"Menu of the day"*) printf '%s\n' "$out" | head -n 1; exit 0;; esac; sleep 1; done; printf '%s\n' "${out:-Nothing answers on port {{ app_port }}.}"; exit 1
```

In the terminal on the right, `/slow answered 200 after 3.0 s`, with
the old heading, `On the menu`, from the old worker process: the
request had started on the old release and finished there, while the
new release was started and switched to. The access log line for
`/slow` is in the terminal on the left after `switched to release`,
since a line is written when a request ends.

Stop the project before moving on to HTTPS.

```{interrupt}
:id: stop-reload
:session: server
```

```{verify}
:id: project-stopped
:label: Nothing answers on port {{ app_port }}
:substrate: shell
:trigger: after:stop-reload
for i in 1 2 3 4 5; do curl -s -o /dev/null --max-time 1 http://127.0.0.1:{{ app_port }}/ || { echo "The project has stopped."; exit 0; }; sleep 1; done; echo "The project still answers on port {{ app_port }}. Stop it with the action above."; exit 1
```

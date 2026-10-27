---
title: Back to gunicorn
requires: [quiz:rollback-to-gunicorn, verify:gunicorn-back, verify:nothing-unanswered, verify:daemon-stopped]
---

# Back to gunicorn

Suppose something about the application under Muru turns out to need
more work. The gunicorn release is still warm.

```{quiz}
:id: rollback-to-gunicorn
question: "You run `muructl rollback orders` with the traffic still running. What happens?"
options:
  - { text: "The traffic moves back to gunicorn at once, with no request refused", correct: true }
  - { text: "gunicorn is started again, and requests get 503 until it answers", explanation: "The retained release kept gunicorn running, which is what makes the rollback instant." }
  - { text: "Nothing: a managed server release cannot be rolled back to", explanation: "A managed server release is a release like any other: it can be held, canaried against, drained, retained and rolled back to." }
explanation: "The gunicorn release was retained with its instance running, so the edge moves the traffic back to it at once. The Muru release is retained in its turn."
```

```{execute}
:id: rollback
:session: client
:wait: prompt
muructl rollback orders
```

In the terminal on the left, the answers are from `gunicorn` again.

```{verify}
:id: gunicorn-back
:label: gunicorn serves again
:substrate: shell
:trigger: after:rollback
out=$(curl -sS --max-time 2 http://127.0.0.1:{{ app_port }}/); printf '%s\n' "$out" | grep 'Served by gunicorn' || { printf '%s\n' "$out"; exit 1; }
```

Stop the traffic. Its totals count the answers from each server: no
request went unanswered, from gunicorn to Muru and back.

```{interrupt}
:id: stop-traffic
:session: server
```

```{verify}
:id: nothing-unanswered
:label: No request went unanswered
:substrate: shell
:trigger: after:stop-traffic
for i in 1 2 3 4 5; do [ -f traffic.log ] && break; sleep 1; done; out=$(cat traffic.log 2>/dev/null); printf '%s\n' "$out" | grep 'no answer: 0$' || { echo "${out:-traffic.py has not written its totals yet. Stop it with the action above.}"; exit 1; }
```

You have finished with the daemon. `--shutdown` drains every release,
stopping gunicorn with its profile's signal, then stops the edge and
the daemon.

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

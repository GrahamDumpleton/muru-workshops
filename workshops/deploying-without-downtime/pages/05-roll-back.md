---
title: Roll back
requires: [verify:r1-back, verify:nothing-unanswered]
---

# Roll back

Suppose `r2` turns out to be wrong. With the traffic still running,
roll back.

```{execute}
:id: rollback
:session: client
:wait: prompt
muructl rollback greeter
```

It returned straight away: `r1` was warm, so the edge moved the
traffic back to it at once, and its worker count grows back to two by
forking from its host. In the terminal on the left, the answers are
from `release r1` again, and `no answer` is still 0.

```{verify}
:id: r1-back
:label: Release r1 serves again
:substrate: shell
:trigger: after:rollback
out=$(curl -sS --max-time 2 http://127.0.0.1:{{ app_port }}/); printf '%s\n' "$out" | grep 'release r1' || { printf '%s\n' "$out"; exit 1; }
```

```{execute}
:id: list-after-rollback
:session: client
:wait: prompt
muructl release list greeter
```

Now `r2` is the retained one, so you could roll forward to it as
quickly.

Stop the traffic. It prints the totals: every request answered, by one
release or the other.

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

---
title: Move the traffic
requires: [verify:muru-promoted]
---

# Move the traffic

Start `traffic.py` in the terminal on the left: four clients asking for
the page over and over, and every two seconds a line counting the
answers by the server that gave them. Leave it running.

```{execute}
:id: start-traffic
:session: server
:wait: 4s
python traffic.py {{ app_port }}
```

Canary the Muru release against gunicorn: 10% of the requests, then
50%, each step held for ten seconds and judged once `r2` has served 20
requests in it, then all of them. The gates compare `r2` with `r1`
over the same requests, so Muru's workers are judged against
gunicorn's own numbers.

```{execute}
:id: canary-native
:session: client
:wait: prompt
muructl rollout canary orders@r2 --steps 10,50 --hold 10s --min-requests 20 --wait
```

In the terminal on the left the answers move from `gunicorn` to `Muru`:
about one in ten, then one in two, then all.

```{verify}
:id: muru-promoted
:label: The Muru release was promoted
:substrate: shell
:trigger: after:canary-native
out=$(muructl rollout status orders 2>&1); printf '%s\n' "$out" | grep ' r2 .*promoted' || { printf '%s\n' "$out"; exit 1; }
```

```{execute}
:id: list-after-canary
:session: client
:wait: prompt
muructl release list orders
```

Muru's workers serve. The gunicorn release is `retained`: drained of
requests, and kept warm, gunicorn still running, for 30 minutes.

---
title: Deploy under load
requires: [quiz:failed-during-deploy, verify:r2-serving]
---

# Deploy under load

`traffic.py` in your workspace keeps four clients asking for the page,
about a hundred requests a second, and every two seconds prints how
many answers came from each release and how many requests got no
answer at all. Start it in the terminal on the left, and leave it
running.

```{execute}
:id: start-traffic
:session: server
:wait: 4s
python traffic.py {{ app_port }}
```

The second version of the application, in `releases/v2`, changes the
greeting.

```{file-open}
:title: Open releases/v2/greeter.py
:path: releases/v2/greeter.py
:area: viewer
```

```{quiz}
:id: failed-during-deploy
:type: text
question: How many of the requests from `traffic.py` will go unanswered while `releases/v2` is deployed?
answer: "0"
otherwise: "Think about when the edge moves requests to the new release, and what happens to the requests the old release already has."
explanation: "None. The new release starts beside the old one, and the edge moves new requests to it only once its workers are ready. The old release finishes the requests it already has before it stops."
```

Deploy it while the traffic runs.

```{execute}
:id: deploy-v2
:session: client
:wait: prompt
muructl deploy greeter releases/v2
```

In the terminal on the left, the answers move from `release r1` to
`release r2` within one two-second line, and `no answer` stays at 0.

```{verify}
:id: r2-serving
:label: Release r2 serves
:substrate: shell
:trigger: after:deploy-v2
out=$(curl -sS --max-time 2 http://127.0.0.1:{{ app_port }}/); printf '%s\n' "$out" | grep 'release r2' || { printf '%s\n' "$out"; exit 1; }
```

```{execute}
:id: list-r2
:session: client
:wait: prompt
muructl release list greeter
```

`r2` serves. `r1` is `retained`: drained of its requests, and kept warm
for 30 minutes, its host and one worker still running, so that going
back to it needs no new start.

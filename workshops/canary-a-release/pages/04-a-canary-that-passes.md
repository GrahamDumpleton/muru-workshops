---
title: A canary that passes
requires: [verify:r2-promoted]
---

# A canary that passes

A canary needs traffic to judge. Start `traffic.py` in the terminal on
the left: four clients asking for the page over and over, with every
two seconds a line counting the answers from each release, the errors
among them, and the requests that got no answer. Leave it running for
this page and the next.

```{execute}
:id: start-traffic
:session: server
:wait: 4s
python traffic.py {{ app_port }}
```

Now canary `r2`. The settings are shortened so the workshop does not
take all afternoon: two steps, 10% then 50%, each held for ten
seconds, with the gates judging once `r2` has served 20 requests in
the step. The defaults are two minutes a step and 100 requests. The
error rate gate, at its default of 1%, applies. `--wait` follows the
rollout until it ends.

```{execute}
:id: canary-r2
:session: client
:wait: prompt
muructl rollout canary greeter@r2 --steps 10,50 --hold 10s --min-requests 20 --wait
```

Watch the terminal on the left as it runs: about one answer in ten
from `release r2`, then about one in two, then all of them, and no
errors.

```{execute}
:id: status-r2
:session: client
:wait: prompt
muructl rollout status greeter
```

The rollout is `promoted` because every step passed its gates. `r2`
serves, and `r1` is kept warm as after a deploy.

```{verify}
:id: r2-promoted
:label: The canary of r2 was promoted
:substrate: shell
:trigger: after:status-r2
out=$(muructl rollout status greeter 2>&1); printf '%s\n' "$out" | grep ' r2 .*promoted' || { printf '%s\n' "$out"; exit 1; }
```

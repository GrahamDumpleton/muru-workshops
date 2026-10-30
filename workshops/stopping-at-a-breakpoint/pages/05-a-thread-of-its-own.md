---
title: A thread of its own
requires: [verify:one-worker-changed, verify:shop-stopped]
---

# A thread of its own

With no breakpoint waiting, `muructl debug attach` still opens a
session, on a thread of its own in the worker, from which the worker's
modules and state can be read and changed. Attach to worker 0.

```{execute}
:id: attach-thread
:session: client
:wait: 3s
muructl debug attach checkout --worker 0
```

`attached to worker 0 at a thread of its own`. The frame is the
runtime's, not a request's, so reach the shop through its module.
Read the price list, then change the cup's price in this worker.

```{execute}
:id: import-shop
:session: client
:wait: 1s
import checkout
```

```{execute}
:id: print-prices
:session: client
:wait: 1s
p checkout.PRICES
```

```{execute}
:id: change-cup
:session: client
:wait: 1s
checkout.PRICES["cup"] = 4
```

```{execute}
:id: continue-thread
:session: client
:wait: prompt
continue
```

Each worker is a process with state of its own, so the change is in
worker 0 alone. `muructl debug exec` runs an expression in every
worker and prints each one's answer.

```{execute}
:id: exec-prices
:session: client
:wait: prompt
muructl debug exec checkout -- 'import checkout; checkout.PRICES["cup"]'
```

```{verify}
:id: one-worker-changed
:label: Worker 0 charges 4 for a cup and worker 1 still 3
:substrate: shell
:trigger: after:exec-prices
out=$(muructl debug exec checkout -- 'import checkout; checkout.PRICES["cup"]' 2>&1); printf '%s\n' "$out" | tr '\n' ' ' | grep -o 'worker 0 ([^)]*): 4 worker 1 ([^)]*): 3' || { printf '%s\n' "${out:-Nothing answers on port {{ app_port }}.}" | tail -n 6; exit 1; }
```

Under the daemon, `debug exec` and `debug attach` are allowed only
where its configuration sets `debug_exec`, since they run code in a
production worker. Under `muructl run` they need nothing: the person
at the terminal started the workers.

You have finished with the shop. Stop it in the terminal on the left.

```{interrupt}
:id: stop-shop
:session: server
```

```{verify}
:id: shop-stopped
:label: Nothing answers on port {{ app_port }}
:substrate: shell
:trigger: after:stop-shop
for i in 1 2 3 4 5; do curl -s -o /dev/null --max-time 1 http://127.0.0.1:{{ app_port }}/ || { echo "The shop has stopped."; exit 0; }; sleep 1; done; echo "The shop still answers on port {{ app_port }}. Stop it with the action above."; exit 1
```

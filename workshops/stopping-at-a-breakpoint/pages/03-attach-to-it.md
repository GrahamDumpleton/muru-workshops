---
title: Attach to it
requires: [verify:order-charged]
---

# Attach to it

Attach to the waiting request. Without `--worker`, the command takes
the worker that has a breakpoint waiting, whichever of the two it is.

```{execute}
:id: attach
:session: client
:wait: 3s
muructl debug attach checkout
```

`muru: attached to worker N at .../checkout.py:17; the end of input
lets the code go on`, then pdb's usual two lines, the file and
function and the line about to run, and its `(Pdb)` prompt. Each line
you type now is a pdb command, run in the worker, in the request's
frame. Look at what it is about to charge.

```{execute}
:id: print-price
:session: client
:wait: 1s
p item, price
```

`('teapt', 0)`: the misspelt name found no price, and the checkout was
about to charge nothing for it. This is a debugger, so the frame's
variables can be changed before the code goes on. Set the price to the
teapot's.

```{execute}
:id: set-price
:session: client
:wait: 1s
price = 12
```

Let the request go on. `continue` ends the session; so would the end
of input, or an hour in all, or ten minutes without a line.

```{execute}
:id: continue
:session: client
:wait: prompt
continue
```

`muru: the session in worker N has ended`, and the shell is back. In
the terminal on the left, `debug.attached` when the session opened,
`debug.detached` when it ended, and the access log line for the
request, `200` after however long it waited. `curl` has written its
answer.

```{execute}
:id: show-order
:session: client
:wait: prompt
cat order.txt
```

```{verify}
:id: order-charged
:label: The checkout charged the price set in the debugger
:substrate: contents
:message: order.txt does not say "charged 12 for teapt" yet. Attach with the action above, set the price and continue; the request writes the file when it finishes.
contains order.txt charged 12 for teapt
```

While the session was open, that worker took no new requests, which
went to the other one, and nothing replaced it: recycling, the hard
timeout, memory limits and scaling all wait for a session to end.

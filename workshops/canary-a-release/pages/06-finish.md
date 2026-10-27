---
title: Finish
---

# Finish

You have canaried two releases on the Muru daemon.

- `muructl deploy --hold` started a release beside the serving one,
  with no traffic, and a `Muru-Preview` header reached it by name.

- `muructl rollout canary` gave the good release 10% and then 50% of
  the requests, judged it against the serving release at every step,
  and promoted it when the gates passed.

- The release with a bug was taken out on its own during the first
  step, as soon as its error rate was over the limit and worse than
  the baseline's, and kept warm for looking at.

- None of it needed a second deployment or a load balancer: the edge
  already routes to several releases of an application, so a canary is
  a change of routing.

Click Finish below for where to go next.

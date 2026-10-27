---
title: Finish
---

# Finish

You have deployed to the Muru daemon without dropping a request.

- A deploy started the new release beside the one serving, and the
  edge switched to it only when its workers were ready. Not one of
  the requests went unanswered.

- The old release was kept warm, its host and one worker running, so
  the rollback moved the traffic back at once.

- The edge, the daemon and each release's host are separate processes.
  The edge holds the connections, and the daemon is never on the
  request path, so it can be stopped and started again without
  stopping the traffic.

- What used to take two deployments and a load balancer happened on
  one machine, with one command each way.

Click Finish below for where to go next.

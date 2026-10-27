---
title: Finish
---

# Finish

You have moved an application from gunicorn to Muru's workers and back
without changing how it is deployed.

- The daemon ran the gunicorn command as it was, as a release of its
  own, behind the edge.

- The same application on Muru's workers was held beside it,
  previewed, and given the traffic a share at a time, judged against
  gunicorn's numbers over the same requests.

- The way back to gunicorn was one instant rollback, because the
  release it replaced was kept warm.

The last section of the document, "When to choose which", sums up
where each server fits. With a managed release, the choice can be made
an application, and a share of its traffic, at a time.

Click Finish below for where to go next.

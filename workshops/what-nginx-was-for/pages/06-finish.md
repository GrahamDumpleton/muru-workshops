---
title: Finish
---

# Finish

You have served a shop from one Muru configuration file, with no proxy
in front, and checked what the edge does that nginx usually does.

- A static route served files from disk with cache headers, `ETag` and
  `Last-Modified`, answered a conditional request with `304`, and sent
  the precompressed file to a client that accepts gzip. Python never
  saw those requests.

- The edge compressed the application's JSON, after the worker had
  finished with it.

- The application named a report with `X-Muru-Sendfile`, and the edge
  sent it as a static file, ranges included, from the directories the
  release allows.

- The site's own 404 page replaced the application's for browsers, and
  maintenance mode answered every request to the application with the
  maintenance page while the static files went on being served.

Click Finish below for where to go next.

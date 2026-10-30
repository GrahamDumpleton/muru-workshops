---
title: Finish
---

# Finish

You have fitted reload and HTTPS to a project.

- `--reload` counts `**/*.py` under the project's directory as source.
  `--reload-include` adds patterns to that, `--reload-exclude` keeps
  files the application writes from starting a release, and an exclude
  wins over an include, so `--reload-exclude '**/*.py'` watches the
  included patterns alone.

- A reload starts the new release beside the old one. A request in
  flight finishes on the old release, with the old code.

- `--host` adds a name to the development certificate, `--https-only`
  answers plain HTTP with a 307 to the same path over HTTPS, and
  `--tls-cert` with `--tls-key` serves a certificate of your own, read
  from the project's directory.

Click Finish below for where to go next.

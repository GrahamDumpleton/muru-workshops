---
title: Finish
---

# Finish

You have moved a project's server settings into the project.

- gunicorn keeps settings in a Python file and four other places,
  uvicorn and Granian on the command line and in environment
  variables, and mod_wsgi in the Apache configuration. Muru keeps them
  in a `[tool.muru]` table in `pyproject.toml`, or in a `muru.toml`.

- The table holds what the application needs wherever it runs: its
  entrypoint, processes, threads, hooks, timeouts and environment
  variables. How one run is served, its port among them, stays on the
  command line.

- A flag wins over the table for one run, and a key the table does not
  know stops the run with a list of the keys it does.

- `--print-config` writes what a run amounts to as the daemon's
  declarative configuration: the listener and limits for the daemon's
  own file, and the release made from the table.

Click Finish below for where to go next.

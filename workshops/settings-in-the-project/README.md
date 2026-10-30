# Keep the run settings with the project

Starts a small WSGI project under a long `muructl run` command line,
then moves its settings into the project's `[tool.muru]` table: the
processes, threads, hooks module, a timeout and an environment
variable. Shows which settings belong in the table and which stay on
the command line, that a flag wins over the table for one run, what a
misspelt key does, and what `muructl run --print-config` writes for
the daemon. Compares with where gunicorn, uvicorn, Granian and mod_wsgi
keep their settings.

About 20 minutes, in two terminals with a document and the project's
files in an area above them. It installs `muru` and `muructl`
0.1.0a11 into an environment of its own, and serves on port 8080
unless you change it.

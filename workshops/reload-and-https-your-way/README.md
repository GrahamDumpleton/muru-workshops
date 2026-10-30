# Reload and HTTPS beyond the defaults

Serves a small menu application with a template and a data file under
`muructl run --reload`. Makes the reload watch templates and data with
`--reload-include`, keeps the file the application writes on every
request from triggering it with `--reload-exclude`, and watches a slow
request finish on the old release while a new one takes over. Then
adds a name to the development certificate with `--host`, redirects
HTTP to HTTPS with `--https-only`, and serves a certificate from a
local CA made with `trustme` through `--tls-cert`. Compares with
gunicorn's and uvicorn's options.

About 30 minutes, in two terminals with a document and the project's
files in an area above them. It installs `muru` and `muructl` 0.1.0a11
and `trustme` into an environment of its own, keeps its certificates
in the workspace, and serves on ports 8080 and 8443 unless you change
them.

# Muru workshops: outline

The design of this course: how it is organised, what each workshop
covers, its name and format, and the decisions that cut across all of
them. It is a living document. Read it before adding a workshop, and
update it when one is added, changed or dropped: the status table at
the end records where each workshop stands, and the open questions
section shrinks as they are settled. The design is settled here, before
the first workshop of a collection is written.

## What this course is

Guided JupyterLab workshops on [Muru](https://github.com/GrahamDumpleton/muru),
the routing edge, control plane and Python runtime for WSGI and ASGI
applications. They are for Python web developers who have deployed an
application with Apache and mod_wsgi, gunicorn, uvicorn or Granian, and
want to know what Muru is, why they would use it, and how.

**Meet Muru** (`introduction`, Part I, ten workshops) is the first
collection and is partly an advertisement. It says where Muru fits
among the servers learners know, shows what it does while they develop,
and shows the daemon deploying releases side by side, which is what the
other servers cannot do on their own. Every workshop puts the familiar
server's way briefly beside Muru's, in prose and diagrams. It assumes
the learner knows what a WSGI or ASGI application is and has run one
under some server. It uses only what is in a released version of Muru.

Later collections go into depth on one area each (see "Later
collections"). They are candidates only until designed here.

Out of scope for the whole course: the WSGI and ASGI protocols
themselves, which
[wsgi-workshops](https://github.com/GrahamDumpleton/wsgi-workshops)
teaches, and developing Muru, which its own repository covers.

## Source material

Everything the workshops say about Muru comes from its documentation,
its source and the installed release, never from memory.

- `reference/muru` is a git submodule of the Muru repository at the
  tag of the release the workshops teach, `v0.1.0-alpha.10` (published
  on PyPI as 0.1.0a10). The user documentation under `docs/tutorials`,
  `docs/explanation` and `docs/howto` is authoritative for released
  behaviour. `CHANGELOG.md` says which release added what, which is how
  to tell whether a feature is released. The design specification
  under `docs/project/design` and the decision records under
  `docs/project/adr` describe intended design: read them for intent,
  and never as evidence that a release behaves a certain way.

- `muructl <command> --help` from the installed release is the
  reference for flags. Try anything against the real release before it
  goes into a page (see `AGENTS.md` for how).

- Part I draws on: `README.md`; `docs/tutorials/first-wsgi-app.md`;
  `docs/explanation/architecture.md`, `process-models.md` and
  `preload.md`; and the how-to pages `daemon.md`, `traffic.md`,
  `rollouts.md`, `static-files.md`, `compression.md`, `file-hints.md`,
  `error-pages.md`, `asgi.md`, `mounts.md`, `starlette-and-fastapi.md`,
  `flask-and-django.md` and `managed-servers.md`.

- Unreleased work is on Muru's `develop` branch. Plan later
  collections from a checkout of it, but write no workshop against it:
  a workshop is written once its features are in a release, and the
  submodule and the pins move to that release first.

- For the other servers, their own documentation:
  [mod_wsgi](https://modwsgi.readthedocs.io/),
  [gunicorn](https://docs.gunicorn.org/) (its design, signals and
  deploying pages), [uvicorn](https://www.uvicorn.org/) (deployment),
  and [Granian](https://github.com/emmett-framework/granian). What a
  workshop says about them is kept to how they arrange processes and
  threads, who talks to clients, and what new code takes, and is
  checked against those pages.

Checked against 0.1.0a8 on CPython 3.14.8, macOS, on 2026-10-27, for
workshop 1:

- `muructl run` is one Rust process holding the edge and the
  controller. It starts a host, `python -m muru.host`, which imports
  the application and forks the workers, whose command line is the
  host's. Under the daemon, `muructl daemon run` is the parent of a
  separate edge (`muructl edge run`) and of each release's host.

- An exception in the application gives 500 with `reason=app_error`
  and the worker carries on. A worker that exits mid-request gives 502
  with `reason=worker_crashed` and a short plain text body naming the
  reason and the request id, and the host forks a replacement. The
  edge did not retry in 0.1.0a8 or 0.1.0a9. From 0.1.0a10 it sends a
  request to another worker when no worker has read it (the worker
  could not be connected to, or closed before the request head reached
  it), marked `retried` in the access log, and never sends again a
  request a worker has read, whatever its method. Workshop 1's POST to
  `/crash` is read before the worker exits, so it is still 502
  `worker_crashed` (checked on 0.1.0a10), and the quiz's explanation
  says when the edge does retry.

- Responses carry `server: muru` and `x-request-id`, and the environ
  carries `muru.request_id`. There is no `SERVER_SOFTWARE`.

- The application answers through jupyter-server-proxy at
  `<jupyter>/proxy/<port>/` and is not refused framing.

- `muructl run` starts the development dashboard on `127.0.0.1:8081`
  by default and says so in its last startup line. If that port is
  taken it prints `no dashboard: Address already in use` and serves the
  application all the same, so workshop 1 leaves the dashboard at its
  default and needs no variable for its port.

- The dashboard's pages use relative addresses (since 0.1.0a7), and
  every page, script, fragment and `v1/history` answers through
  `<jupyter>/proxy/<port>/`. Since 0.1.0a8 its pages send
  `frame-ancestors 'self'`, so a page of the same origin may frame
  them. Checked in Chrome: in an iframe inside JupyterLab at
  `<jupyter>/proxy/<port>/` the dashboard renders and its fragments
  refresh, while an iframe of `http://127.0.0.1:<port>/` is refused,
  because a different port is a different origin. A dashboard page
  therefore opens in a pane only under `:when: web_proxy`, and in a
  browser tab (no `:pane:`) under `not web_proxy`.

- `muructl run`'s dashboard needs no sign-in. The daemon's dashboard
  needs a session for every page, from a link that `muructl dashboard
  login --url <jupyter>/proxy/<port>/` prints under the proxied
  address, which workshops on the daemon have to provide.

Checked against 0.1.0a8 on CPython 3.14, macOS, on 2026-10-27, for
workshops 2 to 5:

- A dashboard port that is taken does not stop `muructl run`: it
  prints `no dashboard: Address already in use` and serves the
  application all the same.

- Flask (3.1.3) catches an exception in a view and answers with its
  own plain 500 page, so the access log line has no reason and the
  client sees no traceback. The page is Muru's only with
  `PROPAGATE_EXCEPTIONS = True`, which Muru's
  `docs/howto/flask-and-django.md` says since 0.1.0a9 (before, it said
  the page was always Muru's); workshop 2's `shop.py` sets it and says
  why. With it, the edge answers `reason=app_error`, with the
  traceback as HTML, as plain text, or as `application/problem+json`
  for `Accept: application/json`.

- Worker output is tagged `muru.worker[N].stdout:` for standard output
  and `muru.worker[N]:` for standard error, and `logging` arrives
  tagged with no configuration. Without `PYTHONUNBUFFERED`, printed
  lines sit in the worker's buffer; every manifest sets it.

- `--access-log errors` keeps 4xx, 5xx and requests slower than
  `--slow` (1s); the dashboard still has every request.

- `--reload` starts a new release (new host and workers) and switches
  once it is ready: 35 requests at ten a second across a reload, none
  failed. A syntax error gives `reload failed: ... release r2 keeps
  serving`, and the failed attempt uses up r3, so the fix is r4.

- `--https` with `MURU_CACHE_DIR` relative to the workspace writes
  `certs/dev.pem` there. mkcert is used when its authority is found;
  `CAROOT` naming an empty or missing directory makes the certificate
  self-signed even with mkcert installed. `curl --cacert dev.pem`
  trusts the self-signed certificate on macOS curl and on OpenSSL 3.5
  (checked with Python's `ssl`). Over TLS the environ has
  `SERVER_PROTOCOL` `HTTP/2.0`, `wsgi.url_scheme` `https` and
  `muru.tls` with `version` and `alpn`.

- The import check reports a connected UDP socket (`left a connected
  socket (fd 3, to 127.0.0.1:8125)`) and a thread (`left a thread
  running`), falls back under `auto` with `worker N imported ...`
  lines, and under `--preload true` exits with `preload is true, so
  the import check failing stops the release`. Hooks get a `Context`
  with `worker_id` (not `worker`); an exception in `post_fork` stops
  the worker, and after three failed starts the host gives up.

- A view that sleeps 0.1s and one that spends 0.1s of thread CPU time,
  40 requests eight at a time, medians from the JSON access log
  (10 CPUs): one process of one thread, both about 10 a second with
  `queue` about 700ms; one process of eight threads, `/wait` 74 a
  second with no queue, `/compute` 10 a second with no queue and `app`
  about 780ms; two processes of four, `/wait` 74, `/compute` 20 with
  `app` about 390ms.

- gunicorn (master): `--reload` restarts each worker on a change and
  is incompatible with `--preload`; a `SyntaxError` under reload makes
  the worker serve a 500 with the traceback (`util.make_fail_app`).
  No access log unless `--access-logfile`, default format the combined
  log; an exception is logged as `Error handling request`. uvicorn
  (master): `--reload` terminates and restarts the server process; an
  access log by default with no timing; an exception is logged as
  `Exception in ASGI application` and answered with plain text
  `Internal Server Error`; workers are started with multiprocessing's
  spawn.

Checked against 0.1.0a8 on CPython 3.14, macOS, on 2026-10-27, for
workshops 6 to 10:

- `muructl run` with no entrypoint reads `[tool.muru]` and its
  `[tool.muru.mounts.NAME]` tables, and says `using [tool.muru] from
  ./pyproject.toml`. Flask (3.1.3) at `/` sees `SCRIPT_NAME` empty;
  FastAPI (0.162.0) at `/api` sees `root_path` `/api` and the whole
  `path`, on the thread `muru-loop`, in the same worker processes. A
  WSGI thread's name is `Dummy-1`, so the workshop does not show it.
  The access log adds `mount=api`. A page in a pane at
  `<jupyter>/proxy/<port>/` opens a WebSocket to a relative `api/echo`
  and gets the echo (checked in Chrome).

- Checked again against 0.1.0a9. The startup lines add `muru.host[N]:
  mount api: api:app is served as ASGI`, the serving line ends `with 2
  workers of 4 threads and an event loop of concurrency 1000`, and
  `muru: mount api serves /api from api:app` follows it. A WebSocket
  has two access log lines with the same `id=`: `101 GET /api/echo 0B
  1.1ms queue=... app=... mount=api worker=1` when the application
  accepts it, and `101 GET /api/echo 42B 1.8ms websocket=closed
  by=client code=1000 received=1 sent=1 ...` when it closes, the time
  being how long it was open. (In 0.1.0a8 there was one line, written
  on close.) The development dashboard, through jupyter-server-proxy
  too (checked in Chrome), has a "WebSockets open" tile, a WebSockets
  table by endpoint and by socket (opened, open for, release, path,
  client, messages each way, worker, request id) shown only when one
  is open, and a chart of requests in flight and WebSockets open;
  `/v1/websockets` gives the same as JSON with `open` first. The "In
  flight" tile stays at 0 with sockets open, while the workers table's
  in-flight column counts them; the workshop names only the tile.

- With a WebSocket open, Ctrl-C on `muructl run` stops it in about
  0.3 seconds on 0.1.0a9 (`websocket_drain_grace` is 0s by default):
  the client gets close 1001 "the server is going away" and the log
  `websocket=closed by=edge code=1001`. Behind jupyter-server-proxy
  the browser sees 1005 instead, as the proxy does not pass the code
  on, so the page shows only "closed". In 0.1.0a8 the same stop took
  about ten seconds and sent no close frame.

- The daemon with `MURU_STATE_DIR`, `MURU_LOG_DIR`, `MURU_CACHE_DIR`
  and `MURU_CONFIG` relative to the working directory starts, deploys,
  writes each release's log there, and `muructl logs` reads it. A
  deploy without `--python` uses `python3` from the `PATH` the daemon
  was started with, the workshop's environment.

- Under four clients at about 150 requests a second, a deploy and a
  rollback left no request unanswered. A replaced release is
  `retained`, warm until 30 minutes later, with its host and one
  worker; `release list` still shows its configured `2x4`.

- `Muru-Preview` does not reach a held release on a daemon with no
  host or route declared: the request goes to the serving release. With
  a default host and one route applied, the header and the
  `muru_preview` cookie both reach it. The rollouts guide implies the
  first works too; to raise with Muru.

- `rollout canary --steps 10,50 --hold 10s --min-requests 20 --wait`
  promotes a good release in about 21 seconds, and rolls back one that
  fails one request in five during the 10% step within about 2
  seconds (`gate failed at 10%: 5xx rate 14.81% over the limit of
  1.00% (baseline 0.00%)`). `--wait` exits 0 either way.

- In an applied file, a release's `source` may be relative to the
  file, but `sendfile_roots` must be absolute and a static route's
  `static` directory is not resolved from the file's directory, so
  workshop 9 fills in absolute paths with `sed`. Static files get
  `ETag`, `Last-Modified`, `Cache-Control` from `cache`, 304 on
  `If-None-Match`, and the `.gz` beside the file for a gzip client
  (7417 bytes to 383); the access log says `reason=static`. JSON from
  the application is compressed with Brotli (4700 bytes to 190 in the
  trial). `X-Muru-Sendfile` within `sendfile_roots` is sent with static
  headers and ranges (206). An application's own 404 is not replaced by
  `error_pages` without `error_override`. Maintenance answers 503 with
  `Retry-After: 60` and the `503:maintenance` page, and static routes
  go on serving.

- A gunicorn (26.2.0) managed release deploys in under half a second,
  answers through the edge (`server: muru`) with `SERVER_SOFTWARE`
  `gunicorn/26.2.0`, lists as `1 gunicorn`, and runs as gunicorn's
  master and workers under the daemon. A native release of the same
  directory, held, canaried against it and promoted, then a rollback
  to gunicorn, left no request unanswered.

## Meet Muru

### Shape of the Meet Muru collection

**Where it fits (1).** The learner can say how Muru divides the work
of serving an application, and how that differs from the servers they
know.

**Developing with it (2 to 6).** The learner can run their own
application under `muructl run`, read what it reports, develop against
HTTPS and HTTP/2, rely on the import check before fork, size processes
and threads, and serve WSGI and ASGI from one server.

**Running it (7 to 10).** The learner can deploy releases to the
daemon without dropping a request, canary a release and watch it roll
back, let the edge do what nginx used to, and bring an existing
gunicorn deployment under Muru unchanged.

Each workshop is 20 to 30 minutes, six to nine pages including welcome
and finish, about four and a half hours in all. Each is self-contained:
it ships its own application and documents, installs its own
environment, and restates in a sentence anything an earlier workshop
showed.

### The Meet Muru workshops

### 1. `where-muru-fits`: Where Muru fits among Python web servers

Which process talks to clients, which runs your code, and what does
new code take, under the servers you know and under Muru?

The welcome page creates the environment (`muru` and `muructl`
0.1.0a10) and runs `muructl --version`. Page 2 opens
`docs/serving-python.md` in the viewer area: Apache with mod_wsgi
(embedded and daemon mode), nginx in front of gunicorn (arbiter,
workers that accept on the shared socket, `sync` and `gthread`,
`--preload`, HUP), uvicorn (event loop per worker, a supervisor that
spawns workers), and Granian (Rust threads and Python in each worker),
each with a Mermaid diagram, ending in a table of who talks to
clients, who runs the code, whether they are the same process, and
what new code takes. A quiz asks in which arrangement a process other
than the one running the code reads the request: mod_wsgi daemon mode.

Page 3 opens `docs/muru-processes.md` (edge, host, workers,
controller; `muructl run` as one Rust process with the edge and the
controller inside; the table again with a Muru row) and `hello.py`,
then starts `muructl run hello:application --port {{ app_port }}`
in the server terminal, leaving the startup line about the dashboard
to workshop 2. Page 4 shows the application
in a pane through jupyter-server-proxy, reads the access log line
field by field (`queue`, `app`, `worker`, `id`), and runs `curl -i` to
see `server: muru` and `x-request-id`. A quiz asks which process wrote
the access log line: the edge, since only it can measure `queue`.

Page 5 runs `show_processes.py`, which lists the `muructl` process,
the host and the worker with what each does. A text quiz asks how many
Python processes `--processes 3` gives (4: the host and three
workers), then the server is restarted that way and listed again.
Page 6 sends `GET /boom` (500, `reason=app_error`, the worker carries
on), asks what a client gets when its worker dies mid-POST (502 from
the edge), sends `POST /crash`, and lists the processes to show the
replacement forked from the same host. Page 7 opens `docs/releases.md`
(the daemon, a separate edge, releases side by side, blue/green,
canary, preview, rollback), runs `muructl run ... --print-config` to
show the development run as a release table, and stops the server.

- Format: two terminals and files, with a viewer area for the
  documents and the application. Ships `hello.py`,
  `show_processes.py`, `docs/serving-python.md`,
  `docs/muru-processes.md` and `docs/releases.md`.

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`; `curl` and `ps`.

- Source: `docs/explanation/architecture.md`,
  `docs/tutorials/first-wsgi-app.md`, `docs/howto/daemon.md`, and the
  other servers' documentation listed under Source material.

- Length: 25 minutes.

### 2. `what-muructl-run-tells-you`: Serve an app and read what it tells you

What does `muructl run` report while you develop, and where do you
look when something goes wrong?

The welcome page creates the environment (`muru`, `muructl`, Flask).
Page 2 opens `docs/where-output-goes.md` (gunicorn, uvicorn and
`muructl run` on requests, your output and failures, with Mermaid
diagrams and a table) and `shop.py`, a Flask application with a view
that prints, a slow report view that logs a warning, and a product
view that raises `KeyError` for product 9, with
`PROPAGATE_EXCEPTIONS` set and a comment saying why. It starts
`muructl run shop:app --port {{ app_port }} --dashboard
127.0.0.1:{{ dashboard_port }} --processes 2` and reads each startup
line. Page 3 asks for a product (the `.stdout` tagged line and the
access log line, field by field), quizzes how the report's logging
warning will be tagged (`muru.worker[N]:`, standard error), and asks
for the report (1.5s of `app`).

Page 4 opens product 9 in a pane (Muru's error page with the
traceback), fetches it as JSON through `python -m json.tool`, checks
for `"reason":"app_error"`, and quizzes what reason Flask's own 404
for `/nothing` gets in the log (none: a reason only appears on a
response Muru made). Page 5 restarts with `--access-log errors`,
quizzes how many lines the seven requests of `send_requests.py` give
(3: the 500, the 404 and the slow report), and runs it. Page 6 opens
the dashboard in a pane through the proxy (a browser tab without
one), sends five rounds, describes what it shows, and stops the shop.

- Format: two terminals and files, viewer area. Ships `shop.py`,
  `send_requests.py` and `docs/where-output-goes.md`.

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`, `flask==3.1.3`;
  `curl`. Variables `app_port` (8080) and `dashboard_port` (8081).

- Source: `docs/tutorials/first-wsgi-app.md`, `docs/howto/logging.md`,
  `docs/howto/dashboard.md`, `docs/howto/error-pages.md`,
  `docs/reference/errors.md`, `docs/howto/flask-and-django.md`.

- Length: 25 minutes.

### 3. `reload-and-https-in-development`: Reload, HTTPS and HTTP/2 on your laptop

How close to production can a development run be?

Page 2 opens `docs/reloading.md` (what gunicorn's, uvicorn's and
`muructl run`'s `--reload` replace, what requests get meanwhile, and
what a change that fails to import leaves serving, with diagrams and a
table) and `greeting.py`, whose first line carries `GREETING` and the
host's process id and whose second the scheme, protocol and
`muru.tls`. It starts `muructl run greeting:application --port
{{ app_port }} --reload`. Page 3 starts `watch.py`, which polls ten
times a second and stops a second after the first change, then
changes `GREETING` with an `editor-replace`: the terminal shows
`switched to release r2`, `watch.py` shows the new host and `0
failed`, and a check reads its `watch.log`.

Page 4 quizzes what requests get after saving a syntax error (the
previous release's answer; the wrong options are gunicorn's and
uvicorn's behaviour), drops the colon from the `def` line while
changing the greeting, shows `release r2 keeps serving` and the old
greeting, then puts the colon back and shows release r4. Page 5
restarts with `--https --https-port {{ https_port }}`, reads the
self-signed certificate line, curls over HTTP (`http`, HTTP/1.1),
quizzes which protocol arrives over HTTPS (HTTP/2.0), curls with
`--cacert muru-cache/certs/dev.pem`, greps curl's verbose output for
ALPN, explains why the pane cannot show it, and stops the server. The
manifest sets `MURU_CACHE_DIR` to `muru-cache` and `CAROOT` to a
missing directory under it, so the certificate stays in the workspace
and is self-signed on every machine.

- Format: two terminals and files, viewer area. Ships `greeting.py`,
  `watch.py` and `docs/reloading.md`.

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`; `curl`. Variables
  `app_port` (8080) and `https_port` (8443).

- Source: `docs/tutorials/first-wsgi-app.md`, `docs/howto/https.md`,
  gunicorn's `workers/base.py` and `config.py`, uvicorn's
  `supervisors/basereload.py`.

- Length: 20 minutes.

### 4. `import-once-fork-safely`: Import once, fork safely

What goes wrong when an application opens a connection at import time
and is then forked, and what does Muru do about it?

Page 2 opens `docs/preload-and-fork.md` (what a fork copies, shares
and loses, with a diagram; gunicorn `--preload` and its `post_fork`,
mod_wsgi daemon mode, uvicorn's spawned workers; Muru's check, its
three modes as a flow diagram and a table, and the hooks) and
`catalog.py`, which starts the metrics client in `metrics.py` at
import: a connected UDP socket to a statsd agent on 8125 and a thread
that sends the counts every five seconds and prints a line. A text
quiz asks how many threads the forked child will have (1), then
`fork_demo.py` imports the catalogue and forks with nothing in the
way: the child has only the main thread, and the same socket from the
same port. Python's fork `DeprecationWarning` shows because the fork
is in the script run.

Page 3 starts `muructl run catalog:application --processes 2` and
reads the `preload:` lines and the fallback, sends six requests, and
points at each worker's own sender reporting. Page 4 quizzes what
`--preload true` does (refuse to start) and shows it. Page 5 opens
`hooks.py` (`post_fork` starts the client), removes the start from
`catalog.py` with an `editor-replace`, starts with `--preload true
--hooks hooks`: no `preload:` lines, a `post_fork` line from each
worker, and their senders reporting from workers forked from a
preloaded host. It notes gunicorn's `post_fork(server, worker)` hook
and stops the server.

- Format: two terminals and files, viewer area. Ships `metrics.py`,
  `catalog.py`, `hooks.py`, `fork_demo.py` and
  `docs/preload-and-fork.md`.

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`; `curl`.

- Source: `docs/explanation/preload.md`, `muructl run --help`,
  gunicorn's `preload_app` setting, uvicorn's `_subprocess.py`.

- Length: 25 minutes.

### 5. `processes-threads-and-the-gil`: Processes, threads and the GIL

How many processes and threads should an application have, and why?

Page 2 opens `docs/processes-and-threads.md` (the GIL with a diagram;
a table of gunicorn `sync` and `gthread`, mod_wsgi daemon mode,
uvicorn, Granian and Muru; where Muru's requests wait, with a diagram;
reading `queue` against `app`; free-threaded Python) and `work.py`,
whose `/wait` sleeps 0.1s and `/compute` spends 0.1s of thread CPU
time. `load.py` sends 40 requests to each path, eight at a time, and
reads the edge's records from `--access-log requests.jsonl`, printing
the rate and the median total, `queue` and `app` times, after a line
with the CPUs it may use (allowing for a cgroup quota).

Page 3 runs one process of one thread: both views about 10 a second,
most of the time in `queue`. Page 4 quizzes what eight threads do to
`/compute` (the same rate, with the waiting moved from `queue` into
`app`), then shows it, with `/wait` about eight times faster. Page 5
quizzes what limits more processes (the CPUs), runs two processes of
four threads (`/compute` doubles where there are two CPUs; with one
it cannot), and stops the server. Free-threaded Python is described in
the document only: the workshop's environment is a regular 3.14, and
Binder has no free-threaded interpreter.

- Format: two terminals and files, viewer area. Ships `work.py`,
  `load.py` and `docs/processes-and-threads.md`.

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`; `curl`.

- Source: `docs/explanation/process-models.md`, gunicorn's design
  documentation, Granian's README, mod_wsgi's `WSGIDaemonProcess`
  defaults.

- Length: 30 minutes.

### 6. `wsgi-and-asgi-together`: WSGI and ASGI from one server

Can one server run a Flask application and a FastAPI application, with
WebSockets, side by side, and show what the sockets are doing?

Page 2 opens `docs/two-interfaces.md` (what gunicorn, uvicorn, Granian
and mod_wsgi each take, the two servers and proxy a mixed site usually
needs, with a diagram; mounts in one worker's threads and event loop,
with a diagram; the edge carrying WebSockets), then `pyproject.toml`,
whose `[tool.muru]` table has `web:app` as the default mount and
`api:app` as the mount `api` at `/api`, with two processes, and
`web.py` (Flask: a page at `/` whose script opens a WebSocket to
`api/echo` relative to itself, and `/about`) and `api.py` (FastAPI:
`/about` and the WebSocket `/echo`). It starts `muructl run --port
{{ app_port }} --dashboard 127.0.0.1:{{ dashboard_port }}` with no
entrypoint and reads the mount's startup lines. Page 3 curls Flask's `/about`
(`SCRIPT_NAME` empty), quizzes where FastAPI runs (the same workers,
on the event loop), and curls `/api/about` (thread `muru-loop`,
`root_path` `/api`), pointing at `mount=api` in the access log. Page 4
opens the page in a pane, where the WebSocket echoes through
jupyter-server-proxy, and points at its handshake line (`101`, written
when FastAPI accepts it), then runs `say.py`, whose socket opens and
closes at once, and reads its closing line (`websocket=closed
by=client code=1000 received=1 sent=1`, same `id=`). Page 5 runs
`listen.py` to hold five more sockets open, opens the dashboard in a
pane (a browser tab without jupyter-server-proxy), and reads the
"WebSockets open" tile (six), the WebSockets table and the chart,
noting that a socket is not a request in flight; stops `listen.py`
(five closing lines, the count back to one); quizzes what happens to
the page's socket when the site stops; and stops the site, which
closes it with `by=edge code=1001` at once.

- Format: two terminals and files, viewer area. Ships `pyproject.toml`,
  `web.py`, `api.py`, `say.py`, `listen.py` and
  `docs/two-interfaces.md`. Variables `app_port` (8080) and
  `dashboard_port` (8081).

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`, `flask==3.1.3`,
  `fastapi==0.162.0`, `websockets==17.3`; `curl`.

- Source: `docs/howto/mounts.md`, `docs/howto/starlette-and-fastapi.md`,
  `docs/howto/asgi.md`, `docs/howto/logging.md`,
  `docs/howto/dashboard.md`, `docs/howto/timeouts.md`,
  `docs/explanation/process-models.md`.

- Length: 25 minutes.

### 7. `deploying-without-downtime`: Deploy without dropping a request

What does a deploy look like when the new release starts beside the
old one?

Page 2 opens `docs/deploying.md` (gunicorn's `HUP` and, with
`--preload`, `USR2`; a mod_wsgi daemon restart; two deployments behind
a load balancer; the Muru daemon, with diagrams and a table), starts
`muructl daemon start --listen 127.0.0.1:{{ app_port }}`, shows the
503 with nothing deployed and `muructl daemon status`. Page 3 deploys
`releases/v1` (`greeter.py`, which names its release from
`muru.context()`, and a `pyproject.toml` with the entrypoint and two
processes) as `greeter`, and lists the releases. Page 4 starts
`traffic.py` in the left terminal (four clients without cookies,
counts every two seconds by the text after "Served by", errors and
requests with no answer), quizzes how many requests go unanswered (0),
deploys `releases/v2` and lists `r1` as retained. Page 5 rolls back,
stops the traffic and checks its totals in `traffic.log` for `no
answer: 0`. Page 6 runs `show_processes.py` (the daemon, the edge, each
release's host and workers), quizzes what `muructl daemon stop`
without `--shutdown` does to requests (nothing: the edge and hosts go
on serving), and shuts the daemon down.

- Format: two terminals and files, viewer area. Ships `releases/v1`,
  `releases/v2`, `traffic.py`, `show_processes.py` and
  `docs/deploying.md`.

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`; `curl`, `ps`.
  Variables `app_port` (8080) and `muru_run_dir` (`/tmp/muru-deploy`).

- Source: `docs/howto/daemon.md`, gunicorn's signals documentation.

- Length: 30 minutes.

### 8. `canary-a-release`: Canary a release and let it roll back

How do you try a new release on a share of the traffic, and back out
when it misbehaves?

Page 2 opens `docs/canary.md` (a canary built from two deployments and
weights; a rollout under the daemon: hold, preview, steps, gates
judged against the baseline, promotion and rollback), starts the
daemon, deploys `releases/v1` and applies `routes.toml` (a default host
and one route, which the previews need). Page 3 deploys `releases/v2`
with `--hold`, shows it held, and previews it with `Muru-Preview: r2`.
Page 4 starts `traffic.py` and runs `muructl rollout canary
greeter@r2 --steps 10,50 --hold 10s --min-requests 20 --wait`, about
20 seconds, then `rollout status` shows it promoted. Page 5 holds
`releases/v3` (one request in five is a 500), quizzes when its
rollout ends (in the 10% step, once it has 20 requests), runs the same
canary, which rolls back within seconds, shows the reason in `rollout
status` and `r3` kept warm, stops the traffic and shuts the daemon
down.

- Format: two terminals and files, viewer area. Ships `releases/v1`
  to `v3`, `routes.toml`, `traffic.py` and `docs/canary.md`.

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`; `curl`. Variables
  `app_port` (8080) and `muru_run_dir` (`/tmp/muru-canary`).

- Source: `docs/howto/rollouts.md`, `docs/howto/traffic.md`.

- Length: 30 minutes.

### 9. `what-nginx-was-for`: What you would have put nginx in front for

What does the edge do that a proxy in front of an application server
usually does?

Page 2 opens `docs/nginx-and-the-edge.md` (a typical nginx
configuration for the shop, and a table of what replaces each part)
and `site.toml.in`, writes `site.toml` with `sed` filling in the
absolute path of `site/`, starts the daemon and applies it: the
release of `site/app/shop.py` with `sendfile_roots`, `error_override`
for 404 with `html_only`, and `error_pages` for 404 and
`503:maintenance`; a default host; a static route at `/static/` with a
one-hour cache; a route to the application. Page 3 shows the style
sheet's headers, a conditional request answered 304, the precompressed
`app.css.gz` sent to a gzip client, quizzes which process sent it (the
edge) and shows `reason=static` in the access log. Page 4 compares the
catalogue's size with and without Brotli, opens `report()`, which
answers with `X-Muru-Sendfile`, and fetches the report and a range of
it (206). Page 5 shows the site's 404 page for HTML and the
application's for curl, turns maintenance on (503, `Retry-After` and
the maintenance page, static files still served) and off, and shuts
the daemon down.

- Format: two terminals and files, viewer area. Ships `site/` (the
  application, static files with a `.gz` variant, a report, two error
  pages), `site.toml.in` and `docs/nginx-and-the-edge.md`.

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`; `curl`, `sed`.
  Variables `app_port` (8080) and `muru_run_dir` (`/tmp/muru-edge`).

- Source: `docs/howto/static-files.md`, `compression.md`,
  `file-hints.md`, `error-pages.md`, `virtual-hosts.md`.

- Length: 30 minutes.

### 10. `bring-your-server-along`: Try Muru without changing your deployment

Can an existing gunicorn deployment move to Muru one step at a time?

Page 2 opens `docs/cutting-over.md` (a managed server release, a
native release canaried against it, and when to choose which server)
and `orders/orders.py`, whose responses name `SERVER_SOFTWARE` or
"Muru", starts the daemon and deploys `muructl deploy orders orders
--server gunicorn -- gunicorn --workers 2 --bind '{bind}'
orders:application`, shows gunicorn answering through the edge, the
release as `1 gunicorn`, the gunicorn master and workers under the
daemon, and applies `routes.toml`. Page 3 deploys the same directory
with `--entrypoint orders:application --processes 2 --hold` and
previews it. Page 4 canaries it against gunicorn under `traffic.py`
until it is promoted. Page 5 quizzes what a rollback to gunicorn does
(moves the traffic at once), rolls back, checks the traffic's totals
and shuts the daemon down. This is the one workshop that installs
another server.

- Format: two terminals and files, viewer area. Ships `orders/`,
  `routes.toml`, `traffic.py`, `show_processes.py` and
  `docs/cutting-over.md`.

- Requires: `muru==0.1.0a10`, `muructl==0.1.0a10`, `gunicorn==26.2.0`;
  `curl`, `ps`. Variables `app_port` (8080) and `muru_run_dir`
  (`/tmp/muru-server`).

- Source: `docs/howto/managed-servers.md`, `docs/howto/rollouts.md`.

- Length: 30 minutes.

### Topics the Meet Muru collection leaves out

- **Running the other servers to compare.** Installing gunicorn,
  uvicorn, Granian or mod_wsgi to show their process trees beside
  Muru's was considered and dropped: a description of their process and
  thread models, with a diagram, says what the comparison needs.
  Workshop 10 is the exception, for the reason given there.

- **Benchmarks.** Throughput figures depend on the machine, and a
  shared Binder container is no place to measure them.

- **systemd, service users, secrets and log rotation.** Linux and
  root only, so they belong to a collection on running Muru as a
  service.

- **Anything only on Muru's develop branch** until it is released:
  uploads, client classes and rate limits, overlays, gRPC mounts, scale
  to zero, profiling and the debugger.

## Naming

Directory names are kebab-case phrases naming the question a workshop
answers, not the mechanism, with no numeric prefix. Titles are sentence
case. Names are unique across the course. Collection ids are
`grahamdumpleton.me/muru/<collection>`, chosen once and never changed,
since a collection's id is its identity to subscribers and to
analytics.

Names taken: the ten in Part I above.

## Later collections

Candidates, not yet designed. Each goes into depth on one area, and
each waits until its features are released.

- **Developing with muructl run**: Flask, Django, Starlette and
  FastAPI; `[tool.muru]`; hooks and lifespan; reload; HTTPS; debugging
  with `--single`.

- **Running Muru as a service**: the daemon, deploy and releases,
  apply, export and diff, virtual hosts and TLS, behind a proxy,
  secrets, users, logs and rotation, `daemon upgrade`, systemd.

- **Releases and traffic**: blue/green, canaries and their gates,
  bucketing, sticky sessions, previews, A/B cohorts, maintenance mode.

- **What the edge does for you**: static files, compression, file
  hints, internal redirects, error pages, authentication sub-requests,
  upstreams, connection limits, uploads, client classes, rate limits
  and overlays.

- **Sizing and keeping workers healthy**: process models, the GIL and
  free-threading, worker groups, timeouts, recycling, memory limits,
  the autoscaler, scale to zero, schedules and node budgets.

- **Seeing inside a running service**: the access log, metrics,
  events and webhooks, the dashboard, and `muructl debug` with
  profiling, tracing, memory and the debugger.

- **Moving an existing application to Muru**: from gunicorn, uvicorn,
  Granian and mod_wsgi, with managed server releases and a mapping of
  settings. Muru's own migration guides are still to be written
  (none in 0.1.0a10).

- **WSGI, ASGI and gRPC together**: mounts, WebSockets, gRPC mounts, and
  handing requests across between WSGI and ASGI once that is released
  (not in 0.1.0a10).

## Decisions that cut across the workshops

**JupyterLab only, Python 3.14.** The workshops run servers and
terminals, which JupyterLite cannot. Python 3.14 is what Binder and the
Codespaces image provide; 3.15 is acceptable where a workshop needs it
and the hosts have it.

**Muru is installed per workshop, pinned.** Each workshop declares an
`environment` whose `requirements.txt` pins `muru` and `muructl` to the
release in `reference/muru`, written the PyPI way (`0.1.0a10`). An exact
pin needs no `--pre`. The extension puts the environment first on
`PATH` in the terminals, so `muructl` finds the environment's Python
with no activation step. No workshop step uses uv or `uv tool install`:
uv is not on Binder, and nothing is installed under the home directory.
The README tells learners to `uv tool install muructl` afterwards, as
Muru's own documentation does.

**Released features only.** A workshop uses only what is in the release
it pins. The pin, the submodule and every workshop's requirements move
together, with `just bump-muru` and a full `just test-all`.

**The format is two terminals and files, with a viewer area.** The
layout `tour` puts a named area, `viewer`, above two terminals side by
side: `server` on the left for the long-running command, `client` on
the right for requests and inspection. Documents, shipped files and
the application's pane open in the viewer area.

**Comparisons are prose and diagrams.** Where it helps, a workshop
ships Markdown documents under `files/docs/`, each with Mermaid
diagrams, and opens them with `file-open` and `:factory: Markdown
Preview` in the viewer area, where there is room to read them. The
instructions say what to look for and stay short. Other servers are
described, never installed, except in workshop 10.

**Learners never type code.** Every command and file change arrives
through an action. Shipped helpers such as `show_processes.py` do the
inspecting, so the commands on the page stay short.

**Ports are variables.** `app_port` (default 8080) for HTTP, and in
later workshops `https_port` (8443) and `dashboard_port` (8081), Muru's
own defaults. A hint on the page that starts a server says how to
change the port from the Variables dialog if it is taken. Servers bind
`127.0.0.1` only, and are stopped before the finish page.

**Progress is reported from Binder and Codespaces.** Both report
anonymous progress events to the workshops' own analytics service,
`https://workshop-analytics.grumpys.work/events`, the one the wrapt
workshops use, so it can be seen where a workshop loses people. The
sink and one ingest token are declared once, in `collection.yaml` at
the root of the repository, which `just index` copies into every
collection index; each deployment's settings only turn reporting on
with `report: always`. One token serves every collection and every
deployment: the collection is identified by the `id` in its index,
which every event carries, and the host and frontend say where the
event came from. The token is public by construction, since the
indexes are. Each welcome message tells the visitor that progress is
reported and what is never sent. Someone who subscribes from their own
JupyterLab is offered the same sink as a checkbox in the trust dialog,
off unless ticked.

**Showing a server in a pane.** Through jupyter-server-proxy at
`{{ jupyter_url }}proxy/{{ app_port }}/` under `:when: web_proxy`, with
a loopback `url-open` under `not web_proxy`. jupyter-server-proxy is a
runtime dependency in `pyproject.toml`, so it is on Binder, in
Codespaces and in a local `just lab`. HTTPS cannot be shown in a pane
through the proxy, so HTTPS and HTTP/2 are shown with curl.

**Daemon state stays in the workspace; its sockets do not.** A
workshop that runs the daemon sets `MURU_STATE_DIR`, `MURU_LOG_DIR`,
`MURU_CACHE_DIR` and `MURU_CONFIG` to paths relative to the workspace
(`muru/state` and so on) in its manifest `env`, which works because
every terminal and check runs there. The run directory cannot follow:
it must be absolute, since a release's host runs elsewhere, and short,
since a socket's path is limited to about a hundred bytes (104 on
macOS), and a workspace inside a checkout is too deep. So each such
workshop declares a variable `muru_run_dir`, exported to terminals and
checks as `MURU_RUN_DIR`, defaulting to `/tmp/muru-<word>` (`deploy`,
`canary`, `edge`, `server`), which the learner can change. A fixed
directory of the workshop's own also keeps it apart from a daemon the
learner runs, whose default on macOS is `/tmp/muru-UID`. The daemon is
started in the background with `muructl daemon start --listen
127.0.0.1:{{ app_port }}`, and stopped with `muructl daemon stop
--shutdown` before the finish page; the run directory's few small
files stay behind in `/tmp`.

**Prediction before execution, sparingly.** The audience is
experienced, so a quiz appears only where predicting the result teaches
something: a count, which process did something, what a client gets.
Never on what the page has just said.

**Checks guard what the next step needs.** A `verify` follows a step a
later page depends on, such as a server that must be up, usually a
`shell` check with curl or a shipped helper, shaped to one line on
success.

**Platforms.** `linux` and `macos`, as Muru's wheels are. Commands are
POSIX and `ps` is called with POSIX options (`-e -o pid=,ppid=,args=`)
so they work on both.

**Done** means lint is clean, `just test <name>` is green, the
workshop is in the index and the README, and its entry here is true.

## Extension features the workshops use

- `environment` with `requirements.txt`, created by `environment-create`
  as the first step of the welcome page; terminals, captures and checks
  get it on `PATH`.

- The `tour` layout: `{ name: viewer, tabs: [] }` as the placeholder
  above `terminal:server` and `terminal:client` in columns. Workshop 1
  settled it.

- `file-open` with `:factory: Markdown Preview` and `:area: viewer` for
  the documents. JupyterLab renders Mermaid blocks in the preview.

- `url-open` with `:pane: app` and `:area: viewer`, in the
  `web_proxy` pair described above, with the `web-proxy` capability.
  Sending the pane the same URL again reloads it, which is how a page
  shows a different worker answering.

- `execute` with `:wait: 3s` to start a server, `interrupt` to stop it,
  and a new `execute` with its own id to start it again.

- `editor-replace` with `:match:`, and with `:regex: true` for an edit
  across lines, to change shipped code: the greeting and the syntax
  error in workshop 3, moving the metrics start into a hook in
  workshop 4. The `write-files` capability comes with it.

- `url-open` without `:pane:` for the dashboard where there is no
  proxy, since its own loopback address is another origin and cannot
  be framed.

- Manifest `env` for settings every command needs, such as
  `MURU_CACHE_DIR` and `CAROOT` in workshop 3, with paths relative to
  the workspace.

- A `shell` check that waits for a file a helper writes, up to ten
  seconds, where the helper outlasts the check's settle time
  (`watch.log` in workshop 3).

- `shell` checks with output shaped as the style guide gives:
  `out=$(...); printf '%s\n' "$out" | tail -n 1 | grep ... || { printf
  '%s\n' "$out"; exit 1; }`.

## Known blockers

- **The daemon's sockets need a short run directory.** A release's
  worker sockets are `RUN/apps/APP/RID/RID/worker-N.sock`, about 31
  bytes plus the application's name below the run directory, and a
  path past the platform's limit (104 bytes on macOS, 108 on Linux)
  stops the edge or the release ("path must be shorter than SUN_LEN").
  `muructl daemon start` then waits its full 30 seconds before saying
  the daemon did not answer. A relative run directory lets the daemon
  start but not a release, whose workers never come up. Worked around
  with `muru_run_dir` under `/tmp`; see the decision on daemon state.

- **The course scaffold's welcome messages repeat the description.**
  `course init` in jupyterlab-workshop 0.30.0 writes "workshops: Guided
  JupyterLab workshops on ..." into both welcome messages and
  `AGENTS.md`. Fixed by hand here.

## Open questions

- **The analytics ingest token** is borrowed for now: `collection.yaml`
  holds the wrapture workshops' token (`sub` `wrapture-workshops`,
  expiring 2027-09-21), since the events are told apart by the
  collection id anyway. Issue one of this course's own with
  `workshop-analytics token issue --name muru-workshops --expires
  <date>`, put it in `collection.yaml` and run `just index`.

## Status

Workshops are written in collection order. Workshop 1 was written
first, on its own, to settle the format before the rest. Workshops 2
to 5 followed together, against 0.1.0a8, and then 6 to 10. All ten were
self-tested again against 0.1.0a9 when it was pinned, and workshop 6
was rewritten for its WebSocket logging and dashboard. All ten passed
their self-tests again on 0.1.0a10, which needed no change to any
workshop beyond the pin and workshop 1's note on retries.

### Meet Muru

| Workshop | Status |
| -------- | ------ |
| 1. `where-muru-fits` | Done |
| 2. `what-muructl-run-tells-you` | Done |
| 3. `reload-and-https-in-development` | Done |
| 4. `import-once-fork-safely` | Done |
| 5. `processes-threads-and-the-gil` | Done |
| 6. `wsgi-and-asgi-together` | Done |
| 7. `deploying-without-downtime` | Done |
| 8. `canary-a-release` | Done |
| 9. `what-nginx-was-for` | Done |
| 10. `bring-your-server-along` | Done |

Planned: designed in the outline, not yet written. Written: the pages
exist and lint is clean. Done: `just test <name>` is green, and the
workshop is in the index and the README.

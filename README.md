# Muru workshops

[![Launch on Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GrahamDumpleton/muru-workshops/main?urlpath=lab)
[![Open in GitHub Codespaces](https://img.shields.io/badge/launch-codespaces-579ACA?logo=github&logoColor=white)](https://codespaces.new/GrahamDumpleton/muru-workshops?quickstart=1)
[![test](https://github.com/GrahamDumpleton/muru-workshops/actions/workflows/test.yml/badge.svg)](https://github.com/GrahamDumpleton/muru-workshops/actions/workflows/test.yml)

Nothing to install: start the workshops on [mybinder.org](https://mybinder.org/v2/gh/GrahamDumpleton/muru-workshops/main?urlpath=lab) with no account, or in [GitHub Codespaces](https://codespaces.new/GrahamDumpleton/muru-workshops?quickstart=1) with a GitHub account.

Guided JupyterLab workshops on [Muru](https://github.com/GrahamDumpleton/muru),
a routing edge, control plane and Python runtime for serving WSGI and
ASGI applications, with zero-downtime releases, traffic management and
Python-aware process management. They are for Python web developers who
have deployed an application with Apache and mod_wsgi, gunicorn,
uvicorn or Granian, and want to see what Muru does differently and how
to use it.

The workshops run on
[jupyterlab-workshop](https://github.com/GrahamDumpleton/jupyterlab-workshop),
a JupyterLab extension that shows the instructions in a side panel with
clickable actions that drive the session, and checks what you have done
as you go. Each workshop is a directory of a `workshop.yaml` manifest
and Markdown pages. See [OUTLINE.md](OUTLINE.md) for the design of the
course.

## The collections

Each collection is a part of the course: its workshops are numbered in
the order to take them, and the Finish dialog of each offers the next.
A [catalog](catalog.json) names every collection, so one URL offers them
all.

### Meet Muru

Where Muru fits among Python web servers, what it does while you
develop, and how its daemon deploys releases without downtime, compared
throughout with Apache and mod_wsgi, gunicorn, uvicorn and Granian.
Each workshop installs Muru 0.1.0a10 into an environment of its own and
runs it in two terminals, with documents and the application shown
above them. Workshops 7 to 10 run the daemon, which keeps its state
in the workspace and its sockets in a short directory under `/tmp`.

1. **Where Muru fits among Python web servers** (`where-muru-fits`, 25
   minutes). How Apache with mod_wsgi, gunicorn, uvicorn and Granian
   divide the work of serving an application, in short documents with
   diagrams, then a small WSGI application under `muructl run`, the
   edge, host and worker processes that serve it, and what happens when
   a request or a worker fails.

2. **Serve an app and read what it tells you**
   (`what-muructl-run-tells-you`, 25 minutes). A Flask application
   under `muructl run`: the startup lines, the access log and its
   errors-only mode, output tagged by worker, the error page with the
   traceback for a browser and as a problem document for an API
   client, and the dashboard, compared with what gunicorn and uvicorn
   report.

3. **Reload, HTTPS and HTTP/2 on your laptop**
   (`reload-and-https-in-development`, 20 minutes). What `--reload`
   replaces under gunicorn, uvicorn and Muru, a reload with no request
   refused and a syntax error that leaves the previous release serving,
   then HTTPS with a development certificate and HTTP/2 over TLS.

4. **Import once, fork safely** (`import-once-fork-safely`, 25
   minutes). What a fork leaves behind when an application opens a
   socket and starts a thread at import, how Muru's import check finds
   both and falls back or refuses to start, and a `post_fork` hook
   that lets the workers be forked from a preloaded host again.

5. **Processes, threads and the GIL**
   (`processes-threads-and-the-gil`, 30 minutes). Other servers'
   process and thread settings mapped onto Muru's, then a view that
   waits and a view that computes measured under one thread, eight
   threads and two processes, read from the edge's queue and app
   times.

6. **WSGI and ASGI from one server** (`wsgi-and-asgi-together`, 25
   minutes). A Flask application at `/` and a FastAPI application at
   `/api` as mounts of one release, in the same worker processes, the
   prefix each one sees, and WebSockets from a browser pane and the
   terminal, with each socket's two access log lines and the sockets
   open on the dashboard.

7. **Deploy without dropping a request**
   (`deploying-without-downtime`, 30 minutes). The daemon, a deploy
   and an instant rollback under a steady stream of requests with none
   unanswered, and the daemon, edge, hosts and workers behind them,
   compared with gunicorn's `HUP`, a mod_wsgi restart and two
   deployments behind a load balancer.

8. **Canary a release and let it roll back** (`canary-a-release`, 30
   minutes). A held release previewed by header, a canary through 10%
   and 50% that is promoted, and a release with a bug whose error rate
   gate rolls it back on its own.

9. **What you would have put nginx in front for**
   (`what-nginx-was-for`, 30 minutes). Static files, precompressed
   variants, compression, a file the application names, the site's own
   error pages and maintenance mode, from one configuration file,
   beside the nginx configuration each replaces.

10. **Try Muru without changing your deployment**
    (`bring-your-server-along`, 30 minutes). An existing gunicorn
    command run unchanged under the daemon, Muru's own workers held
    beside it and given the traffic by a canary, and an instant
    rollback to gunicorn.

## Run locally

With [uv](https://docs.astral.sh/uv/) installed, from a checkout:

```
uv sync --no-dev
uv run jupyter lab --config=jupyter_lab_config.py
```

or `just lab`. Without cloning, `uvx --from "jupyterlab-workshop[lab]"
jupyter-workshop launch --catalog <raw catalog URL>` runs the course in
a directory of its own; add `--with jupyter-server-proxy` to the `uvx`
command so the workshops can show the application in a pane.

The workshops run on Linux and macOS, which Muru has wheels for, and
serve on port 8080 unless you change the port in a workshop's Variables
dialog.

To use Muru for your own applications afterwards, install the command
once with `uv tool install muructl`, and add the runtime library to
each application's environment with `uv add muru`.

## Subscribe from your own JupyterLab

In a JupyterLab with the extension installed, subscribe to the catalog
or to one collection from the workshop browser's Collections dialog:

```
https://raw.githubusercontent.com/GrahamDumpleton/muru-workshops/main/catalog.json
https://raw.githubusercontent.com/GrahamDumpleton/muru-workshops/main/collections/introduction/collection.json
```

## What is in the repository

```
AGENTS.md                guidance for agents writing workshops here
OUTLINE.md               the design of the course
Justfile                 every common task, and the order of each collection
pyproject.toml           the uv project: JupyterLab, jupyter-server-proxy and the pinned extension
catalog.json             names every collection, written by `just index`
collection.yaml          the analytics block `just index` copies into every collection index
collections/<name>/      one collection index per part of the course
workshops/<name>/        one workshop each, every collection's side by side
reference/muru           Muru at the release the workshops teach (submodule)
reference/jupyterlab-workshop
                         the extension at the pinned release (submodule)
binder/                  the Binder image: runtime, requirements, settings, welcome
.devcontainer/           the Codespaces container
.github/workflows/       lint and self-test on each push
course.json              what `jupyter workshop course init` wrote, for `course update`
```

## Writing and checking workshops

`just install` sets up the environment, fetches the reference
checkouts and links the authoring skill; `just new <name>` scaffolds a
workshop under `workshops/`; `just lint` and `just test <name>` check
it; `just index` writes the collection indexes and the catalog in the
order the Justfile gives.

## Updating the releases

`just bump <version>` moves to a new release of the extension,
refreshes the files the scaffold wrote and moves its reference
checkout. `just bump-muru <tag>` moves `reference/muru` to a Muru
release tag, such as `v0.1.0-alpha.11`; then update `muru` and `muructl`
in every `workshops/*/requirements.txt` to the same release and run
`just test-all`.

---
title: How Python apps are usually served
requires: [quiz:who-reads-the-request]
---

# How Python apps are usually served

Every Python web server answers the same few questions differently:
which process talks to clients, which process runs your code, how many
of each there are, and what has to happen before new code is served.
Open the first document, which goes through four common arrangements
with a diagram of each.

```{file-open}
:title: Open the document on how Python apps are served
:path: docs/serving-python.md
:factory: Markdown Preview
:area: viewer
```

Read it through to the table at the end. Two things to notice as you
go. In most of the arrangements, the process that parses a client's
request is the same one that runs your code. And in all of them, new
code is served by replacing the processes that run the old code.

```{quiz}
:id: who-reads-the-request
question: In which of these does a process other than the one running your code read the request from the client connection?
options:
  - { text: "gunicorn with the `gthread` worker class, without nginx", explanation: "Each gunicorn worker accepts connections on the shared socket and parses the HTTP itself, in the same process its threads run your code in." }
  - { text: "uvicorn with `--workers 4`", explanation: "The supervisor only starts the workers. Each worker's event loop reads the requests and runs your code in the same process." }
  - { text: "Apache with mod_wsgi in daemon mode", correct: true }
  - { text: "Granian with `--workers 4`", explanation: "Granian parses HTTP in Rust threads, but those threads live in the worker process that also runs your Python." }
explanation: "In daemon mode an Apache child process reads the request and passes it over a UNIX socket to a mod_wsgi daemon process, which runs your code. Muru splits the work the same way, between processes with different jobs."
```

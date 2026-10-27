---
title: What a fork leaves behind
requires: [quiz:threads-after-fork]
---

# What a fork leaves behind

Open the document on importing once and then forking. Read the first
part, up to "How servers handle it", for what a fork copies and what
it does not.

```{file-open}
:title: Open the document on importing once, then forking
:path: docs/preload-and-fork.md
:factory: Markdown Preview
:area: viewer
```

Now look at the catalogue. As soon as it is imported, it starts the
metrics client, which opens a UDP socket to a metrics agent and starts
a thread that sends the counts every five seconds. Code like this is
everywhere: metrics clients, connection pools and schedulers often
start this way.

```{file-open}
:title: Open catalog.py
:path: catalog.py
:area: viewer
```

`fork_demo.py` does what a preforking server does, with nothing in the
way: it imports the catalogue, then forks a child, and prints the
threads and the metrics socket in each.

```{quiz}
:id: threads-after-fork
:type: text
question: The process that imported the catalogue has two threads, the main thread and the metrics sender. How many threads will the forked child have?
answer: "1"
wrong:
  - { text: "2", explanation: "A fork copies the memory of the process, but only the thread that called fork goes on running in the child." }
  - { text: "0", explanation: "The thread that called fork goes on running in the child. Only the others are missing." }
otherwise: "Think about which thread called fork."
explanation: "Only the thread that called fork exists in the child. The metrics sender is gone, so the counts the child makes are never sent, and nothing says so."
```

```{execute}
:id: run-fork-demo
:session: client
:wait: prompt
python fork_demo.py
```

The child has the main thread alone: no metrics sender. And its
metrics socket is the same socket as the parent's, from the same port,
not a copy. With a database connection in its place, every worker
would be talking over one connection at once.

Python noticed too: the `DeprecationWarning` about forking a
multi-threaded process appears here because the fork is in the script
you ran. Inside a server's own code you would never see it.

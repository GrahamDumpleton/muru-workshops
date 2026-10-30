---
title: Reopening logs
requires: [verify:signal-sent]
---

# Reopening logs

`on_reopen_logs` runs in a worker that receives `SIGUSR1`. It is for a
log file the application opened itself, such as one a `logging` file
handler writes: once the file has been renamed by log rotation, the
handler has to open it again by name. Under the daemon, `muructl logs
reopen --workers` sends the signal to every worker.

`reopen.py` asks the application which worker answers, and sends that
worker `SIGUSR1`.

```{execute}
:id: send-signal
:session: client
:wait: prompt
python reopen.py {{ app_port }}
```

```{verify}
:id: signal-sent
:label: A worker was sent SIGUSR1
:substrate: shell
:trigger: after:send-signal
out=$(curl -s --max-time 2 http://127.0.0.1:{{ app_port }}/); case "$out" in *"worker process"*) echo "The application still answers: $out";; *) echo "${out:-Nothing answers on port {{ app_port }}.}"; exit 1;; esac
```

In the terminal on the left, `hook on_reopen_logs` ran in one worker,
the one with the process id `reopen.py` printed. The other worker had
no signal and ran nothing, and both go on serving.

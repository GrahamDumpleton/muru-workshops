---
title: Only what needs attention
requires: [verify:errors-only-up, quiz:lines-logged]
---

# Only what needs attention

A line for every request is a lot once a page loads its styles,
scripts and images. `--access-log errors` keeps only the lines worth
reading: responses with a 4xx or 5xx status, and requests slower than
`--slow`, which is one second unless you say otherwise. Your code's
output and tracebacks still come through as before.

Stop the shop, then start it again that way.

```{interrupt}
:id: stop-for-errors
:session: server
```

```{execute}
:id: start-errors-only
:session: server
:wait: 3s
muructl run shop:app --port {{ app_port }} --dashboard 127.0.0.1:{{ dashboard_port }} --processes 2 --access-log errors
```

```{verify}
:id: errors-only-up
:label: The shop answers on port {{ app_port }}
:substrate: shell
:trigger: after:start-errors-only
curl -sS --max-time 2 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:{{ app_port }}/
```

`send_requests.py` in your workspace sends seven requests, one after
another: the home page, products 1, 2 and 3, product 9, `/nothing`,
and the slow report.

```{quiz}
:id: lines-logged
:type: text
question: How many access log lines will those seven requests give with `--access-log errors`?
answer: "3"
wrong:
  - { text: "2", explanation: "Product 9 and `/nothing` fail, but the report takes 1.5 seconds, which is slower than `--slow`." }
  - { text: "7", explanation: "That is every request. Only failures and slow requests are kept." }
otherwise: "Count the responses with a 4xx or 5xx status, then the requests that take longer than a second."
explanation: "Product 9 (500), `/nothing` (404) and the report, which takes 1.5 seconds and so counts as slow. The four quick successful requests leave no line."
```

```{execute}
:id: send-mix
:session: client
:wait: prompt
python send_requests.py {{ app_port }}
```

The last line in the terminal on the right counts the responses. In
the terminal on the left there are three access log lines, with the
products' printed lines, the traceback and the report's warning around
them.

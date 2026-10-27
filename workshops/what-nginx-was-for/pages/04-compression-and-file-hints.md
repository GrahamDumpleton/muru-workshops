---
title: Compression and file hints
requires: [verify:report-range]
---

# Compression and file hints

The application's catalogue at `/` is JSON. Compare its size as the
application wrote it with what a client that accepts Brotli receives.

```{execute}
:id: catalogue-sizes
:session: client
:wait: prompt
curl -s -o /dev/null -w '%{size_download} bytes as written\n' http://127.0.0.1:{{ app_port }}/; curl -s -o /dev/null -w '%{size_download} bytes compressed\n' -H 'Accept-Encoding: br' http://127.0.0.1:{{ app_port }}/
```

The edge compressed it, after the worker had finished with it, so the
application spent no time on it. Text, JSON, JavaScript, XML and SVG
are compressed by default, with Brotli, zstd or gzip, whichever the
client prefers, where nginx needs `gzip on` and `gzip_types`.

Some files should go only to clients the application lets have them,
such as a report. Open the application and look at `report()`.

```{file-open}
:title: Open site/app/shop.py
:path: site/app/shop.py
:area: viewer
:line: 32
```

It answers with an empty body and an `X-Muru-Sendfile` header naming
the file. The edge sends the file in its place, as nginx does with
`X-Accel-Redirect`, but only from the directories the release's
`sendfile_roots` lists, here `site/reports`.

```{execute}
:id: get-report
:session: client
:wait: prompt
curl -s -i http://127.0.0.1:{{ app_port }}/report
```

The response has the file, with the application's `Content-Type` and
the static file headers, `ETag`, `Last-Modified` and `Accept-Ranges`.
The `X-Muru-Sendfile` header never reaches the client. And since the
edge sends it as a static file, a range works too.

```{execute}
:id: get-report-range
:session: client
:wait: prompt
curl -s -i -H 'Range: bytes=0-31' http://127.0.0.1:{{ app_port }}/report
```

```{verify}
:id: report-range
:label: The edge answers a range of the report with 206
:substrate: shell
:trigger: after:get-report-range
curl -s -o /dev/null -w '%{http_code}\n' -H 'Range: bytes=0-31' http://127.0.0.1:{{ app_port }}/report | grep '^206$'
```

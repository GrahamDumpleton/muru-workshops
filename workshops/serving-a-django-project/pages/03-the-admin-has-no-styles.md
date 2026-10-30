---
title: The admin has no styles
requires: [quiz:who-serves-static, verify:static-served]
---

# The admin has no styles

Open the admin's sign-in page. Under `runserver` it would be styled,
since `DEBUG` is on.

```{url-open}
:title: Open the admin
:when: web_proxy
:url: {{ jupyter_url }}proxy/{{ app_port }}/admin/login/
:pane: site
:area: viewer
```

```{url-open}
:title: Open the admin
:when: not web_proxy
:url: http://127.0.0.1:{{ app_port }}/admin/login/
```

```{quiz}
:id: who-serves-static
question: The page asks for `/static/admin/css/base.css`, with `DEBUG = True` and `django.contrib.staticfiles` installed. Who answers under `muructl run`?
options:
  - { text: "Nobody serves it: Django's URLs have no route for it, and the answer is 404", correct: true }
  - { text: "django.contrib.staticfiles, as under runserver", explanation: "The app serves files under runserver through a handler that runserver wraps around the application. Other servers do not have it." }
  - { text: "Muru's edge, which serves STATIC_URL from each app's static directory", explanation: "The edge serves only the directories a project's [[tool.muru.static]] entries or the daemon's routes declare, and this project declares none; the admin's files are in Django's own package anyway, until collectstatic gathers them." }
explanation: "Only runserver adds the static files handler. Under any other server the request reaches Django's URL configuration, which has no route for /static/."
```

The page is plain text and links, and in the terminal on the left the
stylesheets are `404 GET /static/admin/css/...`, each with `Not Found`
logged by Django. The document's section on static files has the ways
to serve them; in development, the project's own URLs can, with
`staticfiles_urlpatterns()`. Add it to `mysite/mysite/urls.py`.

```{editor-insert}
:id: import-static
:title: Import staticfiles_urlpatterns in mysite/mysite/urls.py
:path: mysite/mysite/urls.py
:match: from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
```

```{file-write}
:id: add-static
:title: Add the static files to urlpatterns
:path: mysite/mysite/urls.py
:mode: append
:open: true
:area: viewer


# Development only: serve every installed app's static files while
# DEBUG is on. In production something in front serves STATIC_ROOT.
# The prefix is the path as Django sees it: left out, it would be
# STATIC_URL with a proxy's path prefix added, which never matches.
urlpatterns += staticfiles_urlpatterns("/static/")
```

In the terminal on the left, `--reload` saw `urls.py` change, started
a new release with it and switched to it. Load the admin again.

```{url-open}
:title: Load the admin again
:when: web_proxy
:url: {{ jupyter_url }}proxy/{{ app_port }}/admin/login/
:pane: site
:area: viewer
```

```{url-open}
:title: Load the admin again
:when: not web_proxy
:url: http://127.0.0.1:{{ app_port }}/admin/login/
```

```{verify}
:id: static-served
:label: The admin's stylesheet is served
:substrate: shell
:trigger: after:add-static
for i in 1 2 3 4 5 6 7 8 9 10; do code=$(curl -s -o /dev/null --max-time 2 -w '%{http_code}' http://127.0.0.1:{{ app_port }}/static/admin/css/base.css); [ "$code" = 200 ] && { echo "The admin's stylesheet is served."; exit 0; }; sleep 1; done; echo "/static/admin/css/base.css still answers $code. Check that urls.py has both changes and that the terminal on the left switched to a new release."; exit 1
```

The admin is styled, and the stylesheets are `200` in the access log,
each with a `worker=`: a Django view in a worker read the file and
sent it. That is fine while you develop, and `staticfiles_urlpatterns()`
adds nothing once `DEBUG` is off. In production, `collectstatic`
gathers the files into `STATIC_ROOT`, and a `[[tool.muru.static]]`
entry in the project naming that directory under `/static/` has the
edge serve them without a worker, under `muructl run` and the daemon
alike, as Muru's Django tutorial shows.

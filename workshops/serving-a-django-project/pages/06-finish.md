---
title: Finish
---

# Finish

You have served a Django project under `muructl run`.

- `wsgi.py` and `asgi.py` are ready for Muru as `startproject` wrote
  them. The host imported the project once, settings, apps and models,
  and forked the workers from it.

- Only `runserver` serves static files on its own. Under any other
  server, `staticfiles_urlpatterns()` serves them while `DEBUG` is on,
  and in production a `[[tool.muru.static]]` entry in the project has
  the edge serve `STATIC_ROOT`.

- Django answers a failing view with its debug page, or its
  `handler500`; `DEBUG_PROPAGATE_EXCEPTIONS` hands the exception to
  Muru, whose page and `reason=app_error` are the same for every
  project.

- Over `asgi.py`, async views run on the worker's event loop and sync
  views on Django's threads; over `wsgi.py` it is the reverse.

Click Finish below for where to go next.

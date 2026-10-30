---
title: Welcome
requires: [verify:muructl-installed]
---

# Welcome

`muructl run --reload` and `--https` work out of the box for a project
of Python files served on `localhost`. A real project has templates
and data files, writes files of its own, and is reached under other
names. This workshop fits both options to such a project, and along
the way compares them with gunicorn's and uvicorn's.

The project, a menu of the day in the `menu` directory of your
workspace, is already there. Nothing you do here needs you to type
code.

This workshop has an environment of its own with `muru`, `muructl` and
`trustme` installed, at Muru release 0.1.0a11. Create it first; it
takes a minute.

```{environment-create}
:title: Create the workshop environment
```

The environment is on the `PATH` of both terminals below. Check the
version of `muructl` in the terminal on the right.

```{execute}
:id: muructl-version
:session: client
:wait: prompt
muructl --version
```

```{verify}
:id: muructl-installed
:label: muructl is installed
:substrate: shell
:trigger: after:muructl-version
muructl --version
```

```{hint}
:title: If port {{ app_port }} or {{ https_port }} is taken on your machine
The project is served on port {{ app_port }} and, over HTTPS, on port
{{ https_port }}. If something else already uses either of them, open
the Variables dialog from the gear button in the header of this panel
and change `app_port` or `https_port`. Every command in the workshop
uses the new values.
```

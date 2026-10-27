# Welcome to Muru workshops

These are guided, hands-on workshops on Muru, which serves Python WSGI
and ASGI applications with zero-downtime releases. Each workshop takes
a question you might have and has you answer it by doing it, in this
JupyterLab, with the workshop checking your work as you go. The workshop browser lists the workshops in the order to take
them; open the first, and the Finish dialog at the end of each offers
the next.

This session runs in a GitHub codespace, which opens in VS Code in the
browser. JupyterLab starts in the background, which takes a minute or
so the first time, and VS Code then shows a notification that the
application on port 8888 is available. Click its Open in Browser button
to open JupyterLab in a new tab. If the notification has gone, open the
Ports panel in VS Code and open the address of the port labelled
JupyterLab.

Leave the JupyterLab port's visibility as Private. JupyterLab here asks
for no password or token, because a private port can only be reached by
you, signed in to GitHub. Making the port public would let anyone who
has its address run code in your codespace.

When you open a workshop, JupyterLab shows what it will do in this
codespace and asks you how far to trust it. Choose Trust to let its
actions run as the workshop intends. The workshops are not trusted for
you, because the codespace is yours, tied to your GitHub account, and
JupyterLab runs without the GitHub token the codespace holds.

The codespace uses your monthly Codespaces allowance while it runs and
stops by itself after a period of inactivity; your work is kept. Resume
it from [github.com/codespaces](https://github.com/codespaces), and
delete it there when you have finished with the workshops.

As you work through a workshop, its progress is reported to the
workshops' own analytics service: which pages you visited, which
actions you clicked and what the checks found, and when. That is how
it can be seen where the workshops are clear and where they are not.
Nothing in what is reported identifies you or your codespace.
Nothing you type is sent, nor the notebooks you make, the output of
cells, or the answers you give to forms, only which step happened and
when.

"""The Flask side of the orders site: a page and a description of itself.

The page at / opens a WebSocket to the FastAPI side, at api/echo
relative to wherever the page is served from, and shows what comes
back.
"""

import os

from flask import Flask, request

app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Orders</title>
<style>
  body { font: 15px/1.5 system-ui, sans-serif; margin: 1.5rem; }
  #log { border: 1px solid #ccc; padding: 0.5rem 1rem; min-height: 6rem; }
  #log p { margin: 0.25rem 0; }
</style>
</head>
<body>
<h1>Orders</h1>
<p>This page came from Flask, over WSGI, in worker process {pid}. The
messages below go over a WebSocket to FastAPI, over ASGI.</p>
<p><button id="send">Send a message</button></p>
<div id="log"></div>
<script>
  const log = document.getElementById("log");
  const url = new URL("api/echo", window.location.href);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  const socket = new WebSocket(url);
  let count = 0;

  function show(text) {
    const line = document.createElement("p");
    line.textContent = text;
    log.appendChild(line);
  }

  function send() {
    count += 1;
    socket.send("message " + count + " from the browser");
  }

  socket.onopen = () => { show("connected to " + url.pathname); send(); };
  socket.onmessage = (event) => show(event.data);
  socket.onclose = () => show("closed");
  document.getElementById("send").onclick = send;
</script>
</body>
</html>
"""


@app.get("/")
def index():
    return PAGE.replace("{pid}", str(os.getpid()))


@app.get("/about")
def about():
    return {
        "framework": "Flask",
        "interface": "WSGI",
        "worker process": os.getpid(),
        "SCRIPT_NAME": request.environ["SCRIPT_NAME"],
        "PATH_INFO": request.environ["PATH_INFO"],
    }

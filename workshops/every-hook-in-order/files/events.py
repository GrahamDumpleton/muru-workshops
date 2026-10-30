"""An ASGI application with a lifespan, written without a framework.

The lifespan messages arrive on a connection of their own, once in each
worker: startup before the worker takes requests, shutdown when it stops.
"""

import os


async def application(scope, receive, send):
    if scope["type"] == "lifespan":
        while True:
            message = await receive()

            if message["type"] == "lifespan.startup":
                print(f"lifespan startup  in process {os.getpid()}")
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                print(f"lifespan shutdown in process {os.getpid()}")
                await send({"type": "lifespan.shutdown.complete"})
                return

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }
    )
    await send({"type": "http.response.body", "body": f"Events from process {os.getpid()}\n".encode()})

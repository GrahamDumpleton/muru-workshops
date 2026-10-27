"""The FastAPI side of the orders site, mounted at /api."""

import os
import threading

from fastapi import FastAPI, Request, WebSocket

app = FastAPI()


@app.get("/about")
async def about(request: Request):
    return {
        "framework": "FastAPI",
        "interface": "ASGI",
        "worker process": os.getpid(),
        "thread": threading.current_thread().name,
        "root_path": request.scope["root_path"],
        "path": request.scope["path"],
    }


@app.websocket("/echo")
async def echo(websocket: WebSocket):
    await websocket.accept()

    async for text in websocket.iter_text():
        await websocket.send_text(f"FastAPI in worker process {os.getpid()} got: {text}")

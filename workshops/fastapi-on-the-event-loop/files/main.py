"""A FastAPI price service: where each kind of path operation runs.

The prices are loaded from prices.json by the lifespan, once in each
worker, and handed to every request as request.state.prices.
"""

import asyncio
import json
import os
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request


@asynccontextmanager
async def lifespan(app):
    with open("prices.json") as file:
        prices = json.load(file)

    print(f"prices loaded in process {os.getpid()}")
    yield {"prices": prices}
    print(f"lifespan shut down in process {os.getpid()}")


app = FastAPI(lifespan=lifespan)


def where():
    return {"thread": threading.current_thread().name, "process": os.getpid()}


@app.get("/prices")
async def prices(request: Request):
    return request.state.prices


# Where each kind of path operation runs.


@app.get("/where/async")
async def where_async():
    return where()


@app.get("/where/sync")
def where_sync():
    return where()


@app.get("/where/to-thread")
async def where_to_thread():
    return await asyncio.to_thread(where)


# The same fifth of a second of waiting, done four ways.


@app.get("/wait/async")
async def wait_async():
    await asyncio.sleep(0.2)


@app.get("/wait/sync")
def wait_sync():
    time.sleep(0.2)


@app.get("/wait/to-thread")
async def wait_to_thread():
    await asyncio.to_thread(time.sleep, 0.2)


@app.get("/wait/blocking")
async def wait_blocking():
    time.sleep(0.2)


# A call that blocks the event loop for half a minute.


@app.get("/stall")
async def stall():
    time.sleep(30)

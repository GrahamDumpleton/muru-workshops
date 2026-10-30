"""The shop's pages."""

import os

from flask import Blueprint, current_app, render_template

bp = Blueprint("shop", __name__)


@bp.get("/")
def index():
    products = current_app.extensions["pool"].query("SELECT name FROM products ORDER BY id")
    return render_template("index.html", products=[name for (name,) in products], pid=os.getpid())


@bp.get("/pool")
def pool():
    current_app.logger.info("pool asked for in process %d", os.getpid())
    return {
        "worker process": os.getpid(),
        "pool made in": current_app.extensions["pool"].created_in,
    }


@bp.get("/stock")
def stock():
    raise RuntimeError("the stock count for Teapot is negative")

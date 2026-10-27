"""A small Flask shop, to serve under muructl run.

Each view does something worth watching in the terminal: one prints,
one logs a warning and is slow, and asking for a product that does not
exist raises a KeyError.
"""

import logging
import os
import time

from flask import Flask, jsonify

app = Flask(__name__)

# Flask normally catches an exception in a view and answers with a
# plain 500 page of its own. Propagating it lets the server answer
# instead, which under muructl run is a page with the traceback.
app.config["PROPAGATE_EXCEPTIONS"] = True

log = logging.getLogger("reports")

PRODUCTS = {1: "teapot", 2: "kettle", 3: "mug"}


@app.get("/")
def index():
    return f"The shop, served by worker process {os.getpid()}.\n"


@app.get("/products/<int:product_id>")
def product(product_id):
    print(f"looking up product {product_id}")
    name = PRODUCTS[product_id]
    return jsonify(id=product_id, name=name)


@app.get("/report")
def report():
    log.warning("building the sales report, which is slow")
    time.sleep(1.5)
    return "Sales report: 3 products, 0 sales.\n"

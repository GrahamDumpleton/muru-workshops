"""A database pool of one SQLite connection, opened when the pool is made."""

import os
import sqlite3
import threading

PRODUCTS = [(1, "Teapot"), (2, "Mug"), (3, "Tea towel")]


class Pool:
    def __init__(self, path):
        self.created_in = os.getpid()
        self.lock = threading.Lock()
        self.connection = sqlite3.connect(path, timeout=5, check_same_thread=False)

        with self.lock, self.connection:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT)"
            )
            self.connection.executemany("INSERT OR IGNORE INTO products VALUES (?, ?)", PRODUCTS)

    def query(self, sql, *args):
        with self.lock:
            return self.connection.execute(sql, args).fetchall()


def init_app(app):
    app.extensions["pool"] = Pool(app.config["DATABASE"])

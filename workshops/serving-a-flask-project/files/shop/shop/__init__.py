"""The shop: a Flask application built by a factory."""

import os

from flask import Flask

from . import db, views


def create_app():
    app = Flask(__name__)

    # Settings from FLASK_ environment variables, such as
    # FLASK_PROPAGATE_EXCEPTIONS, then the database from SHOP_DATABASE.
    app.config.from_prefixed_env()
    app.config.setdefault("DATABASE", os.environ.get("SHOP_DATABASE", "shop.db"))

    db.init_app(app)
    app.register_blueprint(views.bp)

    app.logger.info("application built in process %d", os.getpid())

    return app

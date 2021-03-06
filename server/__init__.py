# coding: utf-8
import os

from flask import Flask
from server.database import init_db
from server.database import close_db
from server.views.auth import auth_bp
from server.views.feed import feed_bp
from server.views.follow import follow_bp
from server.views.index import index_bp
from server.views.portfolio import portfolio_bp
from server.views.transaction import transaction_bp


def create_app():
    # Create the flask instance and configure the app's secret key and database
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev",)

    # Load the instance config, if it exists
    app.config.from_pyfile("config.py", silent=True)

    init_db()

    # app.teardown_appcontext() tells Flask to call that function when cleaning
    # up after returning the response.
    app.teardown_appcontext(close_db)

    # Registering blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(follow_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(feed_bp)

    return app

from flask import Flask
from .models import db

def create_app(env):
    app = Flask(__name__)
    if env == "test":
        app.config.from_object("config_test")
    else:
        app.config.from_object("config")


    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()  # Create database tables for our data models

        return app
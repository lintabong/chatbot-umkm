from flask import Flask
from .config import Config
from .routes import register_blueprints
from pymongo import MongoClient
from google import genai


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    global mongo, client

    mongo = MongoClient(app.config['MONGO_URI']).get_default_database()
    client = genai.Client()

    register_blueprints(app)

    return app

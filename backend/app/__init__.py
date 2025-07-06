from flask import Flask
from .config import Config
from .routes import register_blueprints
from pymongo import MongoClient
from google import genai


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    global mongo, client, genai_context

    mongo = MongoClient(app.config['MONGO_URI']).get_default_database()
    client = genai.Client()
    genai_context = app.config['MODEL_CONTEXT']

    register_blueprints(app)

    return app

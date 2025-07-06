"""
Collect all Blueprints for easy registration.
"""

def register_blueprints(app):
    # ‑‑ import locally so the modules see the *app* only when called
    from .index import bp as index_bp          # '/', '/version'
    from .chat import bp as chat_bp          # '/startchat', '/listchatid', '/chat/<id>'

    app.register_blueprint(index_bp)
    app.register_blueprint(chat_bp)

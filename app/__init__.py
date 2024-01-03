from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')

    with app.app_context():
        from . import auth
        from . import main
        app.register_blueprint(auth.bp)
        app.register_blueprint(main.bp)

    return app

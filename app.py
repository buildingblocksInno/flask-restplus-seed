"""
Entry Point of the APP
"""
import os
import datetime

from flask import Flask
from flask_cors import CORS

from app_extensions import get_db_connection_url, bcrypt, serializer, jwt
from database import db

from utils.api import api_bp, configure_namespaces


def create_app() -> Flask:
    """Factory method to create a new Flask App"""
    app = Flask(__name__)

    # database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = get_db_connection_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT Configuration
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(
        minutes=int(os.environ.get("JWT_TIMEOUT")))

    # Initializer the CORS for the current App
    CORS(app, support_credentials=True, resources={r"/*": {"origins": "*"}})

    configure_namespaces()
    app.register_blueprint(api_bp)

    return app


def register_extensions(app: Flask):
    """
    Register the required extensions for Flask App
    :param app: app to register the required extensions
    :return: None
    """
    db.init_app(app)
    bcrypt.init_app(app)
    serializer.init_app(app)
    jwt.init_app(app)


if __name__ == '__main__':
    app = create_app()
    register_extensions(app)
    port = os.environ.get("APP_PORT", 8080)
    debug = os.environ.get("APP_DEBUG", False)
    app.run(
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=port,
        debug=debug
    )

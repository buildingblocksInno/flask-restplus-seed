"""
Creates app extensions for configuring the extra services
"""
import os

from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

# load environment variables
load_dotenv()


def get_db_connection_url():
    """
    Generate Connection URL from the CONFIG
    :return: <type: str> Connection URL
    """
    username = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_SCHEMA")
    port = os.environ.get("DB_PORT")

    return f"postgresql://{username}:{password}@{host}:{port}/{db_name}"


jwt = JWTManager()
serializer = Marshmallow()
bcrypt = Bcrypt()

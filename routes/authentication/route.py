"""
The file will contain the APIs used for Authentication
"""
import logging
from http import HTTPStatus

from app_extensions import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import Namespace, Resource

from routes.authentication.auth import UserAccess
from routes.authentication.models import USER_LOGIN_MODEL, \
    SIGNUP_USER_MODEL

logger = logging.getLogger(__name__)

users = []  # temporarily this will work as a database for our users info

AUTH_NS = Namespace("auth", description="APIs for Authentication Operation")

AUTH_NS.model(
    name=SIGNUP_USER_MODEL.name,
    model=SIGNUP_USER_MODEL
)
AUTH_NS.model(
    name=USER_LOGIN_MODEL.name,
    model=USER_LOGIN_MODEL
)


@AUTH_NS.route("/signup")
class SignUp(Resource):
    """
    SignUp user using JWT API
    """

    @AUTH_NS.expect(SIGNUP_USER_MODEL)
    @AUTH_NS.doc("user_signup")
    def post(self):
        """
        POST API which will be used to Sigup New users
        :return:
        """
        data = AUTH_NS.payload

        user_fetched = UserAccess.get_user(
            username=data["username"],
            vendor_id=data["vendor_id"],
            user_type=data["user_type"]
        )
        if user_fetched:
            return {'message': 'User already exists'}, 409

        created_user = UserAccess.create_user(
            username=data["username"],
            vendor_id=data["vendor_id"],
            user_type=data["user_type"],
            password=data["password"]
        )

        return {
            "message": "User created successfully",
            "userId": created_user.id
        }, HTTPStatus.CREATED


@AUTH_NS.route('/login')
class Login(Resource):
    @AUTH_NS.expect(USER_LOGIN_MODEL)
    @AUTH_NS.doc('user_login')
    def post(self):
        data = AUTH_NS.payload
        user = UserAccess.get_user(
            username=data["username"],
            vendor_id=data["vendor_id"],
            user_type=data["user_type"]
        )
        if not user or not bcrypt.check_password_hash(user.password, \
                data["password"]):
            return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, HTTPStatus.OK

"""
This file will contain the models which will be used for input and output
payloads of Authentication module
"""
from common.customTypes import UserType
from flask_restx import Model, fields

SIGNUP_USER_MODEL = Model(
    "user",
    {
        "username": fields.String("username", required=True,
                                  description="The username"),
        "password": fields.String("password", required=True,
                                  description="The password"),
        "user_type": fields.String("userType", required=True,
                                   description="Type of user",
                                   enum=[u_type.name for u_type in UserType]),
        "vendor_id": fields.Integer("vendor_id", required=True,
                                    description="Denotes that the vendor is "
                                                "of which vendor")
    }
)

USER_LOGIN_MODEL = Model(
    "user_login",
    {
        "username": fields.String("username", required=True,
                                  description="The username"),
        "password": fields.String("password", required=True,
                                  description="The password"),
        "user_type": fields.String("userType", required=True,
                                   description="Type of user",
                                   enum=[u_type.name for u_type in UserType]),
        "vendor_id": fields.Integer("vendor_id", required=True,
                                    description="Denotes that the vendor is "
                                                "of which vendor")
    }
)

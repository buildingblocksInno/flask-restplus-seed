"""
Default route where you can set the APIs
"""
import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restx import Namespace, Resource
from flask_restx._http import HTTPStatus

logger = logging.getLogger(__name__)

DEFAULT_NS = Namespace("Default", description="Default Namespace which "
                                              "contains basic required APIs")


@DEFAULT_NS.route("/health-check")
class Default(Resource):
    """
    Health check API for the required
    """
    def get(self):
        """
        Health check get API
        :return:
        """
        logger.info("The service is healthy")
        return {
            "message": "The service is healthy",
            "status_code": HTTPStatus.OK
        }


@DEFAULT_NS.route("/test")
class Test(Resource):
    """
    Test API with required auth
    """

    @jwt_required()
    def get(self):
        """
        Test authentication with this API
        :return:
        """
        try:
            curent_user = get_jwt_identity()
            return {
                "message": f"Welcome to the System: {curent_user}",
                "status_code": HTTPStatus.OK
            }, HTTPStatus.OK
        except NoAuthorizationError as nae:
            logger.error("No Authorized")
            return {
                "message": f"User is Unauthorized",
                "status_code": HTTPStatus.UNAUTHORIZED
            }, HTTPStatus.UNAUTHORIZED

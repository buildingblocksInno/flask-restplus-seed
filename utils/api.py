import os

from flask import Flask, url_for, Blueprint
from flask_restx import Api, apidoc

from routes.authentication.route import AUTH_NS
from routes.default import DEFAULT_NS


VERSION = os.environ.get("VERSION", "0.0.1")


class CustomApi(Api):
    """
    Custom API Builder class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._schema = None

    def init_app(self, app: Flask, **kwargs: dict) -> None:
        """
        This method can be overriden in case any additional things needs to be
        altered in the request.
        For example: Operations which needs to be handled before and after
        request is sent,
        Or Auth needs to be taken care of, etc.
        :param app: Instance of App which needs to be initiated for API
        :param kwargs: additional Keywords Arguments
        :return: NA
        """
        super().init_app(app, **kwargs)

    @property
    def specs_url(self):
        """
        The swagger specific Absolute URL
        API class has _external=True which does not work with few deployment
        systems or any APIs behind proxy.
        :return: NA
        """
        return url_for(self.endpoint("specs"), _external=False)


API_V1_PREFIX = "/api/v1/"
api_bp = Blueprint("api", __name__, url_prefix=API_V1_PREFIX)

api = CustomApi(
    api_bp,
    title="Flask RestX service",
    version=f"v{VERSION}",
    description="The webservice provider"
)

apidoc.apidoc.url_prefix = API_V1_PREFIX

AVAILABLE_NAMESPACES = [
    DEFAULT_NS,
    AUTH_NS
]

api.authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter: **\'Bearer <JWT>\'**, '
                       'where JWT is the access token'
    }
}

api.security = ['Bearer']

def configure_namespaces():
    """
    Configure visible namespaces for this app.
    :return:
    """
    for namespace in AVAILABLE_NAMESPACES:
        api.add_namespace(namespace)

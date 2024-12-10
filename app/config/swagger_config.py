from flask import Blueprint
from flask_restx import Api
from flask_restx import apidoc


from app.routes.transform_image import api as upload_api
from app.routes.server_online import api as test_api

URL_PREFIX = '/api/v1'


def create_api(app):
    """
    Create and configure the Flask-RESTX API with namespaces.
    """
    # Create the API object with the URL prefix for Swagger
    apidoc.url_prefix = URL_PREFIX
    blueprint = Blueprint('main', __name__, url_prefix=URL_PREFIX)

    api = Api(blueprint,
              title='pixelshowroom.com APIs',
              version='1.0',
              description='API for pixel-showroom')  # Swagger UI URL

    # Register namespaces
    api.add_namespace(upload_api)
    api.add_namespace(test_api)

    # Register the blueprint with the Flask app
    app.register_blueprint(blueprint)

    return api

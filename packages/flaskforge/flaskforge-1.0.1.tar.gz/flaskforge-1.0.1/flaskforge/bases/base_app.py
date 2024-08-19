from os import environ

from flask import Flask
from apispec import APISpec
from flask_apispec import FlaskApiSpec
from flask_jwt_extended import JWTManager
from apispec.ext.marshmallow import MarshmallowPlugin

app = Flask(__name__)


app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title=environ.get("TITLE"),
            version=environ.get("API_VERSION"),
            openapi_version="2.0",
            plugins=[MarshmallowPlugin()],
        ),
        "APISPEC_SWAGGER_UI_URL": f"""/{environ.get("APISPEC_SWAGGER_UI_URL")}/""",
        "APISPEC_SWAGGER_URL": "/json/",
    }
)

spec = FlaskApiSpec(app)

app.config.update(
    {
        "JWT_SECRET_KEY": environ.get("JWT_SECRET_KEY"),
        "JWT_TOKEN_LOCATION": [environ.get("JWT_TOKEN_LOCATION", "cookies")],
        "JWT_COOKIE_CSRF_PROTECT": environ.get("JWT_COOKIE_CSRF_PROTECT", False),
    }
)

jwt = JWTManager(app)

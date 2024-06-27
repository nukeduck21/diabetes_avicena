import logging
import warnings

warnings.simplefilter("ignore")

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_mail import Mail

from api.restplus import api
from api.settings import BaseConfig

from api.endpoint.create_training_data import ns as service_creacion_data_diabetes
from api.endpoint.diabetes_train import ns as service__diabetes

_logger = logging.getLogger(__name__)


def initialize_app(flask_app):
    # FLASK MAIL CONFIG
    flask_app.config.from_object(BaseConfig)
    print(flask_app.config.items())

    # BLUEPRINT
    blueprint = Blueprint("api", __name__)
    api.init_app(blueprint)

    CORS(
        flask_app,
        origins="*",
        allow_headers=[
            "Content-Type",
            "application/json",
            "Authorization",
            "Access-Control-Allow-Credentials",
        ],
        supports_credentials=True,
    )

    api.add_namespace(service__diabetes)
    api.add_namespace(service_creacion_data_diabetes)
    flask_app.register_blueprint(blueprint)


app = Flask(__name__)
mail = Mail()

initialize_app(app)
mail.init_app(app)

if __name__ == "__main__":
    _logger.info("Starting training Diabetes")
    app.run(debug=True)#(, host="0.0.0.0", port=8080)
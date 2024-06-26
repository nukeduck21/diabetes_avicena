import logging
from pymongo import MongoClient
import urllib.parse
from flask_restplus import Api, Namespace

import warnings
warnings.simplefilter('ignore')

_logger = logging.getLogger(__name__)

api = Api(
    version='1.0',
    title='Modelos de predicción - Analítica',
    description='Servicios web para el client de predicción de diabetes'
)

api.add_namespace(Namespace('Diabetes', 'Client diabetes'), path='/diabetes')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    _logger.exception(message)
    _logger.exception(e)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
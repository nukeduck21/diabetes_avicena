import os

class BaseConfig():
    """ Basic settings required by all classes """
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")
    MAIL_USE_TLS = True
    MAIL_USE_SSL: False
    MAIL_DEBUG = True

    STANDAR_ESTADIO='models/Convencional/est_timeind_rf.pkl'
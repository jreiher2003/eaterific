import os 

class BaseConfig(object): 
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    CACHE_TYPE = "memcached"
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': os.environ["FACEBOOK_ID"],
            'secret': os.environ["FACEBOOK_SECRET"]
        },
        'twitter': {
            'id': os.environ["TWITTER_ID"],
            'secret': os.environ["TWITTER_SECRET"]
        },
        'google': {
            'id': os.environ["GOOGLE_ID"],
            'secret': os.environ["GOOGLE_SECRET"]
        }
    }

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MAIL_SUPPRESS_SEND = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MAIL_SERVER = "smtp@gmail.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "eaterific"
    MAIL_PASSWORD = "eaterific123"
    MAIL_DEFAULT_SENDER = "eaterific@gmail.com"
    # SQLALCHEMY_ECHO = True

class ProductionConfig(BaseConfig):
    DEBUG = False

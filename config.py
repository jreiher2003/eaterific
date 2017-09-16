import os 

class BaseConfig(object): 
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    # OAUTH_CREDENTIALS = os.environ["OAUTH_CREDENTIALS"]
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '231015064035835',
            'secret': 'd688bfa5a4488201d316cf0acddd45d7'
        },
        'twitter': {
            'id': 'XIhymb80u5I7D6cCqomQue3HB',
            'secret': 'bthFdmSejZ8SvRtOJ7GkgyGMySqCK6Y4JbZx4DuG2RRq1NcPRA'
        },
        'github': {
            'id': 'aef9bc8c658eba792b31',
            'secret': '328b02fd62a7c81a5ab4d465ada7785af1b12df8'
        },
        'google': {
            'id': '724284536117-pcjh1en5ic87du4aqfe9p0kg1v5tjpc5.apps.googleusercontent.com',
            'secret': 'Ny9jL3GIfiRtSTFb8YcRkady'
        },
        'linkedin': {
            'id': '785ik3n0buzw8l',
            'secret': '2guAiqJfvHkagvFO'
        },
        'foursquare': {
            'id': 'NSMK1WFBH2UIAEDV1E3QAPFLPOA5HU0RMNAOFCP4JVQDLMPB',
            'secret': 'VGCRYE3YXZKR0O2XYQNPDAMOS4KJZCLW0XUVP2DHD1BMPYLS'
        },
        'reddit': {
            'id': 'p-ft1woSOtK0zA',
            'secret': 'Zy7XnbiBLKarjZz3Ar3KINSYy3o',
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
    SQLALCHEMY_ECHO = True

class ProductionConfig(BaseConfig):
    DEBUG = False
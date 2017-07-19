import os 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
# from flask_bcrypt import Bcrypt 
from flask_login import LoginManager#, current_user 
from flask_script import Manager

app = Flask(__name__) 
app.config.from_object(os.environ["APP_SETTINGS"])
db = SQLAlchemy(app) 
# bcrypt = Bcrypt(app)
manager = Manager(app) 

from app.users.views import users_blueprint 
app.register_blueprint(users_blueprint) 
from app.rest.views import rest_blueprint 
app.register_blueprint(rest_blueprint) 

from app.users.models import *
lm = LoginManager(app)

@lm.user_loader 
def load_user(id):
    return Users.query.get(int(id)) 


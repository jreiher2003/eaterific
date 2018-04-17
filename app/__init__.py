# -*- coding: utf-8 -*-
import os 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_mail import Mail
from flask_caching import Cache
from flask_login import LoginManager#, current_user 
from flask_script import Manager

app = Flask(__name__) 
app.config.from_object(os.environ["APP_SETTINGS"])
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
manager = Manager(app) 
mail = Mail(app)
cache = Cache(app)

from app.users.views import users_blueprint 
app.register_blueprint(users_blueprint) 
from app.rest.views import rest_blueprint 
app.register_blueprint(rest_blueprint) 

from app.users.models import *
lm = LoginManager(app)

from temp_filters import yelp_city_filter, format_phone

app.jinja_env.filters["format_phone"] = format_phone
app.jinja_env.filters["yelp_city_filter"] = yelp_city_filter

lm.login_view = 'rest.index'

@lm.user_loader 
def load_user(id):
    return UsersProfile.query.get(int(id)) 


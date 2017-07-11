import os 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_script import Manager

app = Flask(__name__) 
app.config.from_object(os.environ["APP_SETTINGS"])
db = SQLAlchemy(app) 
manager = Manager(app) 

from app.rest.views import rest_blueprint 
app.register_blueprint(rest_blueprint) 
# import views

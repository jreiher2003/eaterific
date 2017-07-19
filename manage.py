import os 
import unittest 
from app import app, db
from flask_script import Manager, Server 
from flask_migrate import Migrate, MigrateCommand 
# from app.users.models import Users, UserRegister, SocialLogin, ProviderName, AsyncOperationStatus, AsyncOperation, TodoItem
from app.users.models import *

manager = Manager(app) 
migrate = Migrate(app, db)
manager.add_command("runserver", Server(host="0.0.0.0", port=5555))
manager.add_command('db', MigrateCommand)

@manager.command 
def create_users():
    
    Users.__table__.create(db.engine)
    # UserRegister.__table__.create(db.engine)
    # ProviderName.__table__.create(db.engine)
    # SocialLogin.__table__.create(db.engine)
    
    # TodoItem.__table__.create(db.engine)
    print "created all users tables" 

@manager.command 
def drop_users():
    # TodoItem.__table__.drop(db.engine)
   
    # SocialLogin.__table__.drop(db.engine)
    # ProviderName.__table__.drop(db.engine)
    # UserRegister.__table__.drop(db.engine)
    Users.__table__.drop(db.engine)
    # UserProfile.__table__.drop(db.engine)
    print "dropped all users tables" 

@manager.command 
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests) 

if __name__ == "__main__":
    manager.run()
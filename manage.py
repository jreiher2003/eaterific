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
    UsersProfile.__table__.create(db.engine, checkfirst=True)
    Role.__table__.create(db.engine, checkfirst=True)
    UserRoles.__table__.create(db.engine, checkfirst=True)
    UsersRegister.__table__.create(db.engine, checkfirst=True)
    ProviderName.__table__.create(db.engine, checkfirst=True)
    SocialLogin.__table__.create(db.engine, checkfirst=True)
    TodoItem.__table__.create(db.engine, checkfirst=True)
    print "created all users tables" 

@manager.command 
def drop_users():
    TodoItem.__table__.drop(db.engine,checkfirst=True)
    SocialLogin.__table__.drop(db.engine, checkfirst=True)
    ProviderName.__table__.drop(db.engine, checkfirst=True)
    UsersRegister.__table__.drop(db.engine, checkfirst=True)
    UserRoles.__table__.drop(db.engine, checkfirst=True)
    Role.__table__.drop(db.engine, checkfirst=True)
    UsersProfile.__table__.drop(db.engine, checkfirst=True)
    print "dropped all users tables" 

@manager.command 
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests) 

if __name__ == "__main__":
    manager.run()
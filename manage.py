import os 
import unittest 

from app import app, db
from flask_script import Manager, Server 
from flask_migrate import Migrate, MigrateCommand 


manager = Manager(app) 
migrate = Migrate(app, db)
manager.add_command("runserver", Server(host="0.0.0.0", port=5555))
manager.add_command('db', MigrateCommand)

@manager.command 
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests) 

if __name__ == "__main__":
    manager.run()
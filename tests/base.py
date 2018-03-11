
import datetime
from flask_testing import TestCase 
from app import app, db
from app.users import models


class BaseTestCase(TestCase):
    """A base test case."""
 
    def create_app(self):
        app.config.from_object('config.TestConfig')
        app.test_client()
        return app

    def setup(self):
    	db.create_all()
        db.session.add(
            UsersProfile(
            id = 1,
            screen_name="J3ff_",
            password="password",
            avatar="jeff.jpg",
            email="jeffreiher@gmail.com",
            date_created=datetime.datetime.utcnow,
            date_modified =datetime.datetime.utcnow,
            last_login_at=datetime.datetime.utcnow,
            current_login_at=datetime.datetime.utcnow,
            current_login_ip="10.0.0.1",
            login_count=1))
        db.session.add(Role(id=1, name="admin"))
        db.session.add(UserRoles(id=1, user_id=1, role_id=1))
        db.session.add(UsersRegister(
        	username = "J3ff_",
		    email = "jeffreiher@gmail.com",
		    _password = "password123",
		    confirmed =  datetime.datetime.utcnow,
		    confirmed_at = datetie.datetime.utcnow,
		    users_id = 1))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
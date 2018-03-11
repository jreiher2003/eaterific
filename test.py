import os
from app import app
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):_
        db = app.config['SQLALCHEMY_DATABASE_URI']
        app.testing = True
        self.app = app.test_client()
        with app_context():
            app.init_db()

    def tearDown(self):
        os.close(self.db)
        os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])

if __name__ == '__main__':
    unittest.main()

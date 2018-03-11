import unittest 
from base import BaseTestCase

class TestUser(BaseTestCase):

    def test_login(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)

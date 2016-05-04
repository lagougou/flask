import unittest
from app import create_app,db
from flask import current_app

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def tesst_app_exits(self):
        self.assertFalse(current_app is None)

    def tesing_app_is_tesing(self):
        self.assertTrue(current_app.confit['TESTING'])


import unittest
from json import loads
from backend.src.login_user.login_user import LoginUserClass
import jwt
from backend.src.mongo_connection.mongo_connection import get_jwt_key


class MockDbWithPass:
    def find_one(self, x):
        return {'password': 'testpassword',
                '_id': 'testUserId'}


class MockDb:
    def find_one(self, x):
        pass


class LoginUsersTest(unittest.TestCase):
    def setUp(self):
        self.loginHandler = LoginUserClass()
        self.mockMongo = {
            'Main': {
                'Users': MockDb()
            }
        }
        self.mockMongoWithPass = {
            'Main': {
                'Users': MockDbWithPass()
            }
        }

    def test_give_guest_token(self):
        result = self.loginHandler.give_guest_token('test')

        try:
            jwt.decode(result, get_jwt_key(), algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            self.fail('jwt error')
        except jwt.InvalidTokenError:
            self.fail('jwt error')

    def test_validate_token(self):
        tempToken = self.loginHandler.give_guest_token('test')
        t = loads(self.loginHandler.validate_token(tempToken))
        self.assertEqual(t['status'], 'OK')

    def test_get_user_id_from_token(self):
        token = self.loginHandler.give_guest_token('123')
        result = self.loginHandler.get_user_id_from_token(token)
        self.assertTrue('guestToken' in result)

    def test_login_panel_no_user(self):
        result = loads(self.loginHandler.login_panel('testemail@testemail.com', 'nopassword', self.mockMongo))
        self.assertEqual(result['status'], 'error_no_such_user')

    def test_login_panel_wrong_password(self):
        result = loads(self.loginHandler.login_panel('testemail@testemail.com', 'nopassword', self.mockMongoWithPass))
        self.assertEqual(result['status'], 'error_wrong_password')

    def test_login_panel_correct_password(self):
        result = loads(self.loginHandler.login_panel('testemail@testemail.com', 'testpassword', self.mockMongoWithPass))
        self.assertEqual(result['status'], 'OK')
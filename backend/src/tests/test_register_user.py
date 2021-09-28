import unittest
from json import loads
from backend.src.register_user.register_user import RegisterUserClass


class MockDb:
    def find_one(self, x):
        pass

    def insert_one(self, x):
        pass


class MockNameDbFail:
    def find_one(self, x):
        if 'name' in x:
            return True
        else:
            pass

    def insert_one(self, x):
        pass


class MockEmailDbFail:
    def find_one(self, x):
        if 'email' in x:
            return True
        else:
            pass

    def insert_one(self, x):
        pass


class RegisterUsersTest(unittest.TestCase):
    def setUp(self):
        self.registerHandler = RegisterUserClass()
        self.mockMongoSuccess = {
            'Main': {
                'Users': MockDb()
            }
        }
        self.mockMongoNameFail = {
            'Main': {
                'Users': MockNameDbFail()
            }
        }
        self.mockMongoEmailFail = {
            'Main': {
                'Users': MockEmailDbFail()
            }
        }

    def test_register_name_in_use(self):
        post_info = {
            'name': 'testName',
            'password': 'testPass',
            'username': 'testUserName',
            'email': 'email@email.com'
        }
        t = loads(self.registerHandler.run(post_info, self.mockMongoNameFail))
        self.assertEqual(t['status'], 'error_name_exists')

    def test_register_email_in_use(self):
        post_info = {
            'name': 'testName',
            'password': 'testPass',
            'username': 'testUserName',
            'email': 'email@email.com'
        }
        t = loads(self.registerHandler.run(post_info, self.mockMongoEmailFail))
        self.assertEqual(t['status'], 'error_email_exists')

    def test_register_success(self):
        post_info = {
            'name': 'testName',
            'password': 'testPass',
            'username': 'testUserName',
            'email': 'email@email.com'
        }
        t = loads(self.registerHandler.run(post_info, self.mockMongoSuccess))
        self.assertEqual(t['status'], 'OK')


if __name__ == '__main__':
    unittest.main()

import unittest
from backend.src.handle_groups.handle_groups import HandleGroupsClass


class MockDb:
    def insert_one(self, x):
        pass

    def update_one(self, x, y=None):
        pass

    def find_one(self, x, y=None):
        return {
            "group_invites": [{
                "for_group_id": "test",
                "from_user_id": "test"
            }]
        }


class HandleGroupsTest(unittest.TestCase):
    def setUp(self):
        self.mockMongo = {
            'Main': {
                'Groups': MockDb(),
                'Users': MockDb()
            }
        }
        self.handle_groups_class = HandleGroupsClass(self.mockMongo)

    def test_create_group(self):

        info = {
            'group_name': 'test_group_name',
            'user_id': '507f191e810c19729de860ea'
        }

        t = self.handle_groups_class.create_group(info)
        self.assertEqual(t['status'], 'OK')

    def test_create_group_invalid_id(self):
        info = {
            'group_name': 'test_group_name',
            'user_id': 'invalid_object_id'
        }

        t = self.handle_groups_class.create_group(info)
        self.assertEqual(t['status'], 'error_invalid_userid')

    def test_reject_group_invite(self):
        group_id = '507f191e810c19729de860ea'
        my_user_id = '507f191e810c19729de860ea'
        res = self.handle_groups_class.reject_group_invite(group_id, my_user_id)
        self.assertEqual(res['status'], 'OK')

    def test_reject_group_invite_invalid_group_id(self):
        group_id = 'invalid_object_id'
        my_user_id = '507f191e810c19729de860ea'
        res = self.handle_groups_class.reject_group_invite(group_id, my_user_id)
        self.assertEqual(res['status'], 'error_invalid_group_id')

    def test_reject_group_invite_invalid_user_id(self):
        group_id = '507f191e810c19729de860ea'
        my_user_id = 'invalid_object_id'
        res = self.handle_groups_class.reject_group_invite(group_id, my_user_id)
        self.assertEqual(res['status'], 'error_invalid_userid')

    def test_get_user_group_invites(self):
        my_user_id = '507f191e810c19729de860ea'
        res = self.handle_groups_class.get_user_group_invites(my_user_id)
        self.assertEqual(res['status'], 'OK')

    def test_get_user_group_invites_invalid_user_id(self):
        my_user_id = 'invalid_group_id'
        res = self.handle_groups_class.get_user_group_invites(my_user_id)
        self.assertEqual(res['status'], 'error_invalid_userid')

    def test_send_group_invite(self):
        info = {
            'invited_user_id': '507f191e810c19729de860ea',
            'group_id': '507f191e810c19729de860ea',
            'admin_user_id': '507f191e810c19729de860ea'
        }
        res = self.handle_groups_class.send_group_invite(info)
        self.assertEqual(res['status'], 'OK')

    def test_send_group_invite_invalid_invited_user_id(self):
        info = {
            'invited_user_id': 'invalid_id',
            'group_id': '507f191e810c19729de860ea',
            'admin_user_id': '507f191e810c19729de860ea'
        }
        res = self.handle_groups_class.send_group_invite(info)
        self.assertEqual(res['status'], 'error_invalid_invited_user_id')

    def test_send_group_invite_invalid_group_id(self):
        info = {
            'invited_user_id': '507f191e810c19729de860ea',
            'group_id': 'invalid_id',
            'admin_user_id': '507f191e810c19729de860ea'
        }
        res = self.handle_groups_class.send_group_invite(info)
        self.assertEqual(res['status'], 'error_invalid_group_id')

    def test_send_group_invite_invalid_admin_user_id(self):
        info = {
            'invited_user_id': '507f191e810c19729de860ea',
            'group_id': '507f191e810c19729de860ea',
            'admin_user_id': 'invalid_id'
        }
        res = self.handle_groups_class.send_group_invite(info)
        self.assertEqual(res['status'], 'error_invalid_admin_userid')

    def test_accept_group_invite(self):
        group_id = '507f191e810c19729de860ea'
        my_user_id = '507f191e810c19729de860ea'
        res = self.handle_groups_class.accept_group_invite(group_id, my_user_id)
        self.assertEqual(res['status'], 'OK')

    def test_accept_group_invite_invalid_group_id(self):
        group_id = 'invalid_id'
        my_user_id = '507f191e810c19729de860ea'
        res = self.handle_groups_class.accept_group_invite(group_id, my_user_id)
        self.assertEqual(res['status'], 'error_invalid_group_id')

    def test_accept_group_invite_invalid_user_id(self):
        group_id = '507f191e810c19729de860ea'
        my_user_id = 'invalid_id'
        res = self.handle_groups_class.accept_group_invite(group_id, my_user_id)
        self.assertEqual(res['status'], 'error_invalid_userid')

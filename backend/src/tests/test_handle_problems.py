import unittest
from json import loads
import pymongo.errors
from backend.src.handle_problems.handle_problems import HandleProblemsClass


class MockDb:
    def insert_one(self, x):
        pass


class HandleProblemsTest(unittest.TestCase):
    def setUp(self):
        self.handle_problems_class = HandleProblemsClass()
        self.mockMongoSuccess = {
            'Main': {
                'Problems': MockDb()
            }
        }

    def test_create_problem(self):
        post_info = {
            'title': 'test',
            'public': 'true',
            'tags': ['tag', 'tag2'],
            'text': 'text',
            'start_date': 'somedate',
            'end_date': 'somedate',
            'time_limit': '01:00:00'
        }
        t = loads(self.handle_problems_class.create_problem(post_info, self.mockMongoSuccess))
        self.assertEqual(t['status'], 'OK')

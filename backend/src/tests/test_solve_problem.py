import unittest
from backend.src.solve_problem.solve_problem import SolveProblemClass


class MockCursor:
    inserted_id = '61bceee9a60aabad57ada76d'


class MockDb:
    def find_one(self, x, y=None):
        if x['_id'] == '61bceee9a60aabad57ada76a':
            return 'db_result_not_null'
        else:
            pass

    def update_one(self, x, y=None):
        return '61bceee9a60aabad57ada76c'

    def insert_one(self, x, y=None):
        return MockCursor()


class TestSolveProblem(unittest.TestCase):
    def setUp(self) -> None:
        self.mockMongo = {
            'Main':
                {
                    'Problems': MockDb(),
                    'Code': MockDb()
                }
        }
        self.testId = '61bceee6a60aabad57ada76a'
        self.testId2 = '61bceee9a60aabad57ada76b'
        self.solver = SolveProblemClass(self.mockMongo)

    def test_get_problem_info(self):
        res = self.solver.get_problem_info(self.testId)
        self.assertEqual(res['status'], 'OK')

    def test_upload_code_invalid_id(self):
        res = self.solver.upload_solution({'problem_id': 'invalid_id'})
        self.assertEqual(res['status'], 'error_invalid_problem_id')

    def test_upload_code_invalid_id2(self):
        res = self.solver.upload_solution({'problem_id': self.testId, 'user_id': 'invalid_id'})
        self.assertEqual(res['status'], 'error_invalid_user_id')

    def test_upload_code_solution_not_created(self):
        mock_info = {
            'user_id': self.testId,
            'problem_id': self.testId,
            'language': 'python',
            'code': 'print("testing 1...2...3...)"'
        }
        res = self.solver.upload_solution(mock_info)
        self.assertEqual(res['status'], 'OK')

    def test_upload_code_solution_not_created3(self):
        mock_info = {
            'user_id': self.testId2,
            'problem_id': self.testId2,
            'language': 'python',
            'code': 'print("testing 1...2...3...)"'
        }
        res = self.solver.upload_solution(mock_info)
        self.assertEqual(res['status'], 'OK')


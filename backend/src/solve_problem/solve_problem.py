from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure
import datetime


class SolveProblemClass:
    def __init__(self, mongo_client):
        self.db_problems = mongo_client['Main']['Problems']
        self.db_code = mongo_client['Main']['Code']

    def get_problem_info(self, problem_id):

        if not ObjectId.is_valid(problem_id):
            return {"status": "error_invalid_problem_id", "message": "Invalid problem id."}

        try:
            x = self.db_problems.find_one({'_id': ObjectId(problem_id)},
                                          {'text': 1,
                                           '_id': 0,
                                           'start_date': 1,
                                           'end_date': 1,
                                           'time_limit': 1,
                                           'title': 1})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": x}

    def run_tests(self, problem_id, code, language):
        if not ObjectId.is_valid(problem_id):
            return {"status": "error_invalid_problem_id", "message": "Invalid problem id."}

        try:
            x = self.db_problems.find_one({'_id': ObjectId(problem_id)},
                                          {'tests': 1})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

    def __does_user_have_a_solution(self, user_id, problem_id):
        try:
            x = self.db_problems.find_one(
                {'_id': ObjectId(problem_id), 'solutions': {'$elemMatch': {'author_id': ObjectId(user_id)}}},
                {'solutions': 1, '_id': 0})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        if x is not None:
            return True
        else:
            return False

    def __get_solution_id(self, user_id, problem_id):
        try:
            x = self.db_problems.find_one(
                {'_id': ObjectId(problem_id), 'solutions': {'$elemMatch': {'author_id': ObjectId(user_id)}}},
                {'solutions': 1, '_id': 0})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        x = str(x['solutions'][0]['solution_id'])
        return x

    def __does_user_have_a_saved_code(self, user_id, solution_id):

        try:
            res = self.db_code.find_one({'solution_id': ObjectId(solution_id), 'author_id': ObjectId(user_id)})
        except ConnectionError:
            raise ConnectionError("Failed to connect to db")

        if res is not None:
            return True
        else:
            return False

    def __save_code(self, info):
        insertionData = {
            'code': info['code'],
            'language': info['language'],
            'shared': 0,
            'score': -1,
            'timestamp': datetime.datetime.utcnow(),
            'author_id': ObjectId(info['user_id']),
            'solution_id': ObjectId(info['solution_id']),
            'comments': []
        }

        try:
            x = self.db_code.insert_one(insertionData)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")
        return x.inserted_id

    def __create_solution_for_user(self, user_id, problem_id):

        solution_id = ObjectId.from_datetime(datetime.datetime.now())

        insertionData = {
            'solution_id': solution_id,
            'author_id': ObjectId(user_id),
            'comments': []
        }

        try:
            self.db_problems.update_one({'_id': ObjectId(problem_id)}, {'$push': {'solutions': insertionData}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return solution_id

    def __add_code_id_to_solution(self, problem_id, code_id, user_id):
        try:
            self.db_problems.update_one(
                {'_id': ObjectId(problem_id), 'solutions.author_id': ObjectId(user_id)},
                {'$push': {'solutions.$.code_ids': code_id}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

    def upload_solution(self, info):

        if not ObjectId.is_valid(info['problem_id']):
            return {"status": "error_invalid_problem_id", "message": "Invalid problem id."}

        if not ObjectId.is_valid(info['user_id']):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        if self.__does_user_have_a_solution(info['user_id'], info['problem_id']):
            solution_id = self.__get_solution_id(info['user_id'], info['problem_id'])
        else:
            solution_id = self.__create_solution_for_user(info['user_id'], info['problem_id'])

        info['solution_id'] = solution_id
        code_id = ObjectId(self.__save_code(info))
        self.__add_code_id_to_solution(info['problem_id'], code_id, info['user_id'])

        return {'status': 'OK', 'message': 'Successfully uploaded the code.'}






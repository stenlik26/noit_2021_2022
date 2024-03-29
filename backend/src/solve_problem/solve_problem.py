from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure
import datetime
from backend.src.mongo_connection.mongo_connection import get_executor_address
import requests
import codecs


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

    def run_tests(self, problem_id, code, language, all_tests):
        if not ObjectId.is_valid(problem_id):
            return {"status": "error_invalid_problem_id", "message": "Invalid problem id."}

        try:
            query_result = self.db_problems.find_one({'_id': ObjectId(problem_id)}, {'tests': 1})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        url = get_executor_address() + '/run_test'

        results = []
        passed = 0

        for test in query_result['tests']:

            inputParams = {
                'language': language,
                'code': code,
                'expected_stdout': codecs.unicode_escape_decode(test['output'])[0],
                'timeout': int(test['time_limit']) / 1000
            }
            if test['input'] != "":
                inputParams['stdin'] = test['input']

            result = requests.post(url=url, json=inputParams)

            data = result.json()

            if data['status'] != 'OK':
                return {'status': 'error_executor', 'message': data['message']}

            if data['message']['return_code'] != 0 and data['message']['stderr'] is not None:
                return {'status': 'error_compile', 'message': data['message']['stderr']}

            data = data['message']
            if not(data['is_passing'] or test['is_hidden']) or (not data['is_passing'] and all_tests):

                data['diff'] = data['diff'].replace('\t', '').replace(' |', '|\t')

                if data['return_code'] == 1:
                    # Това може да се промени в executor-a за да не се прави тук
                    data['diff'] = data['stdout'].replace(
                        'Process timed out after',
                        'Изпъленият тест надвиши времевия лимит от').replace(
                        'seconds',
                        'секунди')

                    data['stdout'] = ''
                    inputParams['expected_stdout'] = ''

                current_test_result = {
                    'diff': data['diff'],
                    'test_output': data['stdout'],
                    'expected_stdout': inputParams['expected_stdout']
                }
                if test['input'] != "":
                    current_test_result['input'] = test['input']
                results.append(current_test_result)
            elif data['is_passing']:
                passed += 1

        return {'status': 'OK',
                'message': {
                    'results': results,
                    'passed': passed,
                    'total': len(query_result['tests'])
                    }
                }

    def __does_user_have_a_solution(self, user_id, problem_id):
        try:
            x = self.db_problems.find_one(
                {'_id': ObjectId(problem_id), 'solutions': {'$elemMatch': {'author_id': ObjectId(user_id)}}},
                {'solutions': 1, '_id': 0})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return x is not None

    def __get_solution_id(self, user_id, problem_id):
        try:
            x = self.db_problems.find_one(
                {'_id': ObjectId(problem_id), 'solutions': {'$elemMatch': {'author_id': ObjectId(user_id)}}},
                {'solutions.$': 1, '_id': 0})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        x = str(x['solutions'][0]['solution_id'])
        return x

    def __get_solution_time_of_start(self, user_id, problem_id) -> datetime.datetime:
        try:
            x = self.db_problems.find_one(
                {'_id': ObjectId(problem_id), 'solutions': {'$elemMatch': {'author_id': ObjectId(user_id)}}},
                {'solutions': 1, '_id': 0})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        x = x['solutions'][0]['time_of_start']
        return x

    def __does_user_have_a_saved_code(self, user_id, solution_id):

        try:
            res = self.db_code.find_one({'solution_id': ObjectId(solution_id), 'author_id': ObjectId(user_id)})
        except ConnectionError:
            raise ConnectionError("Failed to connect to db")

        return res is not None

    def __save_code(self, info):
        insertionData = {
            'code': info['code'],
            'language': info['language'],
            'shared': 0,
            'tests_passed': info['passed'],
            'tests_total': info['total'],
            'test_failed': info['results'],
            'timestamp': datetime.datetime.now(),
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
            'score': -1,
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

    def comment_solution(self, solution_id, comment):
        if not ObjectId.is_valid(ObjectId(solution_id)):
            return {"status": "error_invalid_solution_id", "message": "Invalid solution_id."}

        try:
            self.db_problems.update_one(
                {'solutions.solution_id': ObjectId(solution_id)},
                {'$push': {'solutions.$.comments': comment}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")
        return {'status': 'OK', 'message': 'Successfully set a comment'}

    def grade_solution(self, solution_id, grade):
        if not ObjectId.is_valid(ObjectId(solution_id)):
            return {"status": "error_invalid_solution_id", "message": "Invalid solution_id."}

        try:
            self.db_problems.update_one(
                {'solutions.solution_id': ObjectId(solution_id)},
                {'$set': {'solutions.$.score': grade}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")
        return {'status': 'OK', 'message': 'Successfully graded the solution'}

    def create_solution_with_time_limit(self, user_id, problem_id):

        solution_id = ObjectId.from_datetime(datetime.datetime.now())

        insertionData = {
            'solution_id': solution_id,
            'author_id': ObjectId(user_id),
            'score': -1,
            'comments': [],
            'code_ids': [],
            'time_of_start': datetime.datetime.now()
        }

        try:
            self.db_problems.update_one({'_id': ObjectId(problem_id)}, {'$push': {'solutions': insertionData}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

    def init_solution_with_time_limit(self, info):
        info['problem_id'] = ObjectId(info['problem_id'])
        info['user_id'] = ObjectId(info['user_id'])
        if not ObjectId.is_valid(info['problem_id']):
            return {"status": "error_invalid_problem_id", "message": "Invalid problem id."}

        if not ObjectId.is_valid(info['user_id']):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        allowed_time_for_solution = int(info['time_limit']) * 60

        if self.__does_user_have_a_solution(info['user_id'], info['problem_id']):
            time_start_timestamp = self.__get_solution_time_of_start(info['user_id'], info['problem_id'])
            now = datetime.datetime.now()
            delta = now - time_start_timestamp
            if delta.seconds < allowed_time_for_solution:
                return {'status': 'OK', 'message': (allowed_time_for_solution - delta.seconds)}
            else:
                return {'status': 'error_time_is_out', 'message': 'Time ran out.'}

        else:
            self.create_solution_with_time_limit(info['user_id'], info['problem_id'])
            return {'status': 'OK', 'message': allowed_time_for_solution}


import bson.json_util
from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure
from datetime import datetime
import re
import locale
from operator import itemgetter


class HandleProblemsClass:
    def __init__(self, mongo_client):
        self.db_problems = mongo_client["Main"]["Problems"]
        self.db_groups = mongo_client["Main"]["Groups"]
        self.db_code = mongo_client["Main"]["Code"]
        self.db_users = mongo_client["Main"]["Users"]
        self.patterns = {
            'array': ['масив', 'array'],
            'string': ['низ', 'стринг', 'string'],
            'linked-list': ['linked-list', 'свързан списък'],
            'tree': ['дърв', 'tree'],
            'stack': ['stack', 'стек'],
            'list': ['списък', 'list'],
            'queue': ['опашка', 'queue']
        }

    def __insert_problem_id_to_group(self, problem_id, group_id):
        try:
            self.db_groups.update_one(
                {'_id': ObjectId(group_id)},
                {'$push': {'problems': ObjectId(problem_id)}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

    def does_user_have_access(self, user_id, problem_id):

        if not ObjectId.is_valid(problem_id):
            return {"status": "error_invalid_problem_id", "message": "Invalid problem id."}

        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user id."}

        try:
            is_in_group = self.db_groups.find_one({
                'problems': {
                    '$in': [ObjectId(problem_id)]
                },
                'users': {
                    '$in': [ObjectId(user_id)]
                }})
            problem = self.db_problems.find_one({'_id': ObjectId(problem_id), 'public': True})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        if problem is not None:
            return {'status': 'OK', 'has_access': bool(problem['public']) or is_in_group is not None}
        else:
            return {'status': 'OK', 'has_access': is_in_group is not None}

    def create_problem(self, info):

        # Началната дата и крайната дата се очакват във формат yyyy-mm-dd-hh-mm-ss (2021-12-23-23-59-59)
        # Подадената дата е във формат: yyyy-mm-ddThh:mm
        start_date = info['start_date'].replace('T', '-').replace(':', '-').split('-')
        start_date.append('00')
        # Секундите не могат да се избират от timepicker-а затова се добавят тук

        # Целта е да се преобразува полученият timestamp във формат удобен за MongoDB както и за четене от хора
        # Добавя се година, месец и ден със разделител "-". След това се добавят час, минути и секудни със разделител :
        # Между датата и часът има разделителна буква "T"
        start_date_string = "-".join(start_date[:3]) + "T" + ":".join(start_date[3:])

        start_date_mongo_string = datetime.strptime(start_date_string, "%Y-%m-%dT%H:%M:%S")

        end_date = info['end_date'].replace('T', '-').replace(':', '-').split('-')
        end_date.append('00')

        end_date_string = "-".join(end_date[:3]) + "T" + ":".join(end_date[3:])

        end_date_mongo_string = datetime.strptime(end_date_string, "%Y-%m-%dT%H:%M:%S")

        insertionData = {
            'title': info['title'],
            'public': info['public'] == 'true' and True or False,
            'tags': [tag.strip().lower() for tag in info['tags'].split(',')],
            'text': info['text'],
            'tests': loads(info['tests']),
            'solutions': [],
            'start_date': start_date_mongo_string,
            'end_date': end_date_mongo_string,
            'time_limit': info['time_limit'],
            'attempts': '0',
            'difficulty': info['difficulty']
            }

        try:
            res = self.db_problems.insert_one(insertionData)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        for group in info['groups_to_add_problem']:
            self.__insert_problem_id_to_group(res.inserted_id, group)

        return {"status": "OK", "message": "successfully created a problem."}

    def get_all_problems(self, difficulty, tags, name):

        options = {
            'public': True
        }
        if difficulty != 'any':
            options['difficulty'] = difficulty

        if tags != 'any':

            tags = self.patterns[tags]

            # Тука се прави regex за таговете
            for index, value in enumerate(tags):
                # tags[index] = '/' + value + '.*/'
                tags[index] = re.compile(value + '.*', re.IGNORECASE)
            options['tags'] = {'$in': tags}

        if name != '':
            options['title'] = re.compile('.*' + name + '.*', re.IGNORECASE)

        try:
            # db.Problems.find({tags: {$all:[/масив.*/, /функци.*/]}})
            problems = self.db_problems.find(options, {'solutions': 0})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        problems = list(problems)

        for problem in problems:
            problem['_id'] = str(problem['_id'])

        return {'status': 'OK', 'message': problems}

    def get_solutions_for_group(self, problem_id: str, user_id: str, group_problem_ids: list):

        for index, value in enumerate(group_problem_ids):
            if not ObjectId.is_valid(value):
                return {"status": "error_invalid_problem_id", "message": "Invalid problem id."}
            else:
                group_problem_ids[index] = ObjectId(value)

        options = {
            '_id': {'$in': group_problem_ids}
        }

        if problem_id != 'any':
            if not ObjectId.is_valid(problem_id):
                return {"status": "error_invalid_problem_id", "message": "Invalid problem id."}

            options['_id'] = ObjectId(problem_id)

        try:
            problems = self.db_problems.find(options, {'title': 1, 'solutions': 1, '_id': 0})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        problems = list(problems)

        if user_id != 'any':
            for problem in problems:
                for solve in problem['solutions']:
                    if user_id != str(solve['author_id']):
                        problem['solutions'].remove(solve)

        for problem in problems:

            for solve in problem['solutions']:

                solve['code_ids'] = len(solve['code_ids'])
                del solve['comments']
                solve['author_id'] = str(solve['author_id'])
                solve['solution_id'] = str(solve['solution_id'])

        return {'status': 'OK', 'message': loads(bson.json_util.dumps(problems))}

    def get_solution_by_id(self, solution_id: str):
        if solution_id != 'any' and not ObjectId.is_valid(solution_id):
            return {"status": "error_invalid_solution_id", "message": "Invalid solution_id."}

        try:
            submissions = self.db_code.find({'solution_id': ObjectId(solution_id)})
            problem_name = self.db_problems.find_one({
                'solutions': {
                    '$elemMatch': {
                        'solution_id': ObjectId(solution_id)
                    }
                }
            },{
                'title': 1,
                '_id': 0,
                'solutions.$': 1
            })
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        submissions = list(submissions)

        locale.setlocale(locale.LC_ALL, 'bg_BG')

        for submission in submissions:
            submission['_id'] = str(submission['_id'])
            submission['solution_id'] = str(submission['solution_id'])
            submission['author_id'] = str(submission['author_id'])
            submission['timestamp'] = submission['timestamp'].strftime('%x %X')

        try:
            author_name = self.db_users.find_one({'_id': ObjectId(problem_name['solutions'][0]['author_id'])},
                                                 {'name': 1, '_id': 0})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        if len(submissions) == 0:
            return {
                'status': 'error_no_submissions',
                'message': submissions,
                'author_name': author_name['name'],
                'problem_name': problem_name['title']
            }

        return {
            'status': 'OK',
            'message': submissions,
            'author_name': author_name['name'],
            'problem_name': problem_name['title']
        }

    def get_problem_by_solution_id(self, solution_id: str):
        if not ObjectId.is_valid(solution_id):
            return {"status": "error_invalid_solution_id", "message": "Invalid solution_id."}

        try:
            problem_info = self.db_problems.find_one({
                'solutions': {
                    '$elemMatch': {
                        'solution_id': ObjectId(solution_id)
                    }
                }
            },{
                'title': 1,
                '_id': 1,
                'public': 1,
                'solutions.$': 1
            })
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")
        problem_info['score'] = problem_info['solutions'][0]['score']
        problem_info['comments'] = problem_info['solutions'][0]['comments']
        del problem_info['solutions']
        return problem_info

    def get_my_solutions(self, user_id: str):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        data_to_get = {
            'test_failed': 0,
            'code': 0,
            'comments': 0,
            'author_id': 0
        }

        try:
            results = self.db_code.find({'author_id': ObjectId(user_id)}, data_to_get)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        results = list(results)

        locale.setlocale(locale.LC_ALL, 'bg_BG')

        for problem in results:
            if 'solution_id' in problem:
                problem['problem'] = self.get_problem_by_solution_id(problem['solution_id'])
            problem['timestamp'] = problem['timestamp'].strftime('%x %X')

        return {'status': 'OK', 'message': loads(bson.json_util.dumps(results))}

    def get_shared_solutions(self, user_id: str):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        data_to_get = {
            'test_failed': 0,
            'code': 0,
            'comments': 0,
            'score': 0,
            'author_id': 0
        }

        try:
            results = self.db_code.find({'author_id': ObjectId(user_id), 'shared': 1}, data_to_get)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        results = list(results)

        locale.setlocale(locale.LC_ALL, 'bg_BG')

        for problem in results:
            problem['problem'] = self.get_problem_by_solution_id(problem['solution_id'])
            problem['timestamp'] = problem['timestamp'].strftime('%x %X')

        return {'status': 'OK', 'message': loads(bson.json_util.dumps(results))}

    def get_code_info(self, code_id, user_id):

        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        if not ObjectId.is_valid(code_id):
            return {"status": "error_invalid_code_id", "message": "Invalid code_id."}

        try:
            info = self.db_code.find_one({'_id': ObjectId(code_id)})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        if info['author_id'] != ObjectId(user_id) and info['shared'] == 0:
            return {'status': 'error_no_access', 'message': 'User doesnt have access to this code'}

        try:
            author_name = self.db_users.find_one({'_id': ObjectId(info['author_id'])},
                                                 {'name': 1, '_id': 0})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        locale.setlocale(locale.LC_ALL, 'bg_BG')
        info['timestamp'] = info['timestamp'].strftime('%x %X')
        info['author_name'] = author_name['name']

        if 'solution_id' in info:
            problem_info = self.get_problem_by_solution_id(info['solution_id'])
            info['problem_name'] = problem_info['title']
            info['problem_public'] = problem_info['public']
            info['comments'] = problem_info['comments']
        else:
            info['problem_name'] = info['name'] + "(Кодова площадка)"
            info['problem_public'] = True
            info['comments'] = []

        return {'status': 'OK', 'message': loads(bson.json_util.dumps(info))}

    def share_solution(self, code_id, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        if not ObjectId.is_valid(code_id):
            return {"status": "error_invalid_code_id", "message": "Invalid code_id."}

        try:
            self.db_code.update_one({'_id': ObjectId(code_id)}, {'$set': {'shared': 1}})
            self.db_users.update_one({'_id': ObjectId(user_id)}, {'$push': {'shared_code_ids': ObjectId(code_id)}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {'status': 'OK', 'message': 'Successfully shared the code.'}


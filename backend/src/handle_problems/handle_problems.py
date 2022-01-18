from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure
import datetime


class HandleProblemsClass:
    def __init__(self, mongo_client):
        self.db_problems = mongo_client["Main"]["Problems"]
        self.db_groups = mongo_client["Main"]["Groups"]

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
            is_in_group = self.db_groups.find_one({'problems': [ObjectId(problem_id)], 'users': [ObjectId(user_id)]})
            problem = self.db_problems.find_one({'_id': ObjectId(problem_id)}, {'public': 1})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {'status': 'OK', 'has_access': bool(problem['public']) or is_in_group is not None}

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

        start_date_mongo_string = datetime.datetime.strptime(start_date_string, "%Y-%m-%dT%H:%M:%S")

        end_date = info['end_date'].replace('T', '-').replace(':', '-').split('-')
        end_date.append('00')

        end_date_string = "-".join(end_date[:3]) + "T" + ":".join(end_date[3:])

        end_date_mongo_string = datetime.datetime.strptime(end_date_string, "%Y-%m-%dT%H:%M:%S")

        insertionData = {
            'title': info['title'],
            'public': info['public'] == 'true' and True or False,
            'tags': [tag.strip() for tag in info['tags'].split(',')],
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

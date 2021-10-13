from bson.objectid import ObjectId
from json import dumps
from pymongo.errors import ConnectionFailure
import datetime


class HandleProblemsClass:
    def __init__(self):
        pass

    def create_problem(self, info, mongo_client):
        db = mongo_client["Main"]
        db = db["Problems"]

        # Началната дата и крайната дата се очакват във формат yyyy-mm-dd-hh-mm-ss (2021-12-23-23:59-59)

        start_date = info['start_date'].split('-')

        start_date_string = start_date[0] + '-' + start_date[1] + '-' + start_date[2] + 'T' + start_date[3] + ':' + \
            start_date[4] + ":" + start_date[5] + '.000Z'

        start_date_mongo_string = datetime.datetime.strptime(start_date_string, "%Y-%m-%dT%H:%M:%S.000Z")

        end_date = info['end_date'].split('-')

        end_date_string = end_date[0] + '-' + end_date[1] + '-' + end_date[2] + 'T' + end_date[3] + ':' + \
            end_date[4] + ":" + end_date[5] + '.000Z'

        end_date_mongo_string = datetime.datetime.strptime(end_date_string, "%Y-%m-%dT%H:%M:%S.000Z")

        insertionData = {
            'title': info['title'],
            'public': info['public'] == 'true' and True or False,
            'tags': info['tags'],
            'text': info['text'],
            'tests': [],
            'solutions': [],
            'start_date': start_date_mongo_string,
            'end_date': end_date_mongo_string,
            'time_limit': info['time_limit'],
            'attempts': '0'
            }

        try:
            db.insert_one(insertionData)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return dumps({"status": "OK", "message": "successfully created a problem."})

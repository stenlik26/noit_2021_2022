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

        # TODO: Това тука трябва да се помисли. Как ще получим датата и часа от frontend-а
        d = datetime.datetime.strptime("2021-11-26T23:55:55.000Z", "%Y-%m-%dT%H:%M:%S.000Z")

        insertionData = {
            'title': info['title'],
            'public': info['public'] == 'true' and True or False,
            'tags': info['tags'],
            'text': info['text'],
            'tests': [],
            'solutions': [],
            'start_date': d,
            'end_date': d,
            'time_limit': info['time_limit'],
            'attempts': '0'
            }

        try:
            db.insert_one(insertionData)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return dumps({"status": "OK", "message": "successfully created a problem."})

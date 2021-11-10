from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure
import datetime


class HandleProblemsClass:
    def __init__(self):
        pass

    def create_problem(self, info, mongo_client):
        db = mongo_client["Main"]
        db = db["Problems"]

        # Началната дата и крайната дата се очакват във формат yyyy-mm-dd-hh-mm-ss (2021-12-23-23-59-59)
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
            'tags': info['tags'].split(','),
            'text': info['text'],
            'tests': loads(info['tests']),
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

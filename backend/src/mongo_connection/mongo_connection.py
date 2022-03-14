import pymongo
import json
import os


def get_connection():
    print(os.getcwd())
    with open('/var/www/noit_2021_2022/backend/src/mongo_connection/app_config.json') as json_file:
        data = json.load(json_file)

        if data['user'] == 'localhost':
            out = "mongodb://localhost:27017/"
        else:
            out = "mongodb+srv://" + data['user'] + \
                  ":" + data['pass'] + \
                  "@" + data['address'] + \
                  "/" + data['dbName'] + \
                  "?retryWrites=true&w=majority"
        return pymongo.MongoClient(out)


def get_executor_address():
    with open('/var/www/noit_2021_2022/backend/src/mongo_connection/app_config.json') as json_file:
        data = json.load(json_file)
        return data['executor_address']


def get_jwt_key():
    with open('/var/www/noit_2021_2022/backend/src/mongo_connection/app_config.json') as json_file:
        data = json.load(json_file)
        return data['jwt_key']
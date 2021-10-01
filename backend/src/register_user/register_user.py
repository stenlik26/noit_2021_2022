from bson.objectid import ObjectId
from json import dumps
from pymongo import errors


class RegisterUserClass:
    def __init__(self):
        pass

    def __registerUser(self, post_info, mongo_client):

        try:

            db = mongo_client["Main"]
            db = db["Users"]

            nameCheck = db.find_one({"name": post_info['name']})
            if nameCheck:
                return dumps({"status": "error_name_exists", "message": "Name is in use."})

            emailCheck = db.find_one({"email": post_info['email']})
            if emailCheck:
                return dumps({"status": "error_email_exists", "message": "Email already registered."})

        except errors.ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        insertionData = {
            "username": post_info['username'],
            "name": post_info['name'],
            "email": post_info['email'],
            "password": post_info['password'],
            "picture": '',
            "groups": [],
            "files_created_by_user": [],
            "friends": [],
            "description": '',
            "role": '0'
            }

        try:
            db.insert_one(insertionData)
        except errors.ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return dumps({"status": "OK", "message": "successfully created an account."})

    def run(self, post_info, mongo_client):
        return self.__registerUser(post_info, mongo_client)


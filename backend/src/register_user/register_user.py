from bson.objectid import ObjectId
from json import dumps


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

            insertionData = {
                "username": post_info['username'],
                "name": post_info['name'],
                "email": post_info['email'],
                "password": post_info['password'],
                "picture": '',
                "groups": [],
                "file_created_by_user": [],
                "friends": [],
                "description": '',
                "role": '0'
                }
            db.insert_one(insertionData)
            return dumps({"status": "OK", "message": "successfully created an account."})

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return dumps({"status": "error", "message": message})

    def run(self, post_info, mongo_client):
        return self.__registerUser(post_info, mongo_client)


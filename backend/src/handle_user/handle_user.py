from bson.objectid import ObjectId
from json import loads
from bson import json_util
from pymongo.errors import ConnectionFailure


class HandleUserClass:
    def __init__(self, mongo_client):
        self.db_user = mongo_client['Main']['Users']

    def get_profile_info(self, profile_id):
        if not ObjectId.is_valid(profile_id):
            return {"status": "error_invalid_profile_id", "message": "Invalid profile_id."}

        data_to_get = {
            'name': 1,
            'email': 1,
            'picture': 1,
            'description': 1,
            'shared_code_ids': 1
        }

        try:
            info = self.db_user.find_one({'_id': ObjectId(profile_id)}, data_to_get)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        info['_id'] = str(info['_id'])

        return {'status': 'OK', 'message': loads(json_util.dumps(info))}

    def change_profile_name(self, profile_id, new_name):
        if not ObjectId.is_valid(profile_id):
            return {"status": "error_invalid_profile_id", "message": "Invalid profile_id."}

        try:
            self.db_user.update_one({'_id': ObjectId(profile_id)}, {'$set': {'name': new_name}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {'status': 'OK', 'message': 'Successfully changed user name'}

    def change_description(self, profile_id, new_desc):
        if not ObjectId.is_valid(profile_id):
            return {"status": "error_invalid_profile_id", "message": "Invalid profile_id."}

        try:
            self.db_user.update_one({'_id': ObjectId(profile_id)}, {'$set': {'description': new_desc}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {'status': 'OK', 'message': 'Successfully changed user description'}
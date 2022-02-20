from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure
from typing import Dict
import datetime
from backend.src.mongo_connection.mongo_connection import get_executor_address
import requests
import codecs


class UploadCodePlaygroundClass:
    def __init__(self, mongo_client):
        self.db_code = mongo_client['Main']['Code']

    def upload_code(self, info: dict) -> Dict[str, str]:
        if not ObjectId.is_valid(info['user_id']):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        code_id = ObjectId(self.__save_to_db(info))

        return {'status': 'OK', 'message': str(code_id)}

    def __save_to_db(self, info):
        insertion_data = {
            'code': info['code'],
            'language': info['language'],
            'shared': 0,
            'author_id': ObjectId(info['user_id']),
            'comments': []
        }

        try:
            x = self.db_code.insert_one(insertion_data)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")
        return x.inserted_id

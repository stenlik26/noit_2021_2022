from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure
from typing import Dict, Optional
from backend.src.mongo_connection.mongo_connection import get_executor_address


class UploadCodePlaygroundClass:
    def __init__(self, mongo_client):
        self.db_code = mongo_client['Main']['Code']

    def upload_code(self, info: dict) -> Dict[str, str]:
        author_id = info['user_id']

        if not ObjectId.is_valid(info['user_id']):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        name = info['name']
        existing_code_id = self.__get_user_code_id_with_name(author_id, name)['_id']

        print(f"Existing code id = {existing_code_id}")
        if existing_code_id is None:
            # New entry
            code_id = self.__create_code(info['code'], name, info['language'], author_id)
        else:
            # Update
            print("Updating...")
            code_id = existing_code_id
            self.__update_code(info['code'], info['language'], code_id)

        return {'status': 'OK', 'message': str(code_id)}

    def __create_code(self, code: str, name: str, language: str, author_id: str) -> ObjectId:
        insertion_data = {
            'code': code,
            'name': name,
            'language': language,
            'shared': 0,
            'author_id': ObjectId(author_id),
            'comments': []
        }

        try:
            insert_result = self.db_code.insert_one(insertion_data)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")
        return insert_result.inserted_id

    def __update_code(self, new_code: str, new_language: str, code_id: ObjectId):
        try:
            print(f"code_id = {code_id}")
            print(f"new_code = {new_code}")
            print(f"new_language = {new_language}")
            res = self.db_code.update(
                {'_id': code_id},
                {"$set": {'code': new_code, 'language': new_language}}
            )
            # print(f"res = {res.acknowledged}")
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

    def __get_user_code_id_with_name(self, author_id: str, name: str) -> Optional[ObjectId]:
        try:
            code_id = self.db_code.find_one(
                {'author_id': ObjectId(author_id), 'name': name},
                {'_id': 1})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return code_id

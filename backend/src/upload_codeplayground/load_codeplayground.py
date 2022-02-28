from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure


class LoadCodePlayground:
    def __init__(self, mongo_client):
        self.db_code = mongo_client['Main']['Code']

    def get_code_by_object_id(self, info: dict):
        if not ObjectId.is_valid(info['user_id']):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        try:
            result = self.db_code.find_one(
                {'_id': ObjectId(info['code_id'])},
                {'_id': 0, 'code': 1, 'name': 1, 'language': 1}
            )
        except ConnectionFailure:
            return ConnectionError("Failed to connect")

        return result

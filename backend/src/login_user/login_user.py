from bson.objectid import ObjectId
from json import dumps
import datetime
import jwt
import time
from pymongo.errors import ConnectionFailure
from backend.src.mongo_connection.mongo_connection import get_jwt_key


class LoginUserClass:
    def __init__(self):
        pass

    def __encode_user_token(self, user_id: str) -> str:

        if not ObjectId.is_valid(user_id):
            return "invalid_object_id"

        payload_info = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }

        return jwt.encode(
            payload_info,
            get_jwt_key(),
            algorithm="HS256"
        )

    def give_guest_token(self, post_time_stamp: str) -> str:

        payloadInfo = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': 'guestToken' + str(post_time_stamp)
        }

        return jwt.encode(
            payloadInfo,
            get_jwt_key(),
            algorithm='HS256'
        )

    @staticmethod
    def validate_token(token: str) -> str:
        try:
            result = jwt.decode(token, get_jwt_key(), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return dumps({'status': 'error_token_expired', 'message': 'Expired token!'})
        except jwt.InvalidTokenError:
            return dumps({'status': 'error_invalid_token', 'message': 'Invalid token!'})

        if 'guest' in result['sub']:
            return dumps({'status': 'OK', 'userType': 'guest', 'siteAccess': False})
        else:
            return dumps({'status': 'OK', 'userType': 'user', 'siteAccess': True})

    @staticmethod
    def get_user_id_from_token(token: str) -> str:
        try:
            result = jwt.decode(token, get_jwt_key(), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return dumps({'status': 'error_token_expired', 'message': 'Expired token!'})
        except jwt.InvalidTokenError:
            return dumps({'status': 'error_invalid_token', 'message': 'Invalid token!'})

        return result['sub']

    def login_panel(self, input_email: str, input_pass: str, mongo_connection) -> str:
        db = mongo_connection['Main']
        db = db['Users']

        try:
            user = db.find_one({'email': input_email})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        if not user:
            return dumps({"status": "error_no_such_user", "message": "No such user."})

        if input_pass == user['password']:
            return dumps({"status": "OK", "token": self.__encode_user_token(str(user['_id'])), "userId": str(user['_id'])})
        else:
            return dumps({"status": "error_wrong_password", "message": "Wrong password"})







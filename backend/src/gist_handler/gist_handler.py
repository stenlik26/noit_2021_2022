from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure


class GistModule:
    def __init__(self, mongo_connection):
        self.db_users = mongo_connection["Main"]["Users"]

    def set_github_token(self, github_token, user_id):

        if not ObjectId.is_valid(user_id):
            return {'status': 'error_invalid_userid', 'message': 'User objectId is not valid'}

        try:
            self.db_users.update_one({'_id': ObjectId(user_id)}, {'$set':
                                                                      {'github_token': github_token}
                                                                  })
        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

        return {'status': 'OK', 'message': "Updated github token."}

    def get_github_token(self, user_id):
        if not ObjectId.is_valid(user_id):
            return {'status': 'error_invalid_userid', 'message': 'User objectId is not valid'}

        try:
            res = self.db_users.find_one({'_id': ObjectId(user_id)})
        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

        return {'status': 'OK', 'message': res['github_token']}



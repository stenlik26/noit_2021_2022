from bson.objectid import ObjectId
from json import dumps
from pymongo.errors import ConnectionFailure
import datetime


class HandleGroupsClass:
    def __init__(self):
        pass

    def get_user_group_invites(self, mongo_client, my_user_id):
        db = mongo_client["Main"]
        db = db["Users"]

        user_info = {'_id': ObjectId(my_user_id)}
        data_to_get = {'_id': 1, 'group_invites': 1}

        try:
            data = list(db.find(user_info, data_to_get))
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        data = data[0]

        data['_id'] = str(data['_id'])
        for group in data['group_invites']:
            group['from_user_id'] = str(group['from_user_id'])
            group['for_group_id'] = str(group['for_group_id'])

        return {"status": "OK", "message": data}

    def send_group_invite(self, mongo_client, admin_user_id, group_id, invited_user_id):

        db = mongo_client["Main"]
        db = db["Users"]

        invite = {
            'from_user_id': ObjectId(admin_user_id),
            'for_group_id': ObjectId(group_id)
        }

        user_info = {'_id': ObjectId(invited_user_id)}
        user_group_invites = {'$push': {'group_invites': invite}}

        try:
            db.update_one(user_info, user_group_invites)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "successfully sent a group invite"}

    def reject_group_invite(self, mongo_client, group_id, my_user_id):
        db = mongo_client["Main"]
        db = db["Users"]

        user_info = {'_id': ObjectId(my_user_id)}
        user_group_invites = {'$pull': {'group_invites': {'for_group_id': ObjectId(group_id)}}}

        try:
            db.update_one(user_info, user_group_invites)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "successfully rejected a group invite"}

    def create_group(self, mongo_client, info):

        # Needed info from main: - name, creator id, invited users

        db = mongo_client["Main"]
        db = db["Groups"]

        insertionData = {
            'name': info['group_name'],
            'users': [ObjectId(info['user_id'])],
            'admins': [ObjectId(info['user_id'])],
            'shared_files': '',
            'chat': '',
            'problems': []
            }

        try:
            db.insert_one(insertionData)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "Successfully created a group."}

from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure


class HandleGroupsClass:
    def __init__(self):
        pass

    def get_user_group_invites(self, mongo_client, my_user_id):
        db = mongo_client["Main"]
        db = db["Users"]

        if not ObjectId.is_valid(my_user_id):
            return dumps({"status": "error_invalid_userid", "message": "Userid was invalid"})

        user_info = {'_id': ObjectId(my_user_id)}
        data_to_get = {'_id': 0, 'group_invites': 1}

        try:
            data = db.find_one(user_info, data_to_get)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        for group in data['group_invites']:
            group['from_user_id'] = str(group['from_user_id'])
            group['for_group_id'] = str(group['for_group_id'])

        return dumps({"status": "OK", "message": data})

    def send_group_invite(self, mongo_client, info):

        db = mongo_client["Main"]
        db = db["Users"]

        if not ObjectId.is_valid(info['admin_user_id']):
            return dumps({"status": "error_invalid_admin_userid", "message": "Admin userid was invalid"})

        if not ObjectId.is_valid(info['group_id']):
            return dumps({"status": "error_invalid_group_id", "message": "Group id was invalid"})

        if not ObjectId.is_valid(info['invited_user_id']):
            return dumps({"status": "error_invalid_invited_user_id", "message": "Invited user id was invalid"})

        invite = {
            'from_user_id': info['admin_user_id'],
            'for_group_id': info['group_id']
        }

        user_invites = loads(self.get_user_group_invites(mongo_client, info['invited_user_id']))

        user_invites = user_invites['message']['group_invites']

        for user_invite in user_invites:
            if invite == user_invite:
                return {"status": "error_user_is_invited", "message": "User is already invited."}

        for key in invite:
            invite[key] = ObjectId(invite[key])

        user_info = {'_id': ObjectId(info['invited_user_id'])}
        user_group_invites = {'$push': {'group_invites': invite}}

        try:
            db.update_one(user_info, user_group_invites)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return dumps({"status": "OK", "message": "successfully sent a group invite"})

    def reject_group_invite(self, mongo_client, group_id, my_user_id):
        db = mongo_client["Main"]
        db = db["Users"]

        if not ObjectId.is_valid(my_user_id):
            return dumps({"status": "error_invalid_userid", "message": "Userid was invalid"})

        if not ObjectId.is_valid(group_id):
            return dumps({"status": "error_invalid_group_id", "message": "Group id was invalid"})

        user_info = {'_id': ObjectId(my_user_id)}
        user_group_invites = {'$pull': {'group_invites': {'for_group_id': ObjectId(group_id)}}}

        try:
            db.update_one(user_info, user_group_invites)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return dumps({"status": "OK", "message": "successfully rejected a group invite"})

    def accept_group_invite(self, mongo_client, group_id, my_user_id):
        db = mongo_client["Main"]
        db = db["Users"]

        if not ObjectId.is_valid(my_user_id):
            return dumps({"status": "error_invalid_userid", "message": "Userid was invalid"})

        if not ObjectId.is_valid(group_id):
            return dumps({"status": "error_invalid_group_id", "message": "Group id was invalid"})

        user_info = {'_id': ObjectId(my_user_id)}
        user_group_invites = {'$pull': {'group_invites': {'for_group_id': ObjectId(group_id)}}}

        try:
            db.update_one(user_info, user_group_invites)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        user_group_invites = {'$push': {'groups': ObjectId(group_id)}}

        try:
            db.update_one(user_info, user_group_invites)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        db = mongo_client["Main"]
        db = db["Groups"]

        group_info = {'_id': ObjectId(group_id)}
        users_in_group = {'$push': {'users': ObjectId(my_user_id)}}

        try:
            db.update_one(group_info, users_in_group)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return dumps({"status": "OK", "message": "successfully accepted a group invite"})

    def create_group(self, mongo_client, info):

        # Needed info from main: - name, creator id, invited users

        db = mongo_client["Main"]
        db = db["Groups"]

        if not ObjectId.is_valid(info['user_id']):
            return dumps({"status": "error_invalid_userid", "message": "Userid was invalid"})

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

        return dumps({"status": "OK", "message": "Successfully created a group."})

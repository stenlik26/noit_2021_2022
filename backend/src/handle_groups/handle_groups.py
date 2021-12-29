from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure


class HandleGroupsClass:
    def __init__(self, mongo_client):
        self.db_users = mongo_client['Main']['Users']
        self.db_groups = mongo_client['Main']['Groups']

    def get_user_group_invites(self, my_user_id):

        if not ObjectId.is_valid(my_user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        user_info = {'_id': ObjectId(my_user_id)}
        data_to_get = {'_id': 0, 'group_invites': 1}

        try:
            data = self.db_users.find_one(user_info, data_to_get)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        for group in data['group_invites']:
            group['from_user_id'] = str(group['from_user_id'])
            group['for_group_id'] = str(group['for_group_id'])

        return {"status": "OK", "message": data}

    def send_group_invite(self, info):
        if not ObjectId.is_valid(info['admin_user_id']):
            return {"status": "error_invalid_admin_userid", "message": "Admin userid was invalid"}

        if not ObjectId.is_valid(info['group_id']):
            return {"status": "error_invalid_group_id", "message": "Group id was invalid"}

        if not ObjectId.is_valid(info['invited_user_id']):
            return {"status": "error_invalid_invited_user_id", "message": "Invited user id was invalid"}

        invite = {
            'from_user_id': info['admin_user_id'],
            'for_group_id': info['group_id']
        }

        user_invites = self.get_user_group_invites(info['invited_user_id'])

        user_invites = user_invites['message']['group_invites']

        if invite in user_invites:
            return {"status": "error_user_is_invited", "message": "User is already invited."}

        for key in invite:
            invite[key] = ObjectId(invite[key])

        user_info = {'_id': ObjectId(info['invited_user_id'])}
        user_group_invites = {'$push': {'group_invites': invite}}

        try:
            self.db_users.update_one(user_info, user_group_invites)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "successfully sent a group invite"}

    def __remove_group_invite(self, group_id, my_user_id):
        user_info = {'_id': ObjectId(my_user_id)}
        user_group_invites = {'$pull': {'group_invites': {'for_group_id': ObjectId(group_id)}}}

        try:
            self.db_users.update_one(user_info, user_group_invites)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

    def reject_group_invite(self, group_id, my_user_id):
        if not ObjectId.is_valid(my_user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_group_id", "message": "Group id was invalid"}

        self.__remove_group_invite(group_id, my_user_id)

        return {"status": "OK", "message": "successfully rejected a group invite"}

    def accept_group_invite(self, group_id, my_user_id):

        if not ObjectId.is_valid(my_user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_group_id", "message": "Group id was invalid"}

        self.__remove_group_invite(group_id, my_user_id)

        user_group_invites = {'$push': {'groups': ObjectId(group_id)}}
        user_info = {'_id': ObjectId(my_user_id)}

        try:
            self.db_users.update_one(user_info, user_group_invites)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        group_info = {'_id': ObjectId(group_id)}
        users_in_group = {'$push': {'users': ObjectId(my_user_id)}}

        try:
            self.db_groups.update_one(group_info, users_in_group)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "successfully accepted a group invite"}

    def create_group(self, info):

        # Needed info from main: - name, creator id, invited users

        if not ObjectId.is_valid(info['user_id']):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        insertionData = {
            'name': info['group_name'],
            'users': [ObjectId(info['user_id'])],
            'admins': [ObjectId(info['user_id'])],
            'shared_files': '',
            'chat': '',
            'problems': []
            }

        try:
            data = self.db_groups.insert_one(insertionData)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "Successfully created a group.", "group_id": str(data.inserted_id)}

    def get_all_users(self, my_user_id):

        if not ObjectId.is_valid(my_user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        try:
            users = self.db_users.find({}, {'name': 1, 'picture': 1})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        users = list(users)

        for user in users:
            user['_id'] = str(user['_id'])

        for index, entry in enumerate(users):
            if entry['_id'] == my_user_id:
                users.pop(index)

        return {'status': 'OK', 'message': users}

    def send_multiple_invites(self, admin_id, group_id, users_to_invite):
        if not ObjectId.is_valid(admin_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_group_id", "message": "group_id was invalid"}

        res = []

        for user_id in users_to_invite:
            res.append(self.send_group_invite({
                'admin_user_id': admin_id,
                'group_id': group_id,
                'invited_user_id': user_id
            })['status'])

        if all([y == 'OK' for y in res]):
            return {'status': 'OK', 'message': 'Successfully sent group invites.'}
        else:
            return {'status': 'error_invites_not_sent', 'message': res}





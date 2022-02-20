from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure
import bson.json_util
import locale
from datetime import datetime


class HandleGroupsClass:
    def __init__(self, mongo_client):
        self.db_users = mongo_client['Main']['Users']
        self.db_groups = mongo_client['Main']['Groups']
        self.db_problems = mongo_client['Main']['Problems']

    def get_user_group_invites(self, my_user_id):

        if not ObjectId.is_valid(my_user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        user_info = {'_id': ObjectId(my_user_id)}
        data_to_get = {'_id': 0, 'group_invites': 1}

        try:
            data = self.db_users.find_one(user_info, data_to_get)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        options = {'name': 1, '_id': 0}

        for group in data['group_invites']:
            group['from_user_string'] = self.db_users.find_one({'_id': group['from_user_id']}, options)['name']
            group['for_group_string'] = self.db_groups.find_one({'_id': group['for_group_id']}, options)['name']
            group['from_user_id'] = str(group['from_user_id'])
            group['for_group_id'] = str(group['for_group_id'])

        return {"status": "OK", "message": data['group_invites']}

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

        user_invites = user_invites['message']

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
            'users': [],
            'admins': [ObjectId(info['user_id'])],
            'shared_files': '',
            'chat': '',
            'problems': []
            }

        try:
            data = self.db_groups.insert_one(insertionData)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        self.accept_group_invite(data.inserted_id, info['user_id'])

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

    def get_groups_where_user_is_admin(self, admin_id):
        if not ObjectId.is_valid(admin_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        try:
            groups = self.db_groups.find({'admins': {'$in': [ObjectId(admin_id)]}}, {'name': 1})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        groups = list(groups)
        for group in groups:
            group['_id'] = str(group['_id'])

        return groups

    def get_user_access_level(self, user_id, group_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_userid", "message": "group_id was invalid"}

        try:
            group = self.db_groups.find_one({'users': {'$in': [ObjectId(user_id)]}, '_id': ObjectId(group_id)})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        if group is None:
            return {"status": 'error_no_access', "message": 'User doesn\'t have access to this group.'}
        else:
            if ObjectId(user_id) in group['admins']:
                return {"status": 'OK', "message": 'admin'}
            else:
                return {"status": 'OK', 'message': 'user'}

    def get_group_info(self, group_id, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_userid", "message": "group_id was invalid"}

        try:
            group_info = self.db_groups.find_one({'_id': ObjectId(group_id)}, {'_id': 0})
            users = list(self.db_users.find({
                '_id': {
                    '$in': group_info['users']
                }
            },
                {
                    'name': 1,
                    'email': 1,
                    'picture': 1
                }))
            problems = list(self.db_problems.find({
                '_id':
                    {
                         '$in': group_info['problems']
                    }
            },
                {
                    'title': 1,
                    'start_date': 1,
                    'end_date': 1,
                    'time_limit': 1
                }))

        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        for user in users:
            user['is_admin'] = user['_id'] in group_info['admins']
            user['_id'] = str(user['_id'])

        for index,value in enumerate(group_info['problems']):
            group_info['problems'][index] = str(value)

        group_info['users'] = users
        del group_info['admins']

        locale.setlocale(locale.LC_ALL, 'bg_BG')

        for problem in problems:
            now = datetime.now()
            problem['is_active'] = problem['start_date'] < now < problem['end_date']
            problem['start_date'] = problem['start_date'].strftime('%x %X')
            problem['end_date'] = problem['end_date'].strftime('%x %X')

        group_info['problems'] = problems

        return {'status': 'OK', 'message': loads(bson.json_util.dumps(group_info))}

    def make_user_admin(self, group_id, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_userid", "message": "group_id was invalid"}

        group_info = {'_id': ObjectId(group_id)}
        admin = {'$push': {'admins': ObjectId(user_id)}}

        try:
            self.db_groups.update_one(group_info, admin)

        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "User was given admin access."}

    def revoke_user_admin(self, group_id, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_userid", "message": "group_id was invalid"}

        group_info = {'_id': ObjectId(group_id)}
        admin = {'$pull': {'admins': ObjectId(user_id)}}

        try:
            self.db_groups.update_one(group_info, admin)

        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "User was revoked admin access."}

    def remove_user_from_group(self, group_id, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_userid", "message": "group_id was invalid"}

        group_info = {'_id': ObjectId(group_id)}
        admin = {'$pull': {'admins': ObjectId(user_id), 'users': ObjectId(user_id)}}

        try:
            self.db_groups.update_one(group_info, admin)

        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "User was removed from the group."}

    def change_group_name(self, group_id, new_group_name):
        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_userid", "message": "group_id was invalid"}

        group_info = {'_id': ObjectId(group_id)}
        name = {'$set': {'name': new_group_name}}

        try:
            self.db_groups.update_one(group_info, name)

        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {"status": "OK", "message": "Name was successfully changed."}

    def get_users_groups(self, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_userid", "message": "Userid was invalid"}

        query = {'users': {'$in': [ObjectId(user_id)]}}
        info_to_get = {'name': 1}

        try:
            groups = self.db_groups.find(query, info_to_get)
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        groups = list(groups)

        for group in groups:
            group['_id'] = str(group['_id'])

        return {'status': 'OK', 'message': groups}

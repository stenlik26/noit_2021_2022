import os
import pathlib
import shutil

import bson.json_util
from bson.objectid import ObjectId
from json import dumps, loads
from pymongo.errors import ConnectionFailure
from datetime import datetime
import locale


class AdminPanelClass:
    def __init__(self, mongo_client):
        self.db_users = mongo_client["Main"]["Users"]
        self.db_pictures = mongo_client['Main']['PictureForApproval']
        self.db_groups = mongo_client["Main"]["Groups"]

    def check_for_access(self, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        try:
            x = self.db_users.find_one({'_id': ObjectId(user_id)}, {'role': 1})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        if x['role'] == '1':
            return {'status': 'OK', 'message': 'Has access.'}
        else:
            return {'status': 'error_no_access', 'message': 'Doesn\'t have access.'}

    def admin_panel_info(self):
        try:
            users = list(self.db_users.find({}, {'name': 1, 'email': 1, 'role': 1, 'picture': 1}))
            groups = list(self.db_groups.find({}, {'name': 1, 'users': 1}))
            picture_for_approval = list(self.db_pictures.find())
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        locale.setlocale(locale.LC_ALL, 'bg_BG')

        for entry in picture_for_approval:
            usrName = self.db_users.find_one({'_id': ObjectId(entry['userId'])}, {'name': 1})
            entry['_id'] = str(entry['_id'])
            entry['user_name'] = usrName['name']
            entry['time'] = datetime.fromtimestamp(float(entry['time'])).strftime('%x %X')

        for entry in groups:
            entry['users'] = str(len(entry['users']))

        for entry in users:
            entry['_id'] = str(entry['_id'])
            entry['is_admin'] = (entry['role'] == '1')
            del entry['role']

        return {
            'status': 'OK',
            'users': loads(bson.json_util.dumps(users)),
            'groups': loads(bson.json_util.dumps(groups)),
            'pictures': loads(bson.json_util.dumps(picture_for_approval))
        }

    def make_user_admin(self, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        try:
            self.db_users.update_one({'_id': ObjectId(user_id)}, {'$set': {'role': "1"}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {'status': 'OK', 'message': 'Made this user admin.'}

    def revoke_user_admin(self, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        try:
            self.db_users.update_one({'_id': ObjectId(user_id)}, {'$set': {'role': "0"}})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {'status': 'OK', 'message': 'Revoked this user admin.'}

    def delete_group(self, group_id):
        if not ObjectId.is_valid(group_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        try:
            self.db_groups.delete_one({'_id': ObjectId(group_id)})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {'status': 'OK', 'message': 'Deleted this group.'}

    def delete_user(self, user_id):
        if not ObjectId.is_valid(user_id):
            return {"status": "error_invalid_user_id", "message": "Invalid user_id."}

        try:
            self.db_users.delete_one({'_id': ObjectId(user_id)})
        except ConnectionFailure:
            raise ConnectionError("Failed to connect to db")

        return {'status': 'OK', 'message': 'Deleted this user.'}

    def remove_unapproved_picture(self, picture_id):

        try:
            query = {'_id': ObjectId(picture_id)}
            res = self.db_pictures.find_one(query)

            filePath = res['path_Full']
            if os.path.exists(filePath):
                self.db_pictures.delete_one(query)
                os.remove(filePath)
                return {'status': 'OK', 'message': 'Picture successfully deleted.'}
            else:
                self.db_pictures.delete_one(query)
                return {'status': 'error_file_doesnt_exist', 'message': 'The file doesnt exist.'}

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}


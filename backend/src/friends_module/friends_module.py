import shutil

from bson.objectid import ObjectId
import json
from pymongo.errors import ConnectionFailure
import time
import pathlib
from datetime import datetime
import os


class FriendsModule:

    def __init__(self, mongo_connection):
        self.db_users = mongo_connection["Main"]["Users"]
        self.db_requests = mongo_connection["Main"]["FriendRequests"]

    def get_friends_list(self, user_id):
        friends_list = []
        try:
            res = self.db_users.find_one({'_id': ObjectId(user_id)}, {'friends': 1})

            for x in res['friends']:
                y = self.db_users.find_one({'_id': ObjectId(x)}, {'name': 1, 'picture': 1})
                y['_id'] = str(y['_id'])
                friends_list.append(y)

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

        return {'status': 'OK', 'message': friends_list}

    def remove_friend(self, friend_id, user_id):
        if not ObjectId.is_valid(friend_id):
            return {'status': 'error_invalid_friendid', 'message': 'Friend objectId is not valid'}

        if not ObjectId.is_valid(user_id):
            return {'status': 'error_invalid_userid', 'message': 'User objectId is not valid'}

        try:
            self.db_users.update_one({'_id': ObjectId(user_id)}, {'$pull': {'friends': ObjectId(friend_id)}})
            res = self.db_users.update_one({'_id': ObjectId(friend_id)}, {'$pull': {'friends': ObjectId(user_id)}})

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

        if res.modified_count == 1:
            return {'status': 'OK', 'message': 'Successfully removed friend.'}
        else:
            return {'status': 'error_no_such_friend', 'message': 'Friend isnt in friends list.'}

    def search_for_user(self, searched_name: str):
        try:
            output = list(self.db_users.find({
                'name': {
                    '$regex': '.*' + str(searched_name) + '.*',
                    '$options': 'i'
                }
            },
                {
                    'name': 1,
                    'picture': 1,
                    'email': 1
                }))

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

        for user in output:
            user['_id'] = str(user['_id'])

        return {'status': 'OK', 'message': output}

    def send_friend_request(self, sent_from_user_id, to_user_id):
        if not ObjectId.is_valid(sent_from_user_id):
            return {'status': 'error_invalid_sentFromUserId', 'message': 'Friend objectId is not valid'}

        if not ObjectId.is_valid(to_user_id):
            return {'status': 'error_invalid_toUserId', 'message': 'User objectId is not valid'}

        try:

            exists = self.is_my_friend(sent_from_user_id, to_user_id)

            if exists['message'] != 'not_friends':
                return exists

            input = {
                'sentFromUserId': ObjectId(sent_from_user_id),
                'toUserId': ObjectId(to_user_id)
            }

            self.db_requests.insert_one(input)

            return {'status': 'OK', 'message': 'Successfully sent friend request'}

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

    def is_my_friend(self, my_user_id, friend_user_id):
        if not ObjectId.is_valid(my_user_id):
            return {'status': 'error_invalid_myUserId', 'message': 'Friend objectId is not valid'}

        if not ObjectId.is_valid(friend_user_id):
            return {'status': 'error_invalid_friendUserId', 'message': 'User objectId is not valid'}

        if my_user_id == friend_user_id:
            return {'status': 'OK', 'message': 'same_acc'}

        try:

            res = list(self.db_requests.find({'sentFromUserId': ObjectId(my_user_id), 'toUserId': ObjectId(friend_user_id)}))

            if res:
                return {'status': 'OK', 'message': 'friend_request_sent'}

            res = list(self.db_requests.find({'toUserId': ObjectId(my_user_id), 'sentFromUserId': ObjectId(friend_user_id)}))

            if res:
                return {'status': 'OK', 'message': 'friend_request_received'}

            res = self.db_users.find_one({'_id': ObjectId(my_user_id)}, {'friends': 1})['friends']

            if ObjectId(friend_user_id) in res:
                return {'status': 'OK', 'message': 'friends'}

            return {'status': 'OK', 'message': 'not_friends'}

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

    def get_friend_requests(self, my_user_id):
        if not ObjectId.is_valid(my_user_id):
            return {'status': 'error_invalid_myUserId', 'message': 'Friend objectId is not valid'}

        try:
            res = list(self.db_requests.find({'toUserId': ObjectId(my_user_id)}))

            requestsList = []

            for x in res:
                t = self.db_users.find_one({'_id': ObjectId(x['sentFromUserId'])}, {'name': 1, 'picture': 1})
                t['_id'] = str(t['_id'])
                t['requestId'] = str(x['_id'])
                requestsList.append(t)

            return {'status': 'OK', 'message': requestsList}

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

    def remove_friend_request(self, request_id):
        if not ObjectId.is_valid(request_id):
            return {'status': 'error_invalid_myUserId', 'message': 'Friend objectId is not valid'}

        try:
            self.db_requests.delete_one({'_id': ObjectId(request_id)})

            return {'status': 'OK', 'message': 'Successfully deleted friendRequest'}

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

    def approve_friend_request(self, request_id):
        if not ObjectId.is_valid(request_id):
            return {'status': 'error_invalid_myUserId', 'message': 'Friend objectId is not valid'}

        try:

            res = self.db_requests.find_one({'_id': ObjectId(request_id)})

            fromUserId = res['sentFromUserId']
            toUserId = res['toUserId']

            self.db_requests.delete_one({'_id': ObjectId(request_id)})

            query = {"_id": ObjectId(fromUserId)}
            newValue = {"$push": {"friends": ObjectId(toUserId)}}
            self.db_users.update_one(query, newValue)

            query = {"_id": ObjectId(toUserId)}
            newValue = {"$push": {"friends": ObjectId(fromUserId)}}
            self.db_users.update_one(query, newValue)

            return {'status': 'OK', 'message': 'Successfully approved friendRequest'}

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}



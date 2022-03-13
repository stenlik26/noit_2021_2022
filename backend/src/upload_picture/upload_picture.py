import shutil

from bson.objectid import ObjectId
import json
from pymongo.errors import ConnectionFailure
import time
import pathlib
from datetime import datetime
import os


class PictureUpload:
    def __init__(self, mongo_connection):
        self.db_users = mongo_connection["Main"]["Users"]
        self.db_pictures = mongo_connection['Main']['PictureForApproval']

    def __splitall(self, path):
        allparts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path:  # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])
        return allparts

    def upload_picture_for_approval(self, user_id, file):

        nameOfFile = user_id + "@" + str(datetime.now())[:-7]
        nameOfFile = nameOfFile.replace(' ', '_')
        nameOfFile = nameOfFile.replace(':', '-')
        nameOfFile = nameOfFile + '.png'

        current_path = pathlib.Path().absolute()

        path_list = self.__splitall(current_path)

        path_list.pop()
        path_list.pop()

        path_list.append('assets')
        path_list.append('picturesForApproval')

        x = os.path.join(*path_list)

        # pathlib.Path(x).mkdir(exist_ok=True)

        # file.save(os.path.join(str(pathlib.Path().absolute()), x, nameOfFile))

        assets_dir = os.path.join('/var', 'www', 'noit_2021_2022', 'assets', 'picturesForApproval')

        os.makedirs(assets_dir, exist_ok=True)
        file.save(os.path.join(assets_dir, nameOfFile))


        try:
            hasPicForApproval = self.db_pictures.find_one({'userId': user_id})

            if hasPicForApproval is not None:
                self.db_pictures.delete_one({'userId': user_id})
                filePath = os.path.join(hasPicForApproval['path_Full'], hasPicForApproval['filename'])
                os.remove(filePath)

            self.db_pictures.insert_one({
                'userId': user_id,
                "path_Full": os.path.join(x, nameOfFile),
                "filename": nameOfFile,
                'time': str(time.time())
            })

            return {'status': 'OK', 'message': 'Successfully uploaded image.'}

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

    def approve_profile_picture(self, picture_id):
        try:
            queryPic = {'_id': ObjectId(picture_id)}
            picInfo = self.db_pictures.find_one(queryPic)

            queryUser = {'_id': ObjectId(picInfo['userId'])}

            user = self.db_users.find_one(queryUser)

            current_path = pathlib.Path().absolute()

            path_list = self.__splitall(current_path)

            path_list.pop()
            path_list.pop()

            path_list.append('assets')
            path_list.append('profilePictures')

            x = os.path.join(*path_list)

            # pathlib.Path(x).mkdir(exist_ok=True)
            
            assets_dir = os.path.join('/var', 'www', 'noit_2021_2022', 'assets')
            for_approval_dir = os.path.join(assets_dir, 'picturesForApproval')
            approved_dir = os.path.join(assets_dir, 'profilePictures')


            os.makedirs(approved_dir, exist_ok=True)
            
            oldPicPath = os.path.join(approved_dir, user['picture'].replace("assets/profilePictures/", ''))

            picPath = os.path.join('/var', 'www', 'noit_2021_2022', picInfo['path_Full'])

            profilePicPath = os.path.join("assets", "profilePictures", picInfo['filename'])
            # profilePicPath = "assets/profilePictures/" + picInfo['filename']

            if os.path.exists(picPath):

                shutil.move(picPath, os.path.join(approved_dir, picInfo['filename']))
                newValue = {"$set": {"picture": profilePicPath}}
                self.db_users.update_one(queryUser, newValue)
                if not user['picture'] == '':
                    os.remove(oldPicPath)
                self.db_pictures.delete_one(queryPic)
                return {'status': 'OK', 'message': 'Picture successfully deleted.'}
            else:
                self.db_pictures.delete_one(queryPic)
                return {'status': 'error_file_doesnt_exist', 'message': 'The file doesnt exist.'}

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}

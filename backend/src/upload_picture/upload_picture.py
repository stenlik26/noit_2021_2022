from bson.objectid import ObjectId
import json
from pymongo.errors import ConnectionFailure
import time
import pathlib
from datetime import datetime
import os


class PictureUpload:
    def __init__(self, mongo_connection):
        self.db = mongo_connection["Main"]['PictureForApproval']

    def upload_picture_for_approval(self, user_id, file):

        nameOfFile = user_id + "@" + str(datetime.now())[:-7]
        nameOfFile = nameOfFile.replace(' ', '_')
        nameOfFile = nameOfFile.replace(':', '-')
        nameOfFile = nameOfFile + '.png'

        x = os.path.join('..', '..', 'assets', 'picturesForApproval')

        pathlib.Path(x).mkdir(exist_ok=True)

        file.save(os.path.join(str(pathlib.Path().absolute()), x, nameOfFile))

        try:
            hasPicForApproval = self.db.find_one({'userId': user_id})

            if hasPicForApproval is not None:
                self.db.delete_one({'userId': user_id})
                filePath = os.path.join(hasPicForApproval['path_Full'], hasPicForApproval['filename'])
                os.remove(filePath)

            self.db.insert_one({
                'userId': user_id,
                "path_Full": os.path.join(str(pathlib.Path().absolute()), x),
                "filename": nameOfFile,
                'time': str(time.time())
            })

            return {'status': 'OK', 'message': 'Successfully uploaded image.'}

        except ConnectionFailure:
            return {'status': 'error', 'message': 'Cant connect to db.'}


import os
import random
import string

import boto3
from flask import current_app, jsonify, request

from api.config import Config
from api.utils import permission_required
from flask_jwt_extended import jwt_required
from api.models import ObjectStorage
from api import db
from apifairy import response
from api.schemas.objectstorage import ObjectStorageSchema


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

objectstorageschema=ObjectStorageSchema(many=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def create_s3_session():
    return boto3.session.Session().client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION
    )


@jwt_required()
@permission_required('admin.s3.read_all')
def get_all_items():
    s3 = create_s3_session()
    return jsonify(s3.list_objects(Bucket='vapehookahstatic')['Contents'])


@jwt_required()
@permission_required('admin.s3.read')
@response(objectstorageschema)
def get_db_items():
    items = db.session.scalars(ObjectStorage.select())
    return items


@jwt_required()
@permission_required('admin.s3.upload')
def upload():
    if 'image' not in request.files:
        return jsonify(code=400, error='File not found in payload'), 400

    file = request.files['image']
    if file and allowed_file(file.filename):
        file_extension = get_extension(file.filename)
        filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12)) + file_extension
        saved_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        file.save(saved_filename)

        s3 = create_s3_session()
        s3.upload_file(saved_filename, 'vapehookahstatic', filename)

        obj = ObjectStorage(link=filename)
        db.session.add(obj)
        db.session.commit()
        os.remove(saved_filename)
        return jsonify(code=200, id=obj.id)
    return jsonify(code=400, error='File extension is not allowed')


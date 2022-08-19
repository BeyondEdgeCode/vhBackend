import boto3
from flask import current_app, jsonify, request
from api.utils import permission_required
from flask_jwt_extended import jwt_required
from api.models import ObjectStorage
from api import db
import urllib


def create_s3_session():
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_REGION']
    )
    return s3


@jwt_required()
@permission_required('admin.s3.read')
def get_all_items():
    s3 = create_s3_session()
    return jsonify(s3.list_objects(Bucket='vapehookahstatic')['Contents'])


def get_file():
    key = request.json['key']

    # s3 = create_s3_session()

    # presigned_url = s3.generate_presigned_url(
    #     "get_object",
    #     Params={"Bucket": "vapehookahstatic", "Key": key},
    #     ExpiresIn=3600,
    # )
    file = db.session.scalar(ObjectStorage.select().where(ObjectStorage.id == key))
    url = 'https://storage.yandexcloud.net/vapehookahstatic/' + urllib.parse.quote(file.link)
    return jsonify(url=url)
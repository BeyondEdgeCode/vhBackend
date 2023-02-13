from flask import Blueprint
from .routes import get_all_items
# from .routes import get_file
from .routes import upload
from .routes import get_db_items

s3 = Blueprint('s3', __name__, url_prefix='/s3')

s3.add_url_rule('/get_all', 's3_get_all', get_all_items, methods=['GET'])
s3.add_url_rule('/upload', 's3_upload_file', upload, methods=['PUT'])
s3.add_url_rule('/get', 's3_get', get_db_items, methods=['GET'])
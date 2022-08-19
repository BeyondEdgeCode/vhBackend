from flask import Blueprint
from .routes import get_all_items
from .routes import get_file

s3 = Blueprint('s3', __name__)

s3.add_url_rule('/s3/get_all', 's3_get_all', get_all_items, methods=['GET'])
s3.add_url_rule('/s3/get', 's3_get_file', get_file, methods=['COPY'])
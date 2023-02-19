from flask import Blueprint
from .routes import get, create, delete


favourite = Blueprint('favourite', __name__, url_prefix='/product/favourite')

favourite.add_url_rule('', 'favourite_get', get, methods=['GET'])
favourite.add_url_rule('', 'favourite_post', create, methods=['POST'])
favourite.add_url_rule('', 'favourite_delete', delete, methods=['DELETE'])

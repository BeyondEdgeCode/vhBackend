from flask import Blueprint
from .routes import create, update, get_active, get_all

imagecarousel = Blueprint('imagecarousel', __name__, url_prefix='/ic')

imagecarousel.add_url_rule('/get_active', 'ic_get_active', get_active, methods=['GET'])
imagecarousel.add_url_rule('/create', 'ic_create', create, methods=['POST'])
imagecarousel.add_url_rule('/update', 'ic_update', update, methods=['PATCH'])
imagecarousel.add_url_rule('/all', 'all', get_all, methods=['GET'])

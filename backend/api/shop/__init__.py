from flask import Blueprint
from .routes import create, get_all

shop = Blueprint('shop', __name__, url_prefix='/shop')

shop.add_url_rule('/get', 'shop_get_all', get_all, methods=['GET'])
shop.add_url_rule('/create', 'shop_create', create, methods=['POST'])


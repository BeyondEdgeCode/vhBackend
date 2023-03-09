from flask import Blueprint
from .routes import add, get, decrement, increment, delete

basket = Blueprint('basket', __name__, url_prefix='/basket')

basket.add_url_rule('', 'add_item', add, methods=['POST'])
basket.add_url_rule('', 'get_items', get, methods=['GET'])
basket.add_url_rule('/inc', 'inc_items', increment, methods=['PATCH'])
basket.add_url_rule('/dec', 'dec_items', decrement, methods=['PATCH'])
basket.add_url_rule('/delete', 'delete_item', delete, methods=['DELETE'])
from flask import Blueprint
from .routes import create, get_by_user, cancel_by_user, cancel_by_admin, change_state, get_by_admin

order = Blueprint('order', __name__, url_prefix='/order')

order.add_url_rule('/create', 'create', create, methods=['POST'])
order.add_url_rule('/get', 'get_by_user', get_by_user, methods=['GET'])
order.add_url_rule('/aget', 'get_by_admin', get_by_admin, methods=['GET'])
order.add_url_rule('/cancel', 'cancel_by_user', cancel_by_user, methods=['DELETE'])
order.add_url_rule('/acancel', 'cancel_by_admin', cancel_by_admin, methods=['DELETE'])
order.add_url_rule('/state', 'change_state', change_state, methods=['PATCH'])

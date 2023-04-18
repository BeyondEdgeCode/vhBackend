from flask import Blueprint
from .routes import create

order = Blueprint('order', __name__, url_prefix='/order')

order.add_url_rule('/create', 'create', create, methods=['POST'])

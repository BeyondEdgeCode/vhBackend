from flask import Blueprint
from .routes import get

admin = Blueprint('admin', __name__, url_prefix='/admin')

admin.add_url_rule('/get', 'get', get, methods=['GET'])

from flask import Blueprint
from .routes import get_users, get_shops, version

testing = Blueprint('testing', __name__)

testing.add_url_rule('/testing/get_users', 'test_get_users', get_users, methods=['GET'])
testing.add_url_rule('/ver', 'version', version, methods=['GET'])

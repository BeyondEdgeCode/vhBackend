from flask import Blueprint
from .routes import get_users, get_shops, zerodivision_test

testing = Blueprint('testing', __name__)

testing.add_url_rule('/testing/get_users', 'test_get_users', get_users, methods=['GET'])
testing.add_url_rule('/testing/zerodivision', 'zerodivision_handler', zerodivision_test, methods=['GET'])

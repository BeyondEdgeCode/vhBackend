from flask import Blueprint
from .routes import add

permissions = Blueprint('permissions', __name__)

permissions.add_url_rule('/permissions/add', 'permissions_add', add, methods=['POST'])
from flask import Blueprint
from .routes import add
from .cli import cli_assign, cli_create_permission, cli_ls

permissions = Blueprint('permissions', __name__)

permissions.add_url_rule('/permissions/add', 'permissions_add', add, methods=['POST'])
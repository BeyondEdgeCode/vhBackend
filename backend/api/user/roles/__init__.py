from flask import Blueprint
from .routes import add, assign, get_all, add_permission, delete_permission
from .cli import cli_create_role, cli_ls

roles = Blueprint('roles', __name__, url_prefix='/roles')

roles.add_url_rule('/add', 'roles_add', add, methods=['POST'])
roles.add_url_rule('/assign', 'roles_assign', assign, methods=['PATCH'])
roles.add_url_rule('/all', 'roles_get_all', get_all, methods=['GET'])
roles.add_url_rule('/add_permission', 'roles_add_permission', add_permission, methods=['POST'])
roles.add_url_rule('/delete_permission', 'roles_delete_permission', delete_permission, methods=['DELETE'])

from flask import Blueprint
from .routes import add, assign, get_all, add_permission, delete_permission
from .cli import cli_create_role

roles = Blueprint('roles', __name__)

roles.add_url_rule('/roles/add', 'roles_add', add, methods=['POST'])
roles.add_url_rule('/roles/assign', 'roles_assign', assign, methods=['PATCH'])
roles.add_url_rule('/roles/all', 'roles_get_all', get_all, methods=['GET'])
roles.add_url_rule('/roles/add_permission', 'roles_add_permission', add_permission, methods=['POST'])
roles.add_url_rule('/roles/delete_permission', 'roles_delete_permission', delete_permission, methods=['DELETE'])

roles.cli.add_command(cli_create_role, 'create')
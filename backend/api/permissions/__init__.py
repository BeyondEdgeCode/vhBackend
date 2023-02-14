from flask import Blueprint
from .routes import add
from .cli import cli_assign, cli_create_permission

permissions = Blueprint('permissions', __name__)

permissions.add_url_rule('/permissions/add', 'permissions_add', add, methods=['POST'])

permissions.cli.add_command(cli_assign, 'assign')
permissions.cli.add_command(cli_create_permission, 'create_permission')
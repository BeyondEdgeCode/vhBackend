from typing import List

import click
from flask.cli import with_appcontext
from ..models import UserRole
from api.app import db


@click.group()
def roles():
    """Manage roles"""
    pass


@roles.command('create')
@click.argument('rolename', required=True)
@click.argument("description", required=True)
@click.argument('isdefault', required=True)
@with_appcontext
def cli_create_role(rolename: str, description: str, isdefault: bool):
    """Create new UserRole"""
    user_role = UserRole(roleName=rolename, roleDescription=description, is_default=bool(isdefault))
    db.session.add(user_role)
    db.session.commit()
    print(f'New UserRole [id] {user_role.id}, [roleName] {rolename}, [roleDescription] {description}, [is_default] {isdefault}')


@roles.command('ls')
@with_appcontext
def cli_ls():
    """List all UserRole's"""
    user_roles: List[UserRole] = db.session.scalars(UserRole.select())
    from prettytable import PrettyTable
    table = PrettyTable(['id', 'roleName', 'roleDescription', 'is_default'])
    for role in user_roles:
        table.add_row([role.id, role.roleName, role.roleDescription, role.is_default])
    print(table)

import click
from flask.cli import with_appcontext
from ..models import UserRole, Permission, UserRolePermission
from api.app import db


@click.command('create')
@click.argument('key', required=True)
@click.argument("description", default='Без описания')
@with_appcontext
def cli_create_permission(key: str, description: str):
    permission = Permission(key=key, description=description)
    db.session.add(permission)
    db.session.commit()
    print(f'New Permission created with [id] {permission.id} [key] {permission.key}, [description] {permission.description}')


@click.command('assign')
@click.argument('key', required=True)
@click.argument("userrole", required=True)
@with_appcontext
def cli_assign(key: str, userrole: int):
    permission = db.session.scalar(Permission.select().where(Permission.key == key))
    user_role = db.session.scalar(UserRole.select().where(UserRole.id == userrole))
    user_role_permission = UserRolePermission(role_fk=user_role.id, permission_fk=permission.id)

    db.session.add(user_role_permission)
    db.session.commit()
    print(f'New UserRolePermission created with [id] {user_role_permission.id} [UserRole] {user_role_permission.role.id}'
          f', [Permission] {user_role_permission.permission.id}')


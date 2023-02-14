import click
from flask.cli import with_appcontext
from ..models import UserRole
from api.app import db


@click.command('create')
@click.argument('rolename', required=True)
@click.argument("description", required=True)
@click.argument('isdefault', required=True)
@with_appcontext
def cli_create_role(rolename: str, description: str, isdefault: bool):
    user_role = UserRole(roleName=rolename, roleDescription=description, is_default=bool(isdefault))
    db.session.add(user_role)
    db.session.commit()
    print(f'New UserRole [id] {user_role.id}, [roleName] {rolename}, [roleDescription] {description}, [is_default] {isdefault}')

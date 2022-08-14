from sqlalchemy.exc import IntegrityError
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from api import db
from api.models import User, UserRole, UserRolePermission, Permission
from api.utils import get_first, catch_exception, permission_required
from api.schemas.roles import UserRoleSchema
from api.schemas.users import UserSchema
from apifairy import response
from sqlalchemy import and_

roles_schema = UserRoleSchema(many=True)
user_schema = UserSchema()


@jwt_required()
@permission_required('admin.roles.read')
@response(roles_schema)
def get_all():
    users = db.session.scalars(UserRole.select())
    return users


@jwt_required()
@permission_required('admin.roles.add')
def add():
    try:
        roleName = request.json['roleName']
        roleDescription = request.json['roleDesc']
        is_default = request.json['is_default']
    except KeyError as e:
        return catch_exception(e, 'Значение поля некорректно.')

    userRole = UserRole(roleName=roleName, roleDescription=roleDescription, is_default=is_default)
    try:
        db.session.add(userRole)
        db.session.commit()
    except IntegrityError as e:
        return catch_exception(e, 'Введено не уникальное значение')

    return jsonify(code=200, id=userRole.id)


@jwt_required()
def delete():
    try:
        roleId = request.json['roleId']
    except KeyError as e:
        catch_exception(e, 'Значение поля некорректно')


@jwt_required()
@permission_required('admin.roles.assign')
def assign():
    try:
        userId = int(request.json['userId'])
        roleId = int(request.json['roleId'])
    except:
        return catch_exception(e, 'Значение поля некорректно')

    user = get_first(User.select().where(User.id == userId))
    role = get_first(UserRole.select().where(UserRole.id == roleId))

    user.role = role

    db.session.add(user)
    db.session.commit()
    return jsonify(code=200)


@jwt_required()
def add_permission():
    try:
        roleId = int(request.json['roleId'])
        permissionId = int(request.json['permissionId'])
    except KeyError as e:
        return catch_exception(e, 'Значение поля некорректно')

    if not (permission:= db.session.get(Permission, permissionId)):
        return jsonify(code=400, error='Permission not found in database')

    if get_first(UserRolePermission.select().where(and_(UserRolePermission.permission == permission,
                                                        UserRolePermission.role_fk == roleId))):
        return jsonify(code=400, error='Permission already assigned to role')

    role_permission = UserRolePermission(role_fk=roleId, permission=permission)

    db.session.add(role_permission)
    db.session.commit()

    return jsonify(id=role_permission.id)

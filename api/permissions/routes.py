from sqlalchemy.exc import IntegrityError
from flask import request, jsonify
from api.utils import catch_exception, permission_required
from api.models import UserRole, UserRolePermission, Permission
from flask_jwt_extended import jwt_required
from api import db


@jwt_required()
@permission_required('admin.permissions.create')
def add():
    try:
        # roleId = int(request.json['roleId'])
        permission = request.json['permission']
        description = request.json.get('desc', None)
    except KeyError as e:
        return catch_exception(e, 'Значение поля некорректно.')

    permission = Permission(key=permission, description=description)
    try:
        db.session.add(permission)
        db.session.commit()
    except IntegrityError as e:
        return catch_exception(e, 'Введено не уникальное значение')

    return jsonify(code=200, id=permission.id)


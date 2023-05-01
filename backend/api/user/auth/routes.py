from werkzeug.exceptions import BadRequest
from flask import jsonify, request
from werkzeug.exceptions import Unauthorized
from sqlalchemy.sql.expression import and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, current_user, set_access_cookies
from api.utils import get_first_or_false, get_first
from api.models import User, RevokedTokens, UserRole
from api.app import db
from datetime import datetime, timezone
from api.app import jwt
from apifairy import body, response, other_responses, authenticate
from api.schemas.auth import LoginSchema, LoginResponseSchema, RegisterSchema, UserInfoSchema, UserSchema
from flask_cors import cross_origin


jwt.unauthorized_loader(lambda auth: (jsonify({'error': 'Not authorized'}), 401))
jwt.revoked_token_loader(lambda auth: (jsonify({'error': 'Token has been revoked'}), 403))
jwt.invalid_token_loader(lambda auth: (jsonify({'error': 'Invalid token'}), 403))


@jwt.user_identity_loader
def user_identitty_loader(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_loader(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return db.session.scalar(User.select().where(User.id == identity))


# @response(LoginResponseSchema)
@cross_origin()
@body(LoginSchema)
def login(cred):
    user: User = get_first_or_false(User.select().where(User.email == cred['email']))
    if not user:
        return jsonify(status=401, error='Wrong login or password')
    if not user.check_password(cred['password']):
        return jsonify(status=401, error='Wrong login or password')

    if not user.email_confirmed:
        return jsonify(status=403, error='Email is not confirmed')

    return {'access_token': create_access_token(identity=user), 'refresh_token': create_refresh_token(identity=user)}


@jwt_required()
def logout():
    token = get_jwt()
    jti = token['jti']
    ttype = token['type']
    now = datetime.now(timezone.utc)
    revoked_token = RevokedTokens(jti=jti, type=ttype, created_at=now)
    db.session.add(revoked_token)
    db.session.commit()
    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


@cross_origin()
@body(RegisterSchema)
def register(user_info):
    # TODO: Add birthday check
    if get_first_or_false(User.select().where(User.email == user_info['email'])):
        return jsonify(internal_code=1003, error='Email is used'), 400

    default_role = get_first(UserRole.select().where(UserRole.is_default == True))
    user = User(email=user_info['email'], password=generate_password_hash(user_info['password']),
                birthday=user_info['birthday'], role=default_role)
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return jsonify(user_id=user.id), 200


@jwt_required()
@response(UserInfoSchema)
def me():
    return {'id': current_user.id,
            'role': current_user.role.roleName,
            'permissions': current_user.role.get_rights(),
            'user': current_user
            }


@jwt_required()
@body(UserSchema(exclude=['id', 'registrationDate', 'email_confirmed']))
def me_update(args: dict):
    user = db.session.get(User, current_user.id)
    for k, v in args.items():
        setattr(user, k, v)
    db.session.add(user)
    db.session.commit()
    return jsonify(status=200, msg='Данные обновлены')
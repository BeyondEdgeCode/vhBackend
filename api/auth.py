from werkzeug.exceptions import BadRequest
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import Unauthorized
from sqlalchemy.sql.expression import and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from .utils import get_first_or_false
from .models import User
from .app import db

auth = Blueprint('auth', __name__)


@auth.route('/auth/login', methods=['POST'])
def login():
    try:
        email = request.json['email']
        password = request.json['password']
        remember_me = request.json['remember']
    except KeyError:
        return BadRequest()

    user: User = get_first_or_false(User.select().where(User.email == email))
    if user:
        if user.check_password(password):
            if not user.email_confirmed: return jsonify(internal_code=1002, error='Email is not confirmed')
            token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify(token=token, refresh_token=refresh_token)
        else:
            return jsonify(internal_code=1001, error='Bad login or password'), 401
    else:
        return jsonify(internal_code=1001, error='Bad login or password'), 401

@auth.route('/auth/reg', methods=['POST'])
def register():
    try:
        email = request.json['email']
        password = request.json['password']
        birthday = request.json['birthday']
    except KeyError:
        return BadRequest()

    # Check email unique constraint
    if get_first_or_false(User.select().where(User.email == email)):
        return jsonify(internal_code=1003, error='Email is used'), 400

    user = User(email=email, password=generate_password_hash(password), birthday=birthday)
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return jsonify(user_id=user.id), 200






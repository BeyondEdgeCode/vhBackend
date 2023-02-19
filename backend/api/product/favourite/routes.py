from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from api.utils import permission_required
from apifairy import body, response, arguments
from .schema import GetSchema, PostSchema, DeleteSchema
from api.app import db
from api.models import Favourite
from sqlalchemy import and_


@jwt_required()
@permission_required('user.product.favourite.add')
@body(PostSchema)
def create(data: PostSchema):
    if db.session.scalar(Favourite.select().where(
        and_(
            Favourite.user_fk == current_user.id,
            Favourite.product_fk == data['product_fk']
        )
    )):
        return jsonify(status=400, msg='Already exist'), 400

    new_favourite = Favourite(user_fk=current_user.id, product_fk=data['product_fk'])
    db.session.add(new_favourite)
    db.session.commit()

    return jsonify(status=200, msg='Added')


@jwt_required()
@permission_required('user.product.favourite.read')
@response(GetSchema(many=True))
def get():
    return db.session.scalars(Favourite.select().where(
        Favourite.user_fk == current_user.id
    ))


@jwt_required()
@permission_required('user.product.favourite.delete')
@arguments(DeleteSchema)
def delete(data: DeleteSchema):
    record: Favourite = db.session.get(Favourite, data['id'])
    if not record:
        return jsonify(status=404, msg='Not found'), 404
    if record.user_fk != current_user.id:
        return jsonify(status=403, msg='Access denied'), 403

    db.session.delete(record)
    db.session.commit()

    return jsonify(status=200, msg='Deleted')

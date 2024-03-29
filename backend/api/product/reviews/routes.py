from flask import jsonify
from sqlalchemy import and_
from api.models import Reviews, Product, User
from api import db
from apifairy import response, body
from api.utils import permission_required
from flask_jwt_extended import jwt_required, current_user
from api.schemas.reviews import ReviewsSchema
from api.app import cache

reviewschema = ReviewsSchema()
reviewschemamany = ReviewsSchema(many=True)


@jwt_required()
@permission_required('user.review.create')
@body(reviewschema)
def create(args):
    if db.session.scalar(
            Reviews.select()
                    .where(
                        and_(
                            Reviews.product_id == args['product_id'],
                            Reviews.user_id == current_user.id
                        )
            )
    ):
        return jsonify(status=409, error='Already exits'), 409

    review = Reviews(**args, user_id=current_user.id)
    db.session.add(review)
    db.session.commit()
    return jsonify(status=200, error='Created'), 200


@cache.cached(600)
@response(reviewschemamany)
def get(product_id):
    reviews = db.session.scalars(Reviews.select().where(Reviews.product_id == product_id))
    return reviews

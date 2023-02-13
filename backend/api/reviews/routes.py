from api.models import Reviews, Product, User
from api import db
from apifairy import response, body
from api.utils import permission_required
from flask_jwt_extended import jwt_required, current_user
from api.schemas.reviews import ReviewsSchema

reviewschema = ReviewsSchema()
reviewschemamany = ReviewsSchema(many=True)


@jwt_required()
@permission_required('user.review.create')
@body(reviewschema)
@response(reviewschema)
def create(args):
    review = Reviews(**args, user_id=current_user.id)
    db.session.add(review)
    db.session.commit()
    return review


@response(reviewschemamany)
def get(product_id):
    reviews = db.session.scalars(Reviews.select().where(Reviews.product_id == product_id))
    return reviews
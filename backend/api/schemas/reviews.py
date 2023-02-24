from api.app import ma
from api.models import Reviews
from api.product.schema import ProductFKSchema
from marshmallow import validate
from api.schemas.users import UserReviewSchema


class ReviewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reviews

    id = ma.auto_field(dump_only=True)
    product_id = ma.auto_field()
    user = ma.Nested(UserReviewSchema, dump_only=True)
    stars = ma.auto_field(validate=validate.Range(min=0, max=5))
    text = ma.auto_field(validate=validate.Length(min=0, max=1024))

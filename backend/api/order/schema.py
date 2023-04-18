from api.app import ma
from marshmallow.fields import String
from marshmallow.fields import Integer


class CreateOrderSchema(ma.SQLAlchemySchema):
    promocode = String(load_default=None)
    shop_id = Integer(required=True)

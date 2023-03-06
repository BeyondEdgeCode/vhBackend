from api.app import ma
from marshmallow.fields import String, Integer
from api.models import Basket


class BasketIdSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Basket

    id = ma.auto_field()


class AddToBasketSchema(ma.SQLAlchemySchema):

    shop_id = Integer(required=True)
    product_id = Integer(required=True)


class BasketSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Basket

    id = ma.auto_field()
    amount = ma.auto_field()
    product = ma.Nested('ProductShortSchema')

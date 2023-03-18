from api.app import ma
from marshmallow.fields import String, Integer, List, Float
from api.models import Product, Basket


class BasketIdSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product

    id = ma.Integer(required=True)


class AddToBasketSchema(ma.SQLAlchemySchema):

    product_id = Integer(required=True)


class BasketSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Basket

    id = ma.auto_field()
    amount = ma.auto_field()
    product = ma.Nested('ProductShortSchema')


class BasketAvailabilitySchema(ma.SQLAlchemySchema):
    shop_id = Integer()
    not_available = List(Integer)


class BasketWrapperSchema(ma.SQLAlchemySchema):
    products = ma.Nested(BasketSchema(many=True))
    availability = List(ma.Nested(BasketAvailabilitySchema))
    total = Float()

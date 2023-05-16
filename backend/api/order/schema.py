from api.app import ma
from marshmallow.fields import String
from marshmallow.fields import Integer, Nested, Boolean
from api.models import Order, PaymentType, DeliveryType, OrderStatus, OrderItem
from api.promocode.schema import PromocodeSchema
from api.schemas.shop import ShopSchema
from marshmallow_enum import EnumField
from api.product.schema import ProductShortSchema
from api.schemas.users import UserSchema


class OrderLifecycleSchema(ma.SQLAlchemySchema):
    id = Integer(required=True)
    next_state = EnumField(OrderStatus, required=True)


class CreateOrderSchema(ma.SQLAlchemySchema):
    promocode = String(load_default=None)
    shop_id = Integer(required=True)


class OrderItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OrderItem

    product = Nested(ProductShortSchema())
    price = ma.auto_field()
    amount = ma.auto_field()
    item_sum = ma.auto_field()


class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order
        ordered = True

    id = ma.auto_field()
    user = ma.Nested(UserSchema)
    status = EnumField(OrderStatus)
    delivery_type = EnumField(DeliveryType)
    payment_type = EnumField(PaymentType)
    sum = ma.auto_field()
    promocode_ref = ma.Nested(PromocodeSchema(only=['key', 'value', 'promotype']))
    shop = ma.Nested(ShopSchema)
    items = Nested(OrderItemSchema(many=True))
    created_at = ma.auto_field()


class ShortOrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order
        ordered = True

    id = ma.auto_field()
    status = EnumField(OrderStatus)
    sum = ma.auto_field()
    shop = ma.Nested(ShopSchema)
    created_at = ma.auto_field()


class OrderIdSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order

    id = ma.auto_field(load_only=True)


class GetByAdminSchema(ma.SQLAlchemySchema):
    class Meta:
        ordered = True

    active_only = Boolean(load_default=False)
    current_shop_only = Boolean(load_default=True)
    shop_id = Integer(allow_none=True)

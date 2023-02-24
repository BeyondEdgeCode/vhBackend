from api import ma
from marshmallow import validate
from api.models import ProductAvailability
from api.product.schema import ProductSchema
from api.schemas.shop import ShortShopSchema


class ProductAvailabilitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductAvailability

    product_id = ma.auto_field()
    shop_id = ma.auto_field()
    amount = ma.auto_field(validate=validate.Range(min=0))


class ProductAvailabilityGetSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductAvailability

    product_id = ma.auto_field()


class ProductAvailabilityResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductAvailability
        include_fk = True

    id = ma.auto_field()
    product = ma.Nested(ProductSchema)
    shop = ma.Nested(ShortShopSchema)
    amount = ma.auto_field()


class ShopIdSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductAvailability

    id = ma.auto_field(missing=1)
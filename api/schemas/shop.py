from api.app import ma
from api.models import Shop
from marshmallow import validate


class ShopSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Shop
        include_fk = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True, validate=validate.Length(min=1, max=64))
    city = ma.auto_field(required=True, validate=validate.Length(min=1, max=128))
    street = ma.auto_field(required=True, validate=validate.Length(min=1, max=128))
    building = ma.auto_field(required=True, validate=validate.Length(min=1, max=128))
    description = ma.auto_field(required=True, validate=validate.Length(min=1, max=128))
    preview = ma.auto_field(validate=validate.Length(min=1, max=1024))


class ShortShopSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Shop
        include_fk = True

    id = ma.auto_field()
    title = ma.auto_field()

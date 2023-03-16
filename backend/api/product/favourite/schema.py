from api import ma
from api.models import Favourite
from api.product.schema import ProductSchema


class GetSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Favourite
        include_fk = True

    product = ma.Nested(ProductSchema)


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Favourite

    product_fk = ma.auto_field()


class DeleteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Favourite

    id = ma.auto_field()
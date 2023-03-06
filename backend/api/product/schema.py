from api.app import ma
from api.models import Product, ProductAvailability
from api.schemas.category import CategoryInfoSchema
from api.schemas.shop import ShortShopSchema
from marshmallow import validate


class ProductAvailabilityNestedSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductAvailability
        include_fk = True
        ordered = True

    shop = ma.Nested(ShortShopSchema)
    amount = ma.auto_field()


class ProductFKSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        include_fk = True

    id = ma.auto_field()


class ReferencedProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        include_fk = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(dump_only=True)
    specifications = ma.Nested('SpecificationSchema')
    image_link = ma.String(dump_only=True)


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        include_fk = True

    id = ma.auto_field(dump_only=True)
    category = ma.Nested(CategoryInfoSchema, dump_only=True)
    title = ma.auto_field(dump_only=True)
    description = ma.auto_field(dump_only=True)
    price = ma.auto_field(dump_only=True)
    specifications = ma.Method('get_specifications', dump_only=True)
    image_link = ma.String(dump_only=True)
    avg_stars = ma.Integer(dump_only=True)
    available = ma.Nested(ProductAvailabilityNestedSchema, dump_only=True, many=True)

    def get_specifications(self, data: Product):
        return [spec.get_specification() for spec in data.specifications]


class ProductShortSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        include_fk = True

    id = ma.auto_field(dump_only=True)
    category = ma.Nested(CategoryInfoSchema, dump_only=True)
    title = ma.auto_field(dump_only=True)
    price = ma.auto_field(dump_only=True)
    image_link = ma.String(dump_only=True)
    avg_stars = ma.Integer(dump_only=True)


class ProductCreateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product

    title = ma.auto_field(required=True, validate=validate.Length(
        min=1, max=64
    ))
    description = ma.String()
    price = ma.auto_field(required=True)
    parent_fk = ma.auto_field()
    category_fk = ma.auto_field(required=True)
    subcategory_fk = ma.auto_field()
    image_fk = ma.auto_field(required=True)
    specifications = ma.auto_field()
    is_child = ma.auto_field(required=True)

from api.app import ma
from api.models import Product
from .category import CategoryInfoSchema
from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump

class ReferencedProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        include_fk = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(dump_only=True)
    specifications = ma.auto_field(dump_only=True)


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        include_fk = True

    id = ma.auto_field(dump_only=True)
    category = ma.Nested(CategoryInfoSchema, dump_only=True)
    title = ma.auto_field(dump_only=True)
    description = ma.auto_field(dump_only=True)
    price = ma.auto_field(dump_only=True)
    referenced_product = ma.Nested(ReferencedProductSchema, dump_only=True, many=True)
    specifications = ma.auto_field(dump_only=True)


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
    specifications = ma.auto_field()
    is_child = ma.auto_field(required=True)


from api.app import ma
from api.models import Product, ProductAvailability, ProductSpecification, SpecificationToProduct
from .category import CategoryInfoSchema
from .shop import ShortShopSchema
from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump


class ProductAvailabilitySchema(ma.SQLAlchemySchema):
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
    specifications = ma.auto_field(dump_only=True)
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
    referenced_product = ma.Nested(ReferencedProductSchema, dump_only=True, many=True)
    specifications = ma.auto_field(dump_only=True)
    image_link = ma.String(dump_only=True)
    avg_stars = ma.Integer(dump_only=True)

    available = ma.Nested(ProductAvailabilitySchema, dump_only=True, many=True)


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


class SpecificationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductSpecification

    id = ma.auto_field(dump_only=True)
    key = ma.auto_field(required=True)
    value = ma.auto_field(required=True)
    type = ma.auto_field(required=True)


class AssignSpecificationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SpecificationToProduct

    product_id = ma.auto_field(required=True)
    specification_id = ma.auto_field(required=True)


class GetSpecificationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SpecificationToProduct

    product_id = ma.auto_field(required=True)


class ModSpecificationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProductSpecification

    id = ma.auto_field(required=True)
    key = ma.auto_field(required=True)
    value = ma.auto_field(required=True)
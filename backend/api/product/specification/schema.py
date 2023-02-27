import marshmallow.fields

from api.app import ma
from api.models import Specification, SpecificationValue, SpecificationToProduct
from api.product.schema import ProductSchema
from marshmallow.fields import Method, List, Dict


class SpecificationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Specification
        ordered = True

    id = ma.auto_field(dump_only=True)
    key = ma.auto_field()
    type = ma.auto_field()
    is_filter = ma.auto_field()
    values = Method('get_values', dump_only=True)

    def get_values(self, data: Specification):
        if type(data) is dict:
            return {
                'max': data['values']['max'],
                'min': data['values']['min'],
            }
        return data.get_values()


class SpecificationValuesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SpecificationValue

    id = ma.auto_field(dump_only=True)
    specification_id = ma.auto_field(load_only=True)
    specification = ma.Nested(SpecificationSchema, many=True, dump_only=True, )
    value = ma.auto_field()


class ValuesOnlySchema(ma.SQLAlchemySchema):
    class Meta:
        model = SpecificationValue

    id = ma.auto_field()
    value = ma.auto_field()


class SpecificationToProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SpecificationToProduct
        many = True

    id = ma.auto_field(dump_only=True)
    product_id = ma.auto_field(load_only=True)
    product = ma.Nested(ProductSchema, dump_only=True)
    specification_id = ma.auto_field(load_only=True)
    specification = ma.Method('get_specification', dump_only=True)

    def get_specification(self, data: SpecificationToProduct):
        return data.get_specification()


class SpecificationFullSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Specification
        ordered = True

    id = ma.auto_field()
    key = ma.auto_field()
    type = ma.auto_field()
    is_filter = ma.auto_field()
    values = ma.Nested(SpecificationValuesSchema, many=True, only=('id', 'value'))


class SpecificationWithCustom(ma.SQLAlchemySchema):
    filters = ma.Nested(SpecificationSchema, many=True)
    custom = Dict(marshmallow.fields.Raw())

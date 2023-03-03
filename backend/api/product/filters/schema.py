from api.app import ma
from marshmallow import Schema, fields
from typing import Union


class FiltersSchema(ma.SQLAlchemySchema):
    f = fields.List(fields.Integer())


class FiltersElementSchema(ma.SQLAlchemySchema):
    specs = fields.List(fields.Integer)
    id = fields.Integer()


class FiltersNewSchema(ma.SQLAlchemySchema):
    filters = fields.List(
        fields.Dict(
            keys=fields.String,
            values=fields.Raw
        )
    )
    max = fields.Float(load_default=100000.00)
    min = fields.Float(load_default=0.00)
    category_id = fields.Int(required=True)
    available = fields.Bool(load_default=0)


class FiltersSubcategorySchema(ma.SQLAlchemySchema):
    filters = fields.List(
        fields.Dict(
            keys=fields.String,
            values=fields.Raw
        )
    )
    max = fields.Float(load_default=100000.00)
    min = fields.Float(load_default=0.00)
    subcategory_id = fields.Int(required=True)
    available = fields.Bool(load_default=0)




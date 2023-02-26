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



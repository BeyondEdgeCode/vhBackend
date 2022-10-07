from api.app import ma

from marshmallow.base import FieldABC


class FilterValueSchema(ma.Schema):
    value = ma.String()


class FiltersSchema(ma.Schema):
    key = ma.String()
    type = ma.String()
    value = ma.List(ma.Nested(FilterValueSchema))

from marshmallow.base import SchemaABC

from api.app import ma
from marshmallow.fields import Integer, String, List, DateTime
from marshmallow.fields import Nested
from api.models import PromoType
from api.models import Promocode

class PromoTypeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PromoType

    id = ma.auto_field(dump_only=True)
    type = ma.auto_field(required=True)


class PromocodeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Promocode

    id = ma.auto_field(dump_only=True)
    promotype_fk = ma.auto_field(load_only=True)
    key = ma.auto_field()
    value = ma.auto_field()
    is_enabled = ma.auto_field()
    available_until = ma.auto_field()
    promotype = ma.Nested(PromoTypeSchema(only=["type"]), dump_only=True, )


class PromocodeAssignSchema(ma.SQLAlchemySchema):
    promocode_id = Integer()
    products = List(Integer, load_default=[])
    categories = List(Integer, load_default=[])
    subcategories = List(Integer, load_default=[])

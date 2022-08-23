from api.app import ma
from api.models import ObjectStorage


class ObjectStorageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ObjectStorage

    id = ma.auto_field(dump_only=True)
    link = ma.auto_field()
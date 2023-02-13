from api.app import ma
from api.models import ImageCarousel


class ImageCarouselSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ImageCarousel
        include_fk = True

    id = ma.auto_field(dump_only=True)
    image_id = ma.auto_field(required=True)
    active = ma.auto_field(required=True)
    image_link = ma.String(dump_only=True)


class ImageCarouseUpdateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ImageCarousel
        include_fk = True

    id = ma.auto_field(required=True)
    image_id = ma.auto_field(required=True)
    active = ma.auto_field(required=True)
from api.schemas.imagecarousel import ImageCarouselSchema, ImageCarouseUpdateSchema
from apifairy import body, response
from api.utils import permission_required
from flask_jwt_extended import jwt_required
from api.models import ImageCarousel
from api.app import db, cache

icmany = ImageCarouselSchema(many=True)


@jwt_required()
@permission_required('admin.imagecarousel.create')
@body(ImageCarouselSchema)
@response(ImageCarouselSchema)
def create(args):
    image = ImageCarousel(**args)
    db.session.add(image)
    db.session.commit()
    return image


@jwt_required()
@permission_required('admin.imagecarousel.update')
@body(ImageCarouseUpdateSchema)
@response(ImageCarouselSchema)
def update(args):
    image = db.session.scalar(
        ImageCarousel.select().where(ImageCarousel.id == args['id'])
    )
    image.active = args['active']
    image.image_id = args['image_id']
    db.session.add(image)
    db.session.commit()
    return image


@cache.cached(600)
@response(icmany)
def get_active():
    images = db.session.scalars(
        ImageCarousel.select().where(ImageCarousel.active == True)
    )
    return images

from flask import jsonify
from api.app import db
from api.models import ProductAvailability
from .schema import ProductAvailabilitySchema, ShopIdSchema
from .schema import ProductAvailabilityResponseSchema
from apifairy import body, response, arguments
from sqlalchemy import and_
from ...utils import permission_required
from ...utils import responses


@permission_required('admin.product.availability.edit')
@body(ProductAvailabilitySchema)
def edit(data):
    product_availability: ProductAvailability = db.session.scalar(ProductAvailability.select().where(
        and_(
            ProductAvailability.product_id == data['product_id'],
            ProductAvailability.shop_id == data['shop_id']
        )
    ))
    product_availability.amount=data['amount']

    db.session.add(product_availability)
    db.session.commit()

    return responses.throw_200(msg='Ok')


@permission_required('admin.product.availability.get')
@response(ProductAvailabilityResponseSchema(many=True))
def get_all():
    availability = db.session.scalars(
        ProductAvailability.select().order_by(ProductAvailability.id.asc()
    ))

    return availability


@permission_required('admin.product.availability.get')
@response(ProductAvailabilityResponseSchema(many=True))
@arguments(ShopIdSchema)
def get_by_shop(data):
    availability = db.session.scalars(ProductAvailability.select().where(
        ProductAvailability.shop_id == data['id']
    ))
    return availability

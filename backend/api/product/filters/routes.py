from flask import jsonify, current_app
from api import db
from flask_jwt_extended import jwt_required
from api.utils import permission_required
from apifairy import response, body, arguments
from api.models import Product, Category, SpecificationToProduct, SpecificationValue, Specification
from api.models import Specification, SpecificationValue, SpecificationToProduct, Product
from api.schemas.category import SearchByCategorySchema
from api.product.specification.schema import SpecificationSchema, SpecificationToProductSchema, \
    SpecificationValuesSchema
from sqlalchemy import and_
from api.product.schema import ProductSchema


@arguments(SearchByCategorySchema)
@response(SpecificationSchema(many=True))
def get_filters_by_category(args):
    return db.session.scalars(
        Specification.select()
        .join(SpecificationValue)
        .join(SpecificationToProduct)
        .join(Product)
        .distinct(Specification.id)
        .where(
            and_(
                Product.category_fk == args['id'],
                Specification.is_filter == True
            )
        )
    )
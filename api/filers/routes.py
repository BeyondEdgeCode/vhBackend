from flask import jsonify, current_app

from api import db
from flask_jwt_extended import jwt_required
from api.utils import permission_required
from apifairy import response, body, arguments
from api.models import Product, ProductSpecification, Category
from api.schemas.product import SpecificationSchema
from api.schemas.category import SearchByCategorySchema
from api.schemas.filters import FiltersSchema
from sqlalchemy import and_

filters_schema = FiltersSchema(many=True)
get_by_category_schema = SearchByCategorySchema()


@arguments(get_by_category_schema)
@response(filters_schema)
def get_filters(args):
    unique_keys = db.session.scalars(
        ProductSpecification.select()
        .join(Product)
        .join(Category)
        .distinct(ProductSpecification.key)
        .where(Product.category_fk == args['id'])
    )

    filters_list = []

    for unique_key in unique_keys:
        unique_values = db.session.scalars(
            ProductSpecification.select()
            .join(Product)
            .join(Category)
            .distinct(ProductSpecification.value)
            .where(
                and_(
                    Product.category_fk == args['id'],
                    ProductSpecification.key == unique_key.key)
            )
        )
        filters_list.append(
            {
                'key': unique_key.key,
                'type': unique_key.type,
                'value': [{'value': result.value} for result in unique_values]
            }
        )

    return filters_list

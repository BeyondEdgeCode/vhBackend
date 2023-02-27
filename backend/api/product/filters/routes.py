from typing import List

from api import db
from apifairy import response, body, arguments
from api.models import Specification, SpecificationValue, SpecificationToProduct, Product
from api.schemas.category import SearchByCategorySchema
from api.product.schema import ProductSchema
from api.product.specification.schema import SpecificationSchema
from sqlalchemy import and_
from .schema import FiltersNewSchema, FiltersSchema
from flask_cors import cross_origin


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


@cross_origin()
@body(FiltersNewSchema)
@response(ProductSchema(many=True))
def get_by_filters(data):
    candidates = []
    for f in data['filters']:
        query = db.session.scalars(
            Product.select()
            .join(SpecificationToProduct)
            .where(
                SpecificationToProduct.specification_id.in_(
                    f['specs']
                )
            )
        )
        candidates.append(query)

    ids = []
    for candidate in candidates:
        for product in candidate:
            ids.append(product.id)
# https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
    resp = list(set([x for x in ids if ids.count(x) == len(data['filters'])]))
    print(ids)
    return db.session.scalars(
        Product.select().where(
            Product.id.in_(resp)
        )
    )










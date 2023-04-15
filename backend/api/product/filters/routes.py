from flask import current_app

from api import db
from apifairy import response, body, arguments
from api.models import Specification, SpecificationValue, SpecificationToProduct, Product, ProductAvailability
from api.schemas.category import SearchByCategorySchema, SearchBySubCategorySchema
from api.product.schema import ProductSchema
from api.product.specification.schema import SpecificationSchema, SpecificationWithCustom
from sqlalchemy import and_
from .schema import FiltersNewSchema, FiltersSubcategorySchema
from flask_cors import cross_origin
from api.app import cache


@cache.cached(300)
@arguments(SearchByCategorySchema)
@response(SpecificationSchema(many=True))
def get_filters_by_category(args):
    filters = db.session.scalars(
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
    products = [*db.session.scalars(
        Product.select()
        .where(
            Product.category_fk == args['id']
        )
    )]
    product_max = max(products, key=lambda v: v.price)
    product_min = min(products, key=lambda v: v.price)
    print(product_min.price, product_max.price)
    max_min_filter = {
        'id': 0,
        'key': 'price_range',
        'type': 'range',
        'is_filter': 1,
        'values': {
            'max': product_max.price,
            'min': product_min.price
        }
    }
    return [*filters, max_min_filter]


@cache.cached(300)
@arguments(SearchBySubCategorySchema)
@response(SpecificationSchema(many=True))
def get_filters_by_subcategory(args):
    filters = db.session.scalars(
        Specification.select()
        .join(SpecificationValue)
        .join(SpecificationToProduct)
        .join(Product)
        .distinct(Specification.id)
        .where(
            and_(
                Product.subcategory_fk == args['id'],
                Specification.is_filter == True
            )
        )
    )
    products = [*db.session.scalars(
        Product.select()
        .where(
            Product.category_fk == args['id']
        )
    )]
    product_max = max(products, key=lambda v: v.price)
    product_min = min(products, key=lambda v: v.price)
    print(product_min.price, product_max.price)
    max_min_filter = {
        'id': 0,
        'key': 'price_range',
        'type': 'range',
        'is_filter': 1,
        'values': {
            'max': product_max.price,
            'min': product_min.price
        }
    }
    return [*filters, max_min_filter]


def get_lambda(data_value):
    if data_value['available']:
        return lambda: ProductAvailability.amount > 0
    else:
        return lambda: ProductAvailability.amount >= 0


@cross_origin()
@body(FiltersNewSchema)
@response(ProductSchema(many=True))
def get_by_filters(data):
    available_lambda = get_lambda(data)

    if not data['filters']:
        return db.session.scalars(
            Product.select()
            .join(ProductAvailability)
            .where(
                and_(
                    Product.price >= data['min'],
                    Product.price <= data['max'],
                    Product.category_fk == data['category_id'],
                    available_lambda
                )
            )
        )

    candidates = []
    candidates = set()
    for f in data['filters']:
        query_result = db.session.scalars(
            Product.select()
            .join(ProductAvailability)
            .join(SpecificationToProduct)
            .where(
                and_(
                    SpecificationToProduct.specification_id.in_(f['specs']),
                    Product.price >= data['min'],
                    Product.price <= data['max'],
                    Product.category_fk == data['category_id'],
                    available_lambda
                )
            ))

        if not candidates:
            candidates = set(product for product in query_result)
        else:
            candidates = candidates.intersection(set(product for product in query_result))

    # ids = set(product for candidate in candidates for product in candidate)
    # current_app.logger.info(ids)
    current_app.logger.info([candidate.id for candidate in candidates])
    return candidates


@cross_origin()
@body(FiltersSubcategorySchema)
@response(ProductSchema(many=True))
def get_by_subcategory_filters(data):
    available_lambda = get_lambda(data)

    if not data['filters']:
        return db.session.scalars(
            Product.select()
            .join(ProductAvailability)
            .where(
                and_(
                    Product.price >= data['min'],
                    Product.price <= data['max'],
                    Product.subcategory_fk == data['subcategory_id'],
                    available_lambda
                )
            )
        )

    candidates = set()
    for f in data['filters']:
        query_result = db.session.scalars(
            Product.select()
            .join(ProductAvailability)
            .join(SpecificationToProduct)
            .where(
                and_(
                    SpecificationToProduct.specification_id.in_(f['specs']),
                    Product.price >= data['min'],
                    Product.price <= data['max'],
                    Product.subcategory_fk == data['subcategory_id'],
                    available_lambda
                )
            ))

        if not candidates:
            candidates = set(product for product in query_result)
        else:
            candidates = candidates.intersection(set(product for product in query_result))

    # ids = set(product for candidate in candidates for product in candidate)
    # current_app.logger.info(ids)
    current_app.logger.info([candidate.id for candidate in candidates])
    return candidates



# def get_by_subcategory_filters(data):
#     candidates = []
#     if data['available']:
#         available_lambda = lambda: ProductAvailability.amount > 0
#     else:
#         available_lambda = lambda: ProductAvailability.amount >= 0
#
#     if data['filters']:
#         for f in data['filters']:
#             query = db.session.scalars(
#                 Product.select()
#                 .join(ProductAvailability)
#                 .join(SpecificationToProduct)
#                 .where(
#                     and_(
#                         SpecificationToProduct.specification_id.in_(f['specs']),
#                         Product.price >= data['min'],
#                         Product.price <= data['max'],
#                         Product.category_fk == data['subcategory_id'],
#                         available_lambda
#                     )
#                 )
#             )
#             candidates.append(query)
#         ids = []
#         for candidate in candidates:
#             for product in candidate:
#                 ids.append(product.id)
#         # https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
#         resp = list(set([x for x in ids if ids.count(x) == len(data['filters'])]))
#         return db.session.scalars(
#             Product.select().where(
#                 Product.id.in_(resp)
#             )
#         )
#     return db.session.scalars(
#         Product.select()
#         .join(ProductAvailability)
#         .where(
#             and_(
#                 Product.price >= data['min'],
#                 Product.price <= data['max'],
#                 Product.category_fk == data['subcategory_id'],
#                 available_lambda
#             )
#         )
#     )

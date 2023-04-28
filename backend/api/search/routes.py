from flask import current_app, jsonify
from flask_jwt_extended import jwt_required
from api.search_utils import query_index, add_to_index, remove_from_index
from api.models import Product
from api.utils import permission_required
from api.app import db
from .schema import SearchProductSchema
from api.product.schema import ProductShortSchema
from apifairy import body, response


@jwt_required()
@permission_required('admin.search.reindex')
def reindex():
    # TODO: Вынести в celery
    all_products = db.session.scalars(Product.select())
    for product in all_products:
        add_to_index('products', product)
        current_app.logger.info(f'{product.id} reindexed')
    return jsonify(code=200, msg='reindexed')


@response(ProductShortSchema(many=True))
@body(SearchProductSchema)
def search_product(args):
    res, raw = query_index('products', args['query'], 5)
    products = [db.session.get(Product, pid) for pid in res]
    return products

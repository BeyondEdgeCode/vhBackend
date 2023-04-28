from flask import current_app, jsonify

from api.models import Product, ProductAvailability, Shop
from api import db
from .schema import ProductSchema, ProductCreateSchema
from api.schemas.category import SearchByCategorySchema, SearchBySubCategorySchema
from apifairy import response, body, arguments
from api.utils import permission_required
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from api.app import cache
from api.search_utils import add_to_index


@cache.cached(120)
@arguments(SearchByCategorySchema)
@response(ProductSchema(many=True))
def get_by_category(args):
    products = db.session.scalars(Product.select().where(Product.category_fk == args['id']))
    return products


@cache.cached(120)
@arguments(SearchBySubCategorySchema)
@response(ProductSchema(many=True))
def get_by_subcategory(args):
    products = db.session.scalars(Product.select().where(Product.subcategory_fk == args['id']))
    return products


@jwt_required()
@permission_required('admin.product.create')
@body(ProductCreateSchema)
@response(ProductSchema)
def create(args):
    product = Product(**args)
    db.session.add(product)
    db.session.commit()

    shops = db.session.scalars(Shop.select())
    for shop in shops:
        db.session.add(ProductAvailability(product=product, shop=shop, amount=0))
    db.session.commit()

    add_to_index('products', product)
    return product


#
# @jwt_required()
# @permission_required('admin.search.read')
# def read_search():


@cache.cached(600)
@response(ProductSchema(many=True))
def get_last_created():
    return db.session.scalars(
        Product.select().order_by(
            desc(Product.created_at)
        ).limit(10)
    )


@cache.cached(120)
@response(ProductSchema)
def get_one(product_id):
    return db.session.scalar(
        Product.select().where(Product.id == product_id)
    )


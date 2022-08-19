from flask import request
from api.models import Product
from api import db
from api.schemas.product import ProductSchema, ProductCreateSchema
from api.schemas.category import SearchByCategorySchema, SearchBySubCategorySchema
from apifairy import response, body, arguments
from api.utils import permission_required
from flask_jwt_extended import jwt_required

product_schema = ProductSchema(many=True)
single_product_schema = ProductSchema()
product_create = ProductCreateSchema()
search_by_category = SearchByCategorySchema()
search_by_subcategory = SearchBySubCategorySchema()


@arguments(search_by_category)
@response(product_schema)
def get_by_category(args):
    products = db.session.scalars(Product.select().where(Product.category_fk == args['id']))
    return products


@arguments(search_by_subcategory)
@response(product_schema)
def get_by_subcategory(args):
    products = db.session.scalars(Product.select().where(Product.subcategory_fk == args['id']))
    return products


@jwt_required()
@permission_required('admin.product.create')
@body(product_create)
@response(single_product_schema)
def create(args):
    product = Product(**args)
    db.session.add(product)
    db.session.commit()
    return product

from flask import jsonify

from api.models import Product, ProductAvailability, Shop, ProductSpecification
from api import db
from api.schemas.product import ProductSchema, ProductCreateSchema, SpecificationSchema, GetSpecificationSchema
from api.schemas.product import ModSpecificationSchema
from api.schemas.category import SearchByCategorySchema, SearchBySubCategorySchema
from apifairy import response, body, arguments
from api.utils import permission_required
from flask_jwt_extended import jwt_required
from sqlalchemy import desc

product_schema = ProductSchema(many=True)
single_product_schema = ProductSchema()
product_create = ProductCreateSchema()
search_by_category = SearchByCategorySchema()
search_by_subcategory = SearchBySubCategorySchema()
specifications_schema = SpecificationSchema(many=True)
get_specification_schema = GetSpecificationSchema()
mod_specification_schema = ModSpecificationSchema(many=True)


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

    shops = db.session.scalars(Shop.select())
    for shop in shops:
        db.session.add(ProductAvailability(product=product, shop=shop, amount=0))
    db.session.commit()

    return product


@response(product_schema)
def get_last_created():
    return db.session.scalars(
        Product.select().order_by(
            desc(Product.created_at)
        )
    )


@response(single_product_schema)
def get_one(product_id):
    return db.session.scalar(
        Product.select().where(Product.id == product_id)
    )

# @jwt_required()
# @permission_required('admin.product.delete')
# @body()


@jwt_required()
@permission_required('admin.specifications.add')
@body(specifications_schema)
@response(specifications_schema)
def add_specifications(args):
    commit_list = []
    for arg in args:
        commit_list.append(ProductSpecification(**arg))

    db.session.add_all(commit_list)
    db.session.commit()

    return commit_list


@arguments(get_specification_schema)
@response(specifications_schema)
def get_specifications(args):
    return db.session.scalars(
        ProductSpecification.select().where(ProductSpecification.product_id == args['product_id'])
    )


@body(mod_specification_schema)
@response(specifications_schema)
def edit_specification(args):
    commit_list = []
    for arg in args:
        if specification := db.session.get(ProductSpecification, arg['id']):
            specification.key = arg['key']
            specification.value = arg['value']
            commit_list.append(specification)

    db.session.add_all(commit_list)
    db.session.commit()

    return commit_list


def delete_specification():
    pass

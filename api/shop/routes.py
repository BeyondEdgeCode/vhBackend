from flask import request
from flask_jwt_extended import jwt_required
from api.utils import permission_required
from api.schemas.shop import ShopSchema
from api.models import Shop, ProductAvailability, Product
from api.app import db
from apifairy import body, response

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)


@jwt_required()
@permission_required('admin.shop.create')
@response(shop_schema)
@body(shop_schema)
def create(args):
    shop = Shop(**args)
    db.session.add(shop)
    db.session.commit()

    product_availabilities = []
    all_products = db.session.scalars(Product.select())
    for product in all_products:
        product_availabilities.append(ProductAvailability(product=product, shop=shop))

    db.session.add_all(product_availabilities)
    db.session.commit()

    return shop


@response(shops_schema)
def get_all():
    shops = db.session.scalars(Shop.select())
    return shops

from flask import request
from api.models import Product
from api import db


def get_by_category(cat_id):
    products = db.session.scalars(Product.select().where(Product.category_fk == int(cat_id)))
    return products

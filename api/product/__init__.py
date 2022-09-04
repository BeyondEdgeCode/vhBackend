from flask import Blueprint
from .routes import get_by_category, get_by_subcategory, create, get_last_created, get_one

product = Blueprint('product', __name__)

product.add_url_rule('/product/get_latest', 'product_get_latest', get_last_created, methods=['GET'])
product.add_url_rule('/product/get_by_category', 'product_get_by_category', get_by_category, methods=['GET'])
product.add_url_rule('/product/get_by_subcategory', 'product_get_by_subcategory', get_by_subcategory, methods=['GET'])
product.add_url_rule('/product', 'product_create', create, methods=['POST'])
product.add_url_rule('/product/<int:product_id>', 'product_get_one', get_one, methods=['GET'])
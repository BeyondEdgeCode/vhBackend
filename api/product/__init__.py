from flask import Blueprint
from .routes import get_by_category, get_by_subcategory, create

product = Blueprint('product', __name__)

product.add_url_rule('/product/get_by_category', 'product_get_by_category', get_by_category, methods=['GET'])
product.add_url_rule('/product/get_by_subcategory', 'product_get_by_subcategory', get_by_subcategory, methods=['GET'])
product.add_url_rule('/product', 'product_create', create, methods=['POST'])
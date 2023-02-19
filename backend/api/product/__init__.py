from flask import Blueprint
from .routes import get_by_category, get_by_subcategory, create, get_last_created, get_one, add_specifications
from .routes import get_specifications, edit_specification
from .reviews import reviews
from .filters import filters
from .category import category
from .favourite import favourite

product = Blueprint('product', __name__)

product.add_url_rule('/product/get_latest', 'product_get_latest', get_last_created, methods=['GET'])
product.add_url_rule('/product/get_by_category', 'product_get_by_category', get_by_category, methods=['GET'])
product.add_url_rule('/product/get_by_subcategory', 'product_get_by_subcategory', get_by_subcategory, methods=['GET'])
product.add_url_rule('/product', 'product_create', create, methods=['POST'])
product.add_url_rule('/product/<int:product_id>', 'product_get_one', get_one, methods=['GET'])
product.add_url_rule('/product/specification', 'product_specifications_get', get_specifications, methods=['GET'])
product.add_url_rule('/product/specification', 'product_specifications_add', add_specifications, methods=['POST'])
product.add_url_rule('/product/specification', 'product_specifications_patch', edit_specification, methods=['PATCH'])

product.register_blueprint(reviews)
product.register_blueprint(filters)
product.register_blueprint(category)
product.register_blueprint(favourite)
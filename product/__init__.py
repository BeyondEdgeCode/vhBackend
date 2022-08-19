from flask import Blueprint
from .routes import get_by_category

product = Blueprint('product', __name__)

product.add_url_rule('/product?cat_id=<cat_id:int>')
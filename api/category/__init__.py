from flask import Blueprint
from .routes import create, get_all, create_subcategory


category = Blueprint('category', __name__)

category.add_url_rule('/category/create', 'category_create', create, methods=['POST'])
category.add_url_rule('/category', 'category_get_all', get_all, methods=['GET'])
category.add_url_rule('/subcategory/create', 'subcategory_create', create_subcategory, methods=['POST'])
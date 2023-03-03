from flask import Blueprint
from .routes import get_filters_by_category, get_by_filters, get_by_subcategory_filters, get_filters_by_subcategory

filters = Blueprint('filters', __name__, url_prefix='/product/filters')

filters.add_url_rule('/get_by_category', 'get_by_category', get_filters_by_category, methods=['GET'])
filters.add_url_rule('/get_by_subcategory', 'get_by_subcategory', get_filters_by_subcategory, methods=['GET'])
filters.add_url_rule('/get_products_by_category', 'get_products_by_category', get_by_filters, methods=['POST'])
filters.add_url_rule('/get_products_by_subcategory', 'get_products_by_subcategory', get_by_subcategory_filters, methods=['POST'])

from flask import Blueprint
from .routes import get_filters_by_category, get_by_filters

filters = Blueprint('filters', __name__, url_prefix='/product/filters')

filters.add_url_rule('/get_by_category', 'filters_get', get_filters_by_category, methods=['GET'])
filters.add_url_rule('/get_products', 'filters_get_products', get_by_filters, methods=['POST'])

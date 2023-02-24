from flask import Blueprint
from .routes import get_filters_by_category

filters = Blueprint('filters', __name__, url_prefix='/product/filters')

filters.add_url_rule('/get_by_category', 'filters_get', get_filters_by_category, methods=['GET'])
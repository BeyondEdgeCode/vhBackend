from flask import Blueprint
from .routes import get_filters

filters = Blueprint('filters', __name__, url_prefix='/filters')

filters.add_url_rule('/get_by_category', 'filters_get', get_filters, methods=['GET'])
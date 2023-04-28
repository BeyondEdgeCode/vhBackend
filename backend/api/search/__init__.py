from flask import Blueprint
from .routes import reindex, search_product

search = Blueprint('search', __name__, url_prefix='/search')

search.add_url_rule('/', 'search', search_product, methods=['POST'])
search.add_url_rule('/reindex', 'reindex', reindex, methods=['GET'])

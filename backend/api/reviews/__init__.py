from flask import Blueprint
from .routes import create, get

reviews = Blueprint('reviews', __name__, url_prefix='/reviews')

reviews.add_url_rule('/create', 'review_create', create, methods=['POST'])
reviews.add_url_rule('/<int:product_id>', 'reviews_get', get, methods=['GET'])
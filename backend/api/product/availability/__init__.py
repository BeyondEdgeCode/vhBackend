from flask import Blueprint
from .routes import edit, get_all, get_by_shop

availability = Blueprint('availability', __name__, url_prefix='/product/availability')

availability.add_url_rule('/edit', 'availability_edit', edit, methods=['PATCH'])
availability.add_url_rule('/all', 'availability_get_all', get_all, methods=['GET'])
availability.add_url_rule('/shop', 'availabiloty_get_by_shop', get_by_shop, methods=['GET'])
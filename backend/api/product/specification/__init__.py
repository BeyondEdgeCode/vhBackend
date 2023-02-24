from flask import Blueprint
from .routes import create_specification, create_spec_value, assign_spec_to_product, get_all_specifications


specification = Blueprint('specification', __name__, url_prefix='/product/specification')

specification.add_url_rule('/get_all', 'specification_get_all', get_all_specifications, methods=['GET'])


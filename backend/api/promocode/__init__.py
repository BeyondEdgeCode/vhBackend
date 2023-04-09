from flask import Blueprint
from .routes import create_promotype, get_promotypes, create, assign, get

promocode = Blueprint('promocode', __name__, url_prefix='/promocode')

# TODO: Доделать CRUD
promocode.add_url_rule('/type/create', 'type_create', create_promotype, methods=['POST'])
promocode.add_url_rule('/type/get', 'type_get', get_promotypes, methods=['GET'])
promocode.add_url_rule('/create', 'create', create, methods=['POST'])
promocode.add_url_rule('/get', 'get', get, methods=['GET'])
promocode.add_url_rule('/assign', 'assign', assign, methods=['POST'])
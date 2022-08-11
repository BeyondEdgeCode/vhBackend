import json
from flask import Blueprint
from .models import User, Shop, Settings
from .utils import get_all, get_first

testing = Blueprint('testing', __name__)


@testing.get('/')
def root():
    query = get_all(Settings.select())
    parsed_query = [[r.key, r.value] for r in query]
    return f'Shops {parsed_query}'


@testing.get('/api/testing/getUsers')
def getusers():
    users = User.select()
    return json.dumps([u.email for u in users])

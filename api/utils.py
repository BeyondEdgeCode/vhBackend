from .app import db
from flask import request
from werkzeug.exceptions import BadRequest, HTTPException

def get_first(query): return db.session.scalar(query)


def get_first_or_false(query):
    scalar = db.session.scalar(query)
    return scalar if scalar else False


def get_all(query): return db.session.scalars(query)



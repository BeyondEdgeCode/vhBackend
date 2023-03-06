from api.app import ma
from marshmallow.fields import Integer, String

class ResponseSchema(ma.Schema):

    status = Integer(required=True)
    error = String()
    message = String()


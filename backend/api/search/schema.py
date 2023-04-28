from api.app import ma
from marshmallow.fields import Integer, String, List, DateTime

class SearchProductSchema(ma.SQLAlchemySchema):
    query = String(required=True)
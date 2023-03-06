from api.app import ma
from api.models import Shop


class CreateOrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Shop

    

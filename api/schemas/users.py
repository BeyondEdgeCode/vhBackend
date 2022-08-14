from api import ma
from api.models import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        # ordered = True
        include_fk = True

    id = ma.auto_field()
    email = ma.auto_field()
    email_confirmed = ma.auto_field()
    firstName = ma.auto_field()
    lastName = ma.auto_field()
    birthday = ma.auto_field()
    city = ma.auto_field()
    street = ma.auto_field()
    building = ma.auto_field()
    flat = ma.auto_field()
    zipcode = ma.auto_field()
    notificationsAgree = ma.auto_field()
    registrationDate = ma.auto_field()

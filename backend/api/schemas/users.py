from api import ma
from api.models import User
import re
from marshmallow.exceptions import ValidationError
from marshmallow.fields import Str


def check_phone(number) -> None:
    phonematch = re.compile("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")
    if not phonematch.match(number):
        raise ValidationError('Введен некорректный номер телефона.')


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True
        include_fk = True

    id = ma.auto_field()
    email = ma.auto_field()
    email_confirmed = ma.auto_field()
    firstName = ma.auto_field()
    lastName = ma.auto_field()
    birthday = ma.auto_field()
    mobilephone = Str(validate=check_phone)
    city = ma.auto_field()
    street = ma.auto_field()
    building = ma.auto_field()
    flat = ma.auto_field()
    zipcode = ma.auto_field()
    notificationsAgree = ma.auto_field()
    registrationDate = ma.auto_field()


class UserReviewSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_fk = True

    firstName = ma.auto_field(dump_only=True)

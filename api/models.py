from datetime import datetime, timedelta
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from api.app import db


class Updatable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class User(Updatable, db.Model):
    __tablename__ = 'Users'

    # Основная информация
    id = Column(Integer, primary_key=True)
    email = Column(String(120), index=True, unique=True, nullable=False)
    password = Column(String(128))
    role = Column(Integer, ForeignKey('UserRole.id'))

    # Личная информация
    firstName = Column(String(64))
    lastName = Column(String(64), index=True)
    birthday = Column(DateTime)

    # Адрес доставки
    city = Column(String(128))
    street = Column(String(128))
    building = Column(String(64))
    flat = Column(String(32))
    zipcode = Column(Integer)

    # Системная информация
    notificationsAgree = Column(Boolean, default=True)
    registrationDate = Column(DateTime, default=datetime.utcnow)

    userRole = relationship('UserRole', back_populates='users')

class Shop(db.Model):
    __tablename__ = 'Shop'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)

    city = Column(String(128))
    street = Column(String(128))
    building = Column(String(64))
    description = Column(String(512))
    preview = Column(String(1024))


class UserRole(db.Model):
    __tablename__ = 'UserRole'

    id = Column(Integer, primary_key=True)
    roleName = Column(String(64), unique=True, nullable=False)
    roleDescription = Column(String(128))

    users = relationship('User', back_populates='userRole')
    userRoleRights = relationship('UserRoleRights', back_populates='userRole')

    def get_rights(self):
        return [i.right for i in self.rights]


class UserRoleRights(db.Model):
    __tablename__ = 'UserRoleRights'

    id = Column(Integer, primary_key=True)
    role = Column(Integer, ForeignKey('UserRole.id', ondelete='CASCADE'))
    right = Column(String(64), nullable=False)

    userRole = relationship('UserRole', back_populates='userRoleRights')


class Category(db.Model):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), index=True)

    subcategories = relationship('SubCategory', back_populates='categories')


class SubCategory(db.Model):
    __tablename__ = 'SubCategory'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), index=True)
    category = Column(Integer, ForeignKey('Category.id', ondelete='CASCADE'))

    categories = relationship('Category', back_populates='subcategories')


class Product(db.Model):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), index=True, nullable=False)
    description = Column(String(1024), index=True)
    price = Column(Float(2), nullable=False, index=True)

    # TODO: Add relationship to Product and Product<->Category/Product<->SubCategory
    category = Column(Integer, ForeignKey('Category.id'), nullable=False)
    subcategory = Column(Integer, ForeignKey('SubCategory.id', ondelete='CASCADE'))

    specifications = Column(JSON, default=None)


class ProductAvailability(db.Model):
    __tablename__ = 'ProductAvailability'

    id = Column(Integer, primary_key=True)
    # TODO: Add relationships for ProductAvailability<->Product-Product and ProductAvailability<->Shop
    product = Column(Integer, ForeignKey('Product.id'))
    shop = Column(Integer, ForeignKey('Shop.id'))


class Reserve(db.Model):
    __tablename__ = 'Reserve'

    # TODO: Add relationship to Reserve<->User, Reserve<->Product
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('User.id'))
    product = Column(Integer, ForeignKey('Product.id', ondelete='CASCADE'))
    # order = Column(Integer, ForeignKey('Order.id')) TODO: add Order
    amount = Column(Integer, nullable=False)


class Favourite(db.Model):
    __tablename__ = 'Favourite'

    id = Column(Integer, primary_key=True)
    # TODO: Add relationship to Favourite<->User/Favourite<->Product
    user = Column(Integer, ForeignKey('User.id'))
    product = Column(Integer, ForeignKey('Product.id'))


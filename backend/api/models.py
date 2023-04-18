import enum
from datetime import datetime, timedelta
from statistics import mean
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Float, DateTime, Boolean, JSON, Enum, func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from api.app import db
from flask_jwt_extended import get_current_user
import urllib
from .app import cache


class Updatable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class OrderStatus(enum.Enum):
    awaiting_payment = 0
    forming = 1
    waiting_to_receive = 2
    in_delivery = 3
    finished = 4
    canceled_by_system = 5
    canceled_by_user = 6


class PromoRestriction(enum.Enum):
    product_only = 0
    category_only = 1
    subcategory_only = 2
    all = 3


class DeliveryType(enum.Enum):
    pickup = 0
    delivery = 1


class PaymentType(enum.Enum):
    prepay = 0
    postpayment = 1


class ObjectStorage(db.Model):
    __tablename__ = 'ObjectStorage'

    id = Column(Integer, primary_key=True)
    link = Column(String(1024), index=True)

    product = relationship('Product', back_populates='image')
    other_images = relationship('OtherImages', back_populates='image')
    imagecarousel = relationship('ImageCarousel', back_populates='image')


class User(db.Model):
    __tablename__ = 'Users'

    # Основная информация
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), index=True, unique=True, nullable=False)
    email_confirmed = Column(Boolean, default=False)
    password = Column(String(128), nullable=False)
    role_fk = Column(Integer, ForeignKey('UserRole.id'), nullable=False)

    # Личная информация
    firstName = Column(String(64), index=True)
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

    role = relationship('UserRole', back_populates='users')
    reserved = relationship('ProductReserve', back_populates='user')
    likes = relationship('Favourite', back_populates='user')
    basket = relationship('Basket', back_populates='user')
    reviews = relationship('Reviews', back_populates='user')
    email_confirmations = relationship('EmailConfirmation', back_populates='user')
    revokedtokens = relationship('RevokedTokens', back_populates='user')

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    def update_password(self, new_password, old_password) -> bool:
        if check_password_hash(self.password, old_password):
            self.password = generate_password_hash(new_password)
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False


class EmailConfirmation(db.Model):
    __tablename__ = 'EmailConfirmation'

    id = Column(Integer, primary_key=True)
    user_fk = Column(Integer, ForeignKey('Users.id'), nullable=False)
    key = Column(String(512), nullable=False, index=True)
    used = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow()+timedelta(days=3))

    user = relationship('User', back_populates='email_confirmations')


class Shop(db.Model):
    __tablename__ = 'Shop'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)

    city = Column(String(128))
    street = Column(String(128))
    building = Column(String(64))
    description = Column(String(512))
    preview = Column(String(1024))

    available = relationship('ProductAvailability', back_populates='shop')
    orders = relationship('Order', back_populates='shop')


class UserRole(db.Model):
    __tablename__ = 'UserRole'

    id = Column(Integer, primary_key=True)
    roleName = Column(String(64), unique=True, nullable=False)
    roleDescription = Column(String(128))
    is_default = Column(Boolean, default=False)

    users = relationship('User', back_populates='role')
    permissions = relationship('UserRolePermission', back_populates='role')

    @cache.memoize(50)
    def get_rights(self):
        return [i.permission.key for i in self.permissions]

    def __repr__(self):
        return self.roleName

    def __str__(self):
        return self.roleName


class UserRolePermission(db.Model):
    __tablename__ = 'UserRolePermission'

    id = Column(Integer, primary_key=True)
    role_fk = Column(Integer, ForeignKey('UserRole.id', ondelete='CASCADE'))
    permission_fk = Column(Integer, ForeignKey('Permission.id'), nullable=False)

    role = relationship('UserRole', back_populates='permissions')
    permission = relationship('Permission', back_populates='roles')


class Permission(db.Model):
    __tablename__ = 'Permission'

    id = Column(Integer, primary_key=True)
    key = Column(String(128), nullable=False, unique=True)
    description = Column(String(128))

    roles = relationship('UserRolePermission', back_populates='permission')


class Category(db.Model):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), index=True)
    not_for_children = Column(Boolean, nullable=False, default=False)

    subcategories = relationship('SubCategory', back_populates='categories')
    products = relationship('Product', back_populates='categories')


class SubCategory(db.Model):
    __tablename__ = 'SubCategory'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), index=True)
    category_fk = Column(Integer, ForeignKey('Category.id', ondelete='CASCADE'))

    categories = relationship('Category', back_populates='subcategories')
    products = relationship('Product', back_populates='subcategory')


class Product(db.Model):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), index=True, nullable=False)
    description = Column(String(1024), index=True)
    image_fk = Column(Integer, ForeignKey('ObjectStorage.id'))
    price = Column(Float(2), nullable=False, index=True)
    is_child = Column(Boolean, nullable=False)

    parent_fk = Column(Integer, ForeignKey('Product.id'), nullable=True)
    category_fk = Column(Integer, ForeignKey('Category.id'), nullable=False)
    subcategory_fk = Column(Integer, ForeignKey('SubCategory.id', ondelete='CASCADE'))

    created_at = Column(DateTime, default=datetime.utcnow)

    # referenced_product = relationship('Product', back_populates='referenced_product')
    referenced_product = relationship('Product')
    categories = relationship('Category', back_populates='products')
    subcategory = relationship('SubCategory', back_populates='products')
    available = relationship('ProductAvailability', back_populates='product')
    reserved = relationship('ProductReserve', back_populates='product')
    liked = relationship('Favourite', back_populates='product')
    in_baskets = relationship('Basket', back_populates='product')
    image = relationship('ObjectStorage', back_populates='product')
    other_images = relationship('OtherImages', back_populates='product')
    inorders = relationship('OrderItem', back_populates='product')
    reviews = relationship('Reviews', back_populates='product')
    specifications = relationship('SpecificationToProduct', back_populates='product')
    discounts = relationship('DiscountToProduct', back_populates='product')
    promocodes = relationship('PromocodeToProduct', back_populates='product')



    @property
    def image_link(self):
        return 'https://storage.yandexcloud.net/vapehookahstatic/' + urllib.parse.quote(self.image.link)

    @property
    def avg_stars(self):
        total = 0
        for review in self.reviews:
            total += review.stars

        try:
            return total/len(self.reviews)
        except ZeroDivisionError:
            return 0

    @property
    def all_specs(self):
        return [spec.specification_id for spec in self.specifications]


class OtherImages(db.Model):
    __tablename__ = 'OtherImages'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.id'), nullable=False, index=True)
    image_id = Column(Integer, ForeignKey('ObjectStorage.id'), nullable=False)

    image = relationship('ObjectStorage', back_populates='other_images')
    product = relationship('Product', back_populates='other_images')

    @property
    def links(self):
        return [link for link in self.image.link]


class ProductAvailability(db.Model):
    __tablename__ = 'ProductAvailability'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('Shop.id'), nullable=False)
    amount = Column(Integer, nullable=False, default=0)

    product = relationship('Product', back_populates='available')
    shop = relationship('Shop', back_populates='available')
    reserved = relationship('ProductReserve', back_populates='pa')


class ProductReserve(db.Model):
    __tablename__ = 'ProductReserve'

    id = Column(Integer, primary_key=True)
    user_fk = Column(Integer, ForeignKey('Users.id'))
    product_fk = Column(Integer, ForeignKey('Product.id', ondelete='CASCADE'))
    pa_fk = Column(Integer, ForeignKey('ProductAvailability.id', ondelete='CASCADE')) # ProductAvailability_FK
    order_fk = Column(Integer, ForeignKey('Order.id'))
    amount = Column(Integer, nullable=False)

    user = relationship('User', back_populates='reserved')
    product = relationship('Product', back_populates='reserved')
    pa = relationship('ProductAvailability', back_populates='reserved')
    order = relationship('Order', back_populates='reserved')


class Favourite(db.Model):
    __tablename__ = 'Favourite'

    id = Column(Integer, primary_key=True)
    user_fk = Column(Integer, ForeignKey('Users.id'), index=True)
    product_fk = Column(Integer, ForeignKey('Product.id'))

    user = relationship('User', back_populates='likes')
    product = relationship('Product', back_populates='liked')


class Basket(db.Model):
    __tablename__ = 'Basket'

    id = Column(Integer, primary_key=True)
    user_fk = Column(Integer, ForeignKey('Users.id'), nullable=False, index=True)
    product_fk = Column(Integer, ForeignKey('Product.id'), nullable=False)
    amount = Column(Integer, nullable=False, default=1)

    user = relationship('User', back_populates='basket')
    product = relationship('Product', back_populates='in_baskets')


class Order(db.Model):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    user_fk = Column(Integer, ForeignKey('Users.id'), nullable=False, index=True)
    status = Column(Enum(OrderStatus), nullable=False)
    delivery_type = Column(Enum(DeliveryType), nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    sum = Column(Float(2), nullable=False)
    used_promocode = Column(Integer, ForeignKey('Promocode.id'), nullable=True)
    shop_fk = Column(Integer, ForeignKey('Shop.id'), index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    shop = relationship('Shop', back_populates='orders')
    reserved = relationship('ProductReserve', back_populates='order')
    items = relationship('OrderItem', back_populates='order')
    promocode_ref = relationship('Promocode', back_populates='used_at')


class OrderItem(db.Model):
    __tablename__ = 'OrderItem'

    id = Column(Integer, primary_key=True)
    product_fk = Column(Integer, ForeignKey('Product.id'), nullable=False)
    order_fk = Column(Integer, ForeignKey('Order.id'), nullable=False)
    price = Column(Float(2), nullable=False)
    amount = Column(Integer, nullable=False)
    item_sum = Column(Float(2), nullable=False)

    product = relationship('Product', back_populates='inorders')
    order = relationship('Order', back_populates='items')


class Settings(db.Model):
    __tablename__ = 'Settings'

    id = Column(Integer, primary_key=True)
    key = Column(String(128), index=True)
    value = Column(String(128))

    def __repr__(self):
        return f'{self.__tablename__}({self.key}, {self.value})'


class Reviews(db.Model):
    __tablename__ = 'Reviews'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    stars = Column(Integer, nullable=False)
    text = Column(String(1024))
    created_at = Column(DateTime, server_default=func.now())

    product = relationship('Product', back_populates='reviews')
    user = relationship('User', back_populates='reviews')


class PromoType(db.Model):
    __tablename__ = 'PromoType'
    id = Column(Integer, primary_key=True)
    type = Column(String(64), nullable=False)

    promocodes = relationship('Promocode', back_populates='promotype')


class Promocode(db.Model):
    __tablename__ = 'Promocode'

    id = Column(Integer, primary_key=True)
    promotype_fk = Column(Integer, ForeignKey('PromoType.id'), nullable=False)
    key = Column(String(64), nullable=False, index=True)
    value = Column(Integer, nullable=False)
    is_enabled = Column(Boolean, default=True)
    available_until = Column(DateTime, nullable=False, server_default=func.now())
    new_only = Column(Boolean, default=False)
    min_sum = Column(Float(2), default=0.0)
    max_usages = Column(Integer, default=0)
    current_usages = Column(Integer, default=0)

    promotype = relationship('PromoType', back_populates='promocodes')
    to_products = relationship('PromocodeToProduct', back_populates='promocode')
    used_at = relationship('Order', back_populates='promocode_ref')


class PromocodeToProduct(db.Model):
    __tablename__ = 'PromocodeToProduct'

    id = Column(Integer, primary_key=True)
    promocode_id = Column(ForeignKey('Promocode.id'), nullable=False)
    product_id = Column(ForeignKey('Product.id'), nullable=False)

    product = relationship('Product', back_populates='promocodes')
    promocode = relationship('Promocode', back_populates='to_products')


class Discount(db.Model):
    __tablename__ = 'Discount'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    discount_type = Column(String(64), nullable=False, index=True)
    value = Column(Integer)

    to_products = relationship('DiscountToProduct', back_populates='discount')


class DiscountToProduct(db.Model):
    __tablename__ = 'DiscountToProduct'

    id = Column(Integer, primary_key=True)
    discount_id = Column(ForeignKey('Discount.id'), nullable=False)
    product_id = Column(ForeignKey('Product.id'), nullable=False)

    product = relationship('Product', back_populates='discounts')
    discount = relationship('Discount', back_populates='to_products')


class RevokedTokens(db.Model):
    __tablename__ = 'RevokedTokens'

    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False, index=True)
    type = Column(String(16), nullable=False)
    user_fk = Column(Integer, ForeignKey('Users.id'), nullable=False, default=lambda: get_current_user().id)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship('User', back_populates='revokedtokens')


class ImageCarousel(db.Model):
    __tablename__ = 'ImageCarousel'

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey('ObjectStorage.id'), nullable=False)
    active = Column(Boolean, default=False)

    image = relationship('ObjectStorage', back_populates='imagecarousel')

    @property
    def image_link(self):
        return 'https://storage.yandexcloud.net/vapehookahstatic/' + urllib.parse.quote(self.image.link)


class Specification(db.Model):
    __tablename__ = 'Specification'

    id = Column(Integer, primary_key=True)
    key = Column(String(128), nullable=False, index=True)
    type = Column(String(32), nullable=False)
    is_filter = Column(Boolean, default=False)
    values = relationship('SpecificationValue', back_populates='specification')

    @cache.memoize(120)
    def get_values(self):
        return {spec.id: spec.value for spec in self.values}


class SpecificationValue(db.Model):
    __tablename__ = 'SpecificationValue'

    id = Column(Integer, primary_key=True)
    specification_id = Column(Integer, ForeignKey('Specification.id', ondelete='CASCADE'), nullable=False)
    value = Column(String(128), nullable=False)

    specification = relationship('Specification', back_populates='values')
    products = relationship('SpecificationToProduct', back_populates='specification_value')


class SpecificationToProduct(db.Model):
    __tablename__ = 'SpecificationToProduct'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.id', ondelete='CASCADE'), nullable=False)
    specification_id = Column(Integer, ForeignKey('SpecificationValue.id', ondelete='CASCADE'), nullable=False)

    specification_value = relationship('SpecificationValue', back_populates='products')
    product = relationship('Product', back_populates='specifications')

    @cache.memoize(120)
    def get_specification(self):
        return {
            'key': self.specification_value.specification.key,
            'value': self.specification_value.value
        }

import random
from typing import List
import click
from .models import User, UserRole, UserRolePermission, Permission
from .models import Product, ProductAvailability, Category, \
    Specification, SpecificationValue, SpecificationToProduct,\
    ObjectStorage, Shop
from .app import db
from werkzeug.security import generate_password_hash


@click.group()
def fill():
    """Product table functions"""
    pass


@fill.command('users')
def fill_user():
    user_role = UserRole(roleName='admin', roleDescription='default', is_default=1)
    db.session.add(user_role)
    db.session.commit()
    role_permission = Permission(key='admin.all')
    db.session.add(role_permission)
    db.session.commit()
    user_permission = UserRolePermission(role_fk=user_role.id, permission_fk=role_permission.id)
    db.session.add(user_permission)
    db.session.commit()
    user = User(email='me@evgeniy.host', email_confirmed=True, password=generate_password_hash('test1234'),
                role_fk=user_role.id)
    db.session.add(user)
    db.session.commit()


@fill.command('products')
def fill_products():
    links = ['bgo2u81x1.jpg',
             'f48g89pc2.jpg',
             'by399dfm3.jpg',
             '9w0kwzkq4.jpg',
             'jmd79r2y5.jpg',
             'h13h0tly6.jpg',
             't1p7t4a87.jpg',
             'q06n8jck8.jpg',
             'fzrvsmjk9.jpg',
             'i9f7a8bd10.jpg',
             '4wd7owf6ic1.jpg',
             'i5agi99mic2.jpg',
             'n8h4z6mbic3.jpg',
             '6ozfsr7pic4.jpg']

    objectstorage = [
        ObjectStorage(link=img) for img in links
    ]

    db.session.add_all(objectstorage)
    db.session.commit()

    cat = Category(title='Тестовая')

    shop = Shop(title='Тестовый магазин')

    db.session.add_all([cat, shop])
    db.session.commit()

    products = []
    for link_id in range(1, 15):
        products.append(
            Product(title=f'Товар {link_id}', image_fk=link_id, price=100.00, is_child=False, category_fk=cat.id)
        )

    db.session.add_all(products)
    db.session.commit()

    products_available = []
    for product in products:
        products_available.append(
            ProductAvailability(shop_id=shop.id, product_id=product.id, amount=10)
        )

    db.session.add_all(products_available)
    db.session.commit()

    specifications_names = ['PG/VG', 'Производитель', 'Крепость', 'Никотин']

    specs: List[Specification] = []
    for name in specifications_names:
        specs.append(
            Specification(key=name, type='checkbox', is_filter=True)
        )

    db.session.add_all(specs)
    db.session.commit()

    values_1 = ['50/50', '60/40', '40/60', '70/30']
    values_2 = ['SOAK', 'RELL YELLOW', 'BRUSKO', 'ANGRY VAPE', 'RELL', 'THE SCANDALIST']
    values_3 = ['20mg', '0mg', '30mg', '3mg', '20mg STRONG']
    values_4 = ['Щелочной', 'Солевой']

    spec_1 = []
    spec_2 = []
    spec_3 = []
    spec_4 = []

    for v in values_1:
        spec_1.append(SpecificationValue(specification_id=specs[0].id, value=v))
    for v in values_2:
        spec_2.append(SpecificationValue(specification_id=specs[1].id, value=v))
    for v in values_3:
        spec_3.append(SpecificationValue(specification_id=specs[2].id, value=v))
    for v in values_4:
        spec_4.append(SpecificationValue(specification_id=specs[3].id, value=v))

    db.session.add_all(spec_1)
    db.session.add_all(spec_2)
    db.session.add_all(spec_3)
    db.session.add_all(spec_4)
    db.session.commit()

    spec_to_product = []
    for product in products:
        random_1: SpecificationValue = random.choice(spec_1)
        random_2: SpecificationValue = random.choice(spec_2)
        random_3: SpecificationValue = random.choice(spec_3)
        random_4: SpecificationValue = random.choice(spec_4)

        spec_to_product.append(
            SpecificationToProduct(product_id=product.id, specification_id=random_1.id)
        )
        spec_to_product.append(
            SpecificationToProduct(product_id=product.id, specification_id=random_2.id)
        )
        spec_to_product.append(
            SpecificationToProduct(product_id=product.id, specification_id=random_3.id)
        )
        spec_to_product.append(
            SpecificationToProduct(product_id=product.id, specification_id=random_4.id)
        )

    db.session.add_all(spec_to_product)
    db.session.commit()

    print('Done!')
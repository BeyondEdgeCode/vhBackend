import click
from flask.cli import with_appcontext
from ..models import Shop, ProductAvailability, Product
from api.app import db


@click.group('shop')
def shop():
    """Manage Shop table"""
    pass


@shop.command('create')
@click.option('title', '--title')
def create(title):
    new_shop = Shop(title=title)

    db.session.add(new_shop)
    db.session.commit()

    print(f'New Shop id - {new_shop.id}')

    products = db.session.scalars(Product.select())
    product_availabilities = []
    for product in products:
        product_availabilities.append(ProductAvailability(product=product, shop=new_shop))

    db.session.add_all(product_availabilities)
    db.session.commit()

    print(f'{len(product_availabilities)} Product availabilities created')
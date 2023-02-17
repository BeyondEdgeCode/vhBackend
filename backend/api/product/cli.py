from typing import Optional

import click
from flask.cli import with_appcontext
from ..models import Product, ObjectStorage, Category, SubCategory
from api.app import db


@click.group()
def product():
    """Product table functions"""
    pass


@product.command('create')
@click.option('title', '--title')
@click.option('description', '--desc', required=False)
@click.option('price', '--price')
@click.option('is_child', '--is-child')
@click.option('image', '--image')
@click.option('parent', '--parent', default=None, required=False)
@click.option('category', '--category')
@click.option('subcategory', '--subcategory', default=None, required=False)
def create(title: str, description: Optional[str], price: float, is_child: bool,
           image: int, parent: Optional[int], category: int, subcategory: Optional[int]):
    new_product = Product()
    new_product.title = title
    new_product.price = price
    new_product.is_child = bool(is_child)
    new_product.image_fk = int(image)
    new_product.category_fk = int(category)
    if description is not None:
        new_product.description = description
    if parent is not None:
        new_product.parent_fk = int(parent)
    if subcategory is not None:
        new_product.subcategory_fk = int(subcategory)

    db.session.add(new_product)
    db.session.commit()

    print(f'New id - {new_product.id}')

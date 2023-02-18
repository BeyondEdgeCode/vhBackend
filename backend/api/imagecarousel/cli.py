from typing import List

import click
from flask.cli import with_appcontext
from ..models import ImageCarousel, ObjectStorage
from api.app import db
from prettytable import PrettyTable


@click.group()
def ic():
    """Manage ImageCarousel"""
    pass


@ic.command('create')
@click.option('image_fk', '--image', type=int)
@click.option('active', '--active')
def create(image_fk: int, active: int):
    new_ic = ImageCarousel(image_id=int(image_fk), active=bool(active))
    db.session.add(new_ic)
    db.session.commit()

    print(f'New id {new_ic.id}')


@ic.command('ls')
def ls():
    all_ic: List[ImageCarousel] = db.session.scalars(ImageCarousel.select())
    table = PrettyTable(['id', 'image_id', 'active'])
    for item in all_ic:
        table.add_row([item.id, item.image_id, int(item.active)])

    print(table)
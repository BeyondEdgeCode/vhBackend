import click
from flask.cli import with_appcontext
from ..models import ImageCarousel, ObjectStorage
from api.app import db


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
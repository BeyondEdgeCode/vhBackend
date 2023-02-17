import os
import string
import random
from typing import List

from prettytable import PrettyTable
import click
from flask.cli import with_appcontext
from ..models import ObjectStorage
from .routes import create_s3_session, get_extension
from api.app import db


@click.group()
def s3():
    """Manage S3 storage"""
    pass


@s3.command('upload')
@click.argument('image_link')
def upload(image_link):
    """Upload file to S3"""
    s3_client = create_s3_session()
    filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8)) \
               + os.path.basename(image_link)
    s3_client.upload_file(image_link, 'vapehookahstatic', filename)

    obj = ObjectStorage(link=filename)
    db.session.add(obj)
    db.session.commit()

    print(f'New id {obj.id}')


@s3.command('ls')
def ls():
    """List all objects in bucket"""
    items: List[ObjectStorage] = db.session.scalars(ObjectStorage.select())
    table = PrettyTable(['id', 'link', 'count(linked to product)'])
    for item in items:
        table.add_row([item.id, item.link, len(item.product)])

    print(table)


from typing import List
from typing import Union
import click
from flask.cli import with_appcontext
from api.models import Category, SubCategory
from api.app import db


@click.group()
def category():
    """Manage categories"""
    pass


@category.command('create-category')
@click.argument('title', required=True)
@click.argument('not_for_children', required=True)
def cli_create(title: str, not_for_children: bool):
    """Create new category"""
    cat = Category(title=title, not_for_children=bool(not_for_children))
    db.session.add(cat)
    db.session.commit()
    print(f'New id {cat.id}')


@category.command('create-subcategory')
@click.argument('subcategory_name', required=True)
@click.argument('category_id', required=True)
def cli_create_subcategory(subcategory_name: str, category_id: int):
    category_fk = db.session.scalar(Category.select().where(Category.id == int(category_id)))
    new_sub_category = SubCategory(title=subcategory_name, category_fk=category_fk.id)
    db.session.add(new_sub_category)
    db.session.commit()
    print(f'New id {new_sub_category.id}')


@category.command('update')
@click.argument('category_id', required=True)
@click.argument('title', default=None)
@click.argument('not_for_children', default=None)
def cli_update(category_id: int, title: Union[str, None], not_for_children: Union[str, None]):
    """Update existing category info"""
    cat: Category = db.session.scalar(Category.select().where(Category.id == category_id))
    if title is not None:
        cat.title = title
    if not_for_children is not None:
        cat.not_for_children = bool(not_for_children)
    db.session.add(cat)
    db.session.commit()
    print('Updated.')


@category.command('ls')
def cli_ls():
    """List all categories"""
    categories: List[Category] = db.session.scalars(Category.select())
    from prettytable import PrettyTable
    table = PrettyTable(['id', 'title', 'not_for_children', 'count(subcategories)', 'count(products)'])
    for c in categories:
        table.add_row([c.id, c.title, c.not_for_children, len(c.subcategories), len(c.products)])
    print(table)



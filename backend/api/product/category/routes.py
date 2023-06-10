from flask import request, jsonify
from flask_jwt_extended import jwt_required
from api.utils import permission_required, catch_exception
from api.models import Category, SubCategory
from api import db
from api.schemas.category import CategorySchema, SubCategorySchema
from apifairy import response
from api.app import cache

category_schema = CategorySchema(many=True)


@jwt_required()
@permission_required('admin.category.create')
def create():
    try:
        title = request.json['title']
        not_for_children = bool(request.json['not_for_children'])
    except KeyError or ValueError as e:
        return catch_exception(e, 'Значение поля некорректно')

    new_category = Category(title=title, not_for_children=not_for_children)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(status=200, msg='created', id=new_category.id), 200


@jwt_required()
@permission_required('admin.subcategory.create')
def create_subcategory():
    try:
        title = request.json['title']
        category_id = int(request.json['category_id'])
    except KeyError or ValueError as e:
        return catch_exception(e, 'Значение поля некорректно')

    new_subcategory = SubCategory(title=title, category_fk=category_id)
    db.session.add(new_subcategory)
    db.session.commit()
    return jsonify(status=200, msg='created', id=new_subcategory.id), 200


@cache.cached(600)
@response(category_schema)
def get_all():
    all_categories = db.session.scalars(Category.select())
    return all_categories

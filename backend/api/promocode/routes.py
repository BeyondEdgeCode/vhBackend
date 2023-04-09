from flask import jsonify
from api.models import Category, PromoType, Promocode, PromocodeToProduct, Product, SubCategory
from apifairy import response, body
from .schema import PromoTypeSchema, PromocodeAssignSchema
from .schema import PromocodeSchema
from api.app import db
from flask_jwt_extended import jwt_required
from api.utils import permission_required


@jwt_required()
@permission_required('admin.promocode.type.create')
@body(PromoTypeSchema)
def create_promotype(args):
    new_type = PromoType(**args)
    db.session.add(new_type)
    db.session.commit()
    return jsonify(status=200, msg='Создан')


@jwt_required()
@permission_required('admin.promocode.type.read')
@response(PromoTypeSchema(many=True))
def get_promotypes():
    types = db.session.scalars(PromoType.select())
    return types


@jwt_required()
@permission_required('admin.promocode.create')
@body(PromocodeSchema)
def create(args):
    new_promocode = Promocode(**args)
    db.session.add(new_promocode)
    db.session.commit()
    return jsonify(status=200, msg='Создан')


@jwt_required()
@permission_required('admin.promocode.assign')
@body(PromocodeAssignSchema)
def assign(args):
    promocode: Promocode = db.session.get(Promocode, args['promocode_id'])
    assigned = {products_list.product_id for products_list in promocode.to_products}
    print(args)

    if not promocode:
        return jsonify(status=404, msg='Promocode not found')

    total_added = 0
    total_errors = 0

    for product_id in args['products']:
        product: Product = db.session.get(Product, product_id)
        if not product:
            total_errors += 1
            continue
        if product_id in assigned:
            total_errors += 1
            continue
        db.session.add(
            PromocodeToProduct(promocode_id=promocode.id, product_id=product_id)
        )
        total_added += 1
        assigned.add(product_id)

    for category_id in args['categories']:
        category: Category = db.session.get(Category, category_id)
        if not category:
            total_errors += 1
            continue

        for product in category.products:
            if product.id in assigned:
                total_errors += 1
                continue
            db.session.add(
                PromocodeToProduct(promocode_id=promocode.id, product_id=product.id)
            )
            total_added += 1
            assigned.add(product.id)

    for subcategory_id in args['subcategories']:
        subcategory: SubCategory = db.session.get(SubCategory, subcategory_id)
        if not subcategory:
            total_errors += 1
            continue
        for product in subcategory.products:
            if product.id in assigned:
                total_errors += 1
                continue
            db.session.add(
                PromocodeToProduct(promocode_id=promocode.id, product_id=product.id)
            )
            total_added += 1
            assigned.add(product.id)

    db.session.commit()
    return jsonify(status=200, added=total_added, skipped=total_errors)


@jwt_required()
@permission_required('admin.promocode.change')
def changestate(args):
    ...


@jwt_required()
@permission_required('admin.promocode.read')
@response(PromocodeSchema(many=True))
def get():
    promocodes = db.session.scalars(Promocode.select())
    return promocodes


@jwt_required()
def check():
    ...




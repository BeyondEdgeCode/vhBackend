import datetime
from typing import List
from flask import jsonify
from sqlalchemy import and_, func, select, text
from api.models import Category, PromoType, Promocode, PromocodeToProduct, Product, SubCategory, Basket
from apifairy import response, body
from .schema import PromoTypeSchema, PromocodeAssignSchema
from .schema import PromocodeSchema, PromocodeCheckSchema
from api.app import db
from flask_jwt_extended import jwt_required
from api.utils import permission_required
from flask_jwt_extended import current_user
from flask import current_app


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
        return jsonify(status=404, msg='Промокод не найден')

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


def check_validity(promocode):
    if not promocode:
        current_app.logger.info('Promocode not found')
        return jsonify(status=404, msg='Промокод не найден')

    if promocode.current_usages >= promocode.max_usages:
        current_app.logger.info('promocode.current_usages >= promocode.max_usages')
        return jsonify(status=404, msg='Промокод достиг максимума использований')

    if datetime.datetime.now() >= promocode.available_until:
        current_app.logger.info('promocode.available_until >= datetime.datetime.now()')
        return jsonify(status=404, msg='Срок действия промокода истек')


def find_intersection(promocode):
    user_basket: List[Basket] = db.session.scalars(
        Basket.select().where(
            Basket.user_fk == current_user.id
        )
    )

    basket_ids = {product.product_fk for product in user_basket}
    promocode_assigned_products = {promo_to_prod.product_id for promo_to_prod in promocode.to_products}

    intersection = basket_ids.intersection(promocode_assigned_products)

    # Удачи будущему мне разобраться с этим
    basket_intersection_sum = db.session.scalar(
        select(
            func.sum(Basket.amount * Product.price)
        )
        .select_from(Product)
        .join(Basket)
        .where(
            and_(
                Basket.user_fk == current_user.id,
                Product.id.in_(intersection)
            )
        )
    )
    return intersection, basket_intersection_sum, user_basket


def check_min_sum(intersection, basket_intersection_sum, promocode):
    if not intersection or basket_intersection_sum < promocode.min_sum:
        return jsonify(error=400,
                       msg=f'Не выполнено условие, минимальная сумма акционных товаров: {promocode.min_sum} руб.')
    else:
        return True


@jwt_required()
@body(PromocodeCheckSchema)
def check(args):
    promocode: Promocode = db.session.scalar(
        Promocode.select().where(
            Promocode.key == args['promocode']
        )
    )

    check_validity_res = check_validity(promocode)
    if check_validity_res:
        return check_validity_res

    intersection, basket_intersection_sum, _ = find_intersection(promocode)
    valid_promocode = check_min_sum(intersection, basket_intersection_sum, promocode)
    if valid_promocode != True:
        return valid_promocode

    return jsonify(promocode=args['promocode'],
                   intersection_sum=basket_intersection_sum,
                   intersection=list(intersection),
                   type=promocode.promotype.type,
                   value=promocode.value)

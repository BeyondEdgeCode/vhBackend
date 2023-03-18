import json
from typing import List

from flask import jsonify

from api.models import Basket, Product, ProductAvailability, Shop
from apifairy import body, response, arguments
from .schema import AddToBasketSchema, BasketSchema, BasketIdSchema, BasketWrapperSchema
from flask_cors import cross_origin
from api.app import db
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import and_, func
from api.schemas.response import ResponseSchema


@cross_origin()
@jwt_required()
@body(AddToBasketSchema)
def add(data: AddToBasketSchema):
    # Check, if product already in basket add +1 to amount
    existed_record: Basket = db.session.scalar(
        Basket.select().where(and_(
            Basket.user_fk == current_user.id,
            Basket.product_fk == data['product_id']
        )))

    max_amount: int = db.session.query(
        func.max(ProductAvailability.amount)
        ).where(
            ProductAvailability.product_id == data['product_id']
        ).scalar()

    if existed_record:
        if existed_record.amount + 1 > max_amount:
            return {'status': 400, 'error': 'Недостаточно товара в магазине'}
        else:
            existed_record.amount += 1
            db.session.add(existed_record)
            db.session.commit()
            return {'status': 200, 'message': 'Товар добавлен'}

    if max_amount == 0:
        return {'status': 400, 'error': 'Недостаточно товара в магазине'}

    db.session.add(
        Basket(user_fk=current_user.id, product_fk=data['product_id'], amount=1)
    )
    db.session.commit()
    return {'status': 200, 'message': 'Товар добавлен'}


@cross_origin()
@cross_origin()
@jwt_required()
@body(BasketIdSchema)
@response(ResponseSchema)
def decrement(data: BasketIdSchema):
    item: Basket = db.session.scalar(
        Basket.select()
        .where(
            and_(
                Basket.product_fk == data['id'],
                Basket.user_fk == current_user.id
            )
        )
    )

    if not item:
        return {'status': 404, 'error': 'Item not found'}

    if item.amount == 1:
        db.session.delete(item)
        db.session.commit()
        return {'status': 200, 'message': 'Готово'}

    item.amount -= 1
    db.session.add(item)
    db.session.commit()
    return {'status': 200, 'message': 'Готово'}


@cross_origin()
@jwt_required()
@body(BasketIdSchema)
@response(ResponseSchema)
def increment(data: BasketIdSchema):
    item: Basket = db.session.scalar(
        Basket.select()
        .where(
            and_(
                Basket.product_fk == data['id'],
                Basket.user_fk == current_user.id
            )
        )
    )
    if not item:
        return {'status': 404, 'error': 'Item not found'}

    max_amount: int = db.session.query(
        func.max(ProductAvailability.amount)
    ).where(
        ProductAvailability.product_id == item.product_fk
    ).scalar()

    if item.amount + 1 > max_amount:
        return {'status': 400, 'error': 'Недостаточно товара в магазине'}

    item.amount += 1
    db.session.add(item)
    db.session.commit()

    return {'status': 200, 'message': 'Готово'}


@jwt_required()
@response(BasketWrapperSchema)
def get():
    basket_items: List[Basket] = [*db.session.scalars(
        Basket.select()
        .where(
                Basket.user_fk == current_user.id
        )
    )]
    shops_list: List[Shop] = db.session.scalars(
        Shop.select()
    )
    not_available_info = []
    for shop in shops_list:
        data = {
                'shop_id': shop.id,
                'not_available': []
                }
        for item in basket_items:
            value: ProductAvailability = db.session.scalar(
                ProductAvailability.select().where(
                    ProductAvailability.product_id == item.product_fk
                )
            )
            if value.amount < item.amount:
                data['not_available'].append(item.product_fk)

        not_available_info.append(data)
    total = sum([item.product.price * item.amount for item in basket_items], 0.0)
    return {'products': basket_items, 'availability': not_available_info, 'total': total}


@jwt_required()
@arguments(BasketIdSchema)
@response(ResponseSchema)
def delete(data: BasketIdSchema):
    obj: Basket = db.session.scalar(
        Basket.select().where(
            and_(
                Basket.user_fk == current_user.id,
                Basket.product_fk == data['id']
            )
        )
    )

    db.session.delete(obj)
    db.session.commit()
    return {'status': 200, 'message': 'Deleted'}


from typing import List
from api.models import Basket, ProductAvailability, Shop
from apifairy import body, response, arguments
from .schema import AddToBasketSchema, BasketIdSchema, BasketWrapperSchema
from flask_cors import cross_origin
from api.app import db
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import and_, func
from api.schemas.response import ResponseSchema
from time import perf_counter_ns
from api.app import cache


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

@cache.cached(10)
@jwt_required()
@response(BasketWrapperSchema)
def get():
    start = perf_counter_ns()
    basket_items: List[Basket] = tuple([*db.session.scalars(
        Basket.select()
        .where(
                Basket.user_fk == current_user.id
        )
    )])

    shops_list: List[Shop] = tuple(db.session.scalars(
            Shop.select()
        ))

    def map_shops(shop: Shop):
        data = {
            'shop_id': shop.id,
            'not_available': []
        }

        def second_map(item: Basket):
            value: ProductAvailability = db.session.scalar(
                ProductAvailability.select().where(
                    and_(
                        ProductAvailability.product_id == item.product_fk,
                        ProductAvailability.shop_id == shop.id
                    )
                )
            )
            if value.amount < item.amount:
                return item.product_fk

        values = map(second_map, basket_items)
        data['not_available'] = [*filter(lambda x: x is not None, values)]
        return data

    not_available_info = [*map(map_shops, shops_list)]
    total = sum([item.product.price * item.amount for item in basket_items], 0.0)
    print((perf_counter_ns() - start)/1_000_000, 'ms')
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

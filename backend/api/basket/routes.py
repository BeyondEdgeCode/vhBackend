from api.models import Basket, Product, ProductAvailability, Shop
from apifairy import body, response
from .schema import AddToBasketSchema, BasketSchema, BasketIdSchema
from flask_cors import cross_origin
from api.app import db
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import and_
from api.schemas.response import ResponseSchema


@cross_origin()
@jwt_required()
@body(AddToBasketSchema)
@response(ResponseSchema)
def add(data: AddToBasketSchema):
    # Check, if product already in basket add +1 to amount
    if existed_record := db.session.scalar(
            Basket.select().where(and_(
                Basket.user_fk == current_user.id,
                Basket.product_fk == data['product_id'],
                Basket.shop_id == data['shop_id']
            ))):
        existed_record: Basket = existed_record
        available: ProductAvailability = db.session.scalar(ProductAvailability.select().where(
            and_(
                ProductAvailability.product_id == data['product_id'],
                ProductAvailability.shop_id == data['shop_id']

            )))
        if existed_record.amount + 1 > available.amount:
            return {'status': 400, 'error': 'Недостаточно товара в магазине'}
        else:
            existed_record.amount += 1
            db.session.add(existed_record)
            db.session.commit()
            return {'status': 200, 'message': 'Товар добавлен'}

    available: ProductAvailability = db.session.scalar(
        ProductAvailability.select().where(
            and_(
                ProductAvailability.product_id == data['product_id'],
                ProductAvailability.shop_id == data['shop_id']
            )
        ))

    if available.amount <= 0:
        return {'status': 400, 'error': 'Недостаточно товара в магазине'}

    db.session.add(
        Basket(user_fk=current_user.id, product_fk=data['product_id'], shop_id=data['shop_id'], amount=1)
    )
    db.session.commit()
    return {'status': 200, 'message': 'Товар добавлен'}


@cross_origin()
@jwt_required()
@body(BasketIdSchema)
@response(ResponseSchema)
def decrement(data: BasketIdSchema):
    item: Basket = db.session.scalar(
        Basket.select()
        .where(
            and_(
                Basket.id == data['id'],
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


@jwt_required()
@body(BasketIdSchema)
@response(ResponseSchema)
def increment(data: BasketIdSchema):
    item: Basket = db.session.scalar(
        Basket.select()
        .where(
            and_(
                Basket.id == data['id'],
                Basket.user_fk == current_user.id
            )
        )
    )
    if not item:
        return {'status': 404, 'error': 'Item not found'}

    product_available: ProductAvailability = db.session.get(ProductAvailability, item.product_fk)

    if item.amount + 1 > product_available.amount:
        return {'status': 400, 'error': 'Недостаточно товара в магазине'}

    item.amount += 1
    db.session.add(item)
    db.session.commit()

    return {'status': 200, 'message': 'Готово'}


@jwt_required()
@response(BasketSchema(many=True))
def get():
    return db.session.scalars(
        Basket.select()
        .where(
            and_(
                Basket.user_fk == current_user.id
            )
        )
    )
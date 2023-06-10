from datetime import datetime
from typing import List
from flask import jsonify, current_app, abort
from sqlalchemy import and_, desc
from sqlalchemy.engine import ScalarResult
from api.models import Order, OrderItem, OrderStatus, Basket, DeliveryType, PaymentType
from api.models import ProductAvailability, Promocode
from apifairy import body, response, arguments
from .schema import CreateOrderSchema, ShortOrderSchema, OrderSchema, OrderIdSchema, OrderLifecycleSchema, GetByAdminSchema
from flask_jwt_extended import jwt_required, current_user
from api.app import db
from api.promocode.routes import check_min_sum, check_validity, find_intersection
from ..utils import permission_required


def get_basket() -> List[Basket]:
    return db.session.scalars(
        Basket.select().where(
            Basket.user_fk == current_user.id
        )
    )


@jwt_required()
@permission_required('admin.order.lifecycle')
@body(OrderLifecycleSchema)
@response(OrderSchema)
def change_state(args):
    order: Order = db.session.get(Order, args['id'])

    if not order:
        return jsonify(status=404, msg='Заказ не найден'), 404

    order.status = args['next_state']
    db.session.add(order)
    db.session.commit()
    return order


@jwt_required()
@permission_required('admin.order.cancel')
@arguments(OrderIdSchema)
@response(OrderSchema)
def cancel_by_admin(args):
    order: Order = db.session.get(Order, args['id'])

    if not order:
        return jsonify(status=404, msg='Заказ не найден'), 404

    if order.status == OrderStatus.canceled_by_user or order.status == OrderStatus.canceled_by_system:
        return jsonify(status=400, msg='Заказ уже отменен.'), 400

    order.status = OrderStatus.canceled_by_system
    db.session.add(order)
    db.session.commit()

    return order


@jwt_required()
@arguments(OrderIdSchema)
def cancel_by_user(args):
    order: Order = db.session.get(Order, args['id'])
    if not order:
        return jsonify(status=404, msg='Заказ не найден'), 404

    if order.user_fk != current_user.id:
        return jsonify(status=403, msg='Нет доступа.'), 403

    if order.status == OrderStatus.canceled_by_user or order.status == OrderStatus.canceled_by_system:
        return jsonify(status=400, msg='Заказ уже отменен.'), 400

    if order.status == OrderStatus.finished:
        return jsonify(status=400, msg='Завершенный заказ нельзя отменить.'), 400

    order.status = OrderStatus.canceled_by_user
    db.session.add(order)
    db.session.commit()
    return jsonify(status=200, msg=f'Заказ №{order.id} отменен.')


@jwt_required()
@response(OrderSchema(many=True))
def get_by_user():
    orders: List[Order] = db.session.scalars(Order.select().where(
        Order.user_fk == current_user.id
    ).order_by(desc(Order.id)))
    return orders


@jwt_required()
@permission_required('admin.orders.read')
@arguments(GetByAdminSchema)
@response(ShortOrderSchema(many=True))
def get_by_admin(args):
    def get_lambda_1(arg):
        if arg:
            return lambda: Order.status.in_(['forming',
                                             'awaiting_payment',
                                             'in_delivery',
                                             'waiting_to_receive'])
        else:
            return lambda: Order.status.in_([e.name for e in OrderStatus])

    def get_lambda_2(arg):
        if arg:
            return lambda: Order.shop_fk == 1
        else:
            return lambda: Order.shop_fk != 0

    l1 = get_lambda_1(args['active_only'])
    l2 = get_lambda_2(args['current_shop_only'])

    orders: List[Order] = db.session.scalars(Order.select().where(
        and_(
            l1, l2
        )
    ).order_by(desc(Order.id)))

    return orders


@jwt_required()
@permission_required('admin.orders.read')
@arguments(OrderIdSchema)
@response(OrderSchema)
def get_one_by_admin(args):
    order = db.session.get(Order, args['id'])
    if not order:
        abort(404)
    return order


@jwt_required()
@body(CreateOrderSchema)
def create(payload):
    intersection = None
    promocode = None
    user_basket: List[Basket] = get_basket()

    if not user_basket:
        return jsonify(status=400, msg='Ошибка при создании заказа, корзина пуста.'), 400

    if payload['promocode']:
        promocode: Promocode = db.session.scalar(
            Promocode.select().where(
                Promocode.key == payload['promocode']
            )
        )
        check_validity_res = check_validity(promocode)
        if check_validity_res:
            return check_validity_res

        intersection, basket_intersection_sum, _ = find_intersection(promocode)
        valid_promocode = check_min_sum(intersection, basket_intersection_sum, promocode)
        current_app.logger.info(basket_intersection_sum)

        if valid_promocode != True:
            return valid_promocode

    order_items_list = []
    basket_sum = 0.0
    for basket_item in user_basket:
        availability: ProductAvailability = db.session.scalar(ProductAvailability.select().where(
            and_(
                ProductAvailability.product_id == basket_item.product_fk,
                ProductAvailability.shop_id == payload['shop_id']
            )
        ))
        if availability.amount < basket_item.amount:
            continue

        if promocode and basket_item.product_fk in intersection and promocode.promotype.type == 'percent':
            price = basket_item.product.price - basket_item.product.price / 100 * promocode.value
            item_sum = price * basket_item.amount
            basket_sum += item_sum
            order_items_list.append(
                OrderItem(product_fk=basket_item.product_fk,
                          price=price,
                          amount=basket_item.amount,
                          item_sum=item_sum)
            )
        else:
            basket_sum += basket_item.product.price * basket_item.amount
            current_app.logger.info(f'+= {basket_item.product.price * basket_item.amount}')
            current_app.logger.info(f'sum {basket_sum}')
            order_items_list.append(
                OrderItem(product_fk=basket_item.product_fk,
                          price=basket_item.product.price,
                          amount=basket_item.amount,
                          item_sum=basket_item.product.price * basket_item.amount)
            )

    if not order_items_list:
        return jsonify(status=400, msg='Ошибка при создании заказа, доступные товары не найдены.'), 400

    if promocode and promocode.promotype.type == 'fixed':
        basket_sum -= promocode.value

    user_basket: List[Basket] = [*get_basket()]  # ebaniy rot etogo casino, po drugomy ne rabotaet ;(

    for item in user_basket:
        product = item.product
        product_avaliability: ProductAvailability = db.session.scalar(ProductAvailability.select().where(
            and_(
                ProductAvailability.product_id == product.id,
                ProductAvailability.shop_id == payload['shop_id']
            )
        ))
        product_avaliability.amount -= item.amount
        db.session.add(product_avaliability)

        db.session.delete(item)

    new_order = Order(user_fk=current_user.id, status=OrderStatus.forming,
                      delivery_type=DeliveryType.pickup, payment_type=PaymentType.postpayment,
                      sum=basket_sum, used_promocode=promocode.id if promocode else None,
                      shop_fk=payload['shop_id'])

    db.session.add(new_order)
    db.session.commit()

    for item in order_items_list:
        item.order_fk = new_order.id

    db.session.add_all(order_items_list)
    db.session.commit()

    return jsonify(status=200, msg=f'Заказ № {new_order.id} создан')

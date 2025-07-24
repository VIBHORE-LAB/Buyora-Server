from flask import Blueprint
from app.controllers.order_controller import create_order, get_orders, get_order_by_id, cancel_order

order_bp = Blueprint('order', __name__, url_prefix='/api/orders')

@order_bp.route('/create' , methods=['POST'])
def handle_create_order():
    return create_order()


@order_bp.route('', methods = ['GET'])
def handle_get_orders():
    return get_orders()

@order_bp.route('/<int:order_id>', methods=['GET'])
def handle_get_order_by_id(order_id):
    return get_order_by_id(order_id)

@order_bp.route('/cancel/<int:order_id>', methods=['DELETE'])
def handle_cancel_order(order_id):
    return cancel_order(order_id)

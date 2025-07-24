from flask import Blueprint
from app.controllers.cart_controller import add_to_cart, get_cart, increase_quantity, decrease_quantity, remove_from_cart,clear_cart

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('/add', methods=['POST'])
def handle_add_to_cart():
    return add_to_cart()

@cart_bp.route('', methods=['GET'])
def handle_get_cart():
    return get_cart()

@cart_bp.route('/<int:product_id>/increase', methods=['PUT'])
def handle_increase_quantity(product_id):
    return increase_quantity(product_id)

@cart_bp.route('/<int:product_id>/decrease', methods=['PUT'])
def handle_decrease_quantity(product_id):
    return decrease_quantity(product_id)

@cart_bp.route('/<int:product_id>/remove', methods=['DELETE'])
def handle_remove_from_cart(product_id):
    return remove_from_cart(product_id)


@cart_bp.route('/clear', methods=['DELETE'])
def handle_clear_cart():
    return clear_cart()


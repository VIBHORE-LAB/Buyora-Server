from flask import Blueprint, request
from app.controllers.product_controller import create_product, get_products, get_product_by_id,update_product, delete_product, get_products_by_seller

product_bp = Blueprint('product', __name__, url_prefix='/api/products')  

@product_bp.route('/create', methods=['POST'])
def handle_create_product():
    return create_product()


@product_bp.route('/', methods=['GET'])
def handle_get_products():
    return get_products()

@product_bp.route('/<int:product_id>',methods=['GET'])
def handle_get_product_by_id(product_id):
    return get_product_by_id(product_id)


@product_bp.route('/update/<int:product_id>', methods=['PUT'])
def handle_update_product(product_id):
    return update_product(product_id)

@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def handle_delete_product(product_id):
    return delete_product(product_id)


@product_bp.route('/sellerProducts', methods=['GET'])
def handle_get_products_by_seller():
    return get_products_by_seller()

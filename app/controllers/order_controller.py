from flask import jsonify, current_app,request
from app.Models.order import Order, OrderItem
from app.Models import db
import jwt
from app.Models.user import User
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pytz


def check_auth():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid authorization header"}),401
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"error:" "Invalid token"}), 401
    
    if payload['role'] != 'Customer':
        return jsonify({"error": "Unauthorize access"}), 403
    user = User.query.get(payload['user_id'])
    return user

def create_order():
    user = check_auth()
    if not isinstance(user, User):
        return user

    data = request.get_json()
    items = data.get('items', [])
    address = data.get('address')

    # Calculate subtotal
    subtotal = 0
    from app.Models.product import Product
    for item in items:
        product = Product.query.get(item['product_id'])
        if product:
            subtotal += product.price * item.get('quantity', 1)

    total = subtotal  # Only product cost

    # Create order
    india = pytz.timezone("Asia/Kolkata")
    india_now = datetime.now(india)
    expected_delivery = india_now + timedelta(days=3)

    order = Order(
        user_id=user.id,
        status='pending',
        address=address,
        expected_delivery=expected_delivery
    )
    db.session.add(order)
    db.session.flush()

    # Add order items
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product:
            continue
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.get('quantity', 1),
            price=product.price * item.get('quantity', 1)
        )
        db.session.add(order_item)

    db.session.commit()

    # Return order info with total
    return jsonify({
        "order": order.to_dict(),
        "subtotal": subtotal,
        "total": total
    }), 201

def get_orders():
    try:
        user = check_auth()
        if not isinstance(user, User):
            return user
        orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
        # Each order will have its items grouped, with quantity per item
        return jsonify({
            "orders": [order.to_dict() for order in orders]
        }), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


def get_order_by_id(order_id):
    try:
        user = check_auth()
        if not isinstance(user, User):
            return user
        order = Order.query.filter_by(id = order_id, user_id = user.id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        return jsonify({"order": order.to_dict()}), 200
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    
def cancel_order(order_id):
    try:
        user = check_auth()
        if not isinstance(user, User):
            return user
        order = Order.query.filter_by(id = order_id, user_id = user.id).first()
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        if order.status != 'pending':
            return jsonify({"error": "Only pending orders can be cancelled"}), 400
        order.status = 'cancelled'
        db.session.commit()
        return jsonify({"message": "Order cancelled successfully"}), 200
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


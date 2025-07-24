from flask import jsonify, current_app, request
from app.Models.product import Product
from app.Models import db
from sqlalchemy import or_
from sqlalchemy import and_

from app.Models.order import OrderItem
import cloudinary.uploader
import jwt
from app.Models.user import User


def create_product():
    try:

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "MIssing or invalid authorization header"}), 401
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        if payload['role'] != 'Seller':
            return jsonify({"error": "Unauthorized access"}), 403

        seller = User.query.get(payload['user_id'])
        if not seller:
            return jsonify({"error": "Seller not found"}), 404
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_file = request.files.get('image')
        image_url = None
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result.get('secure_url')
        else:
            return jsonify({"error": "Image file is required"}), 400
        category = request.form.get('category')





        new_product = Product(
            name=name,
            description = description,
            price = price, 
            image_url = image_url,
            category = category,
            seller_id = seller.id

        )


        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_products():
    try:
        name = request.args.get('name')
        if name:
            products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
            if products:
                return jsonify([product.to_dict() for product in products]), 200
            else:
                return jsonify({"error": "No products found"}), 404
        else:

            products = Product.query.all()
            return jsonify([product.to_dict() for product in products]), 200
    
    except Exception as e:
        return jsonify({"error":str(e)}), 500

def get_product_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if product:
            return jsonify(product.to_dict()), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# def get_product_by_name(name):
#     try:
        
#         products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
#         if products:
#             return jsonify([product.to_dict() for product in products]), 200
#         else:
#             return jsonify({"error": "No products found"}), 404

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

    
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        
        name = request.form.get('name', product.name)
        description = request.form.get('description', product.description)
        price = request.form.get('price', product.price)

        image_file = request.files.get('image')
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            product.image_url = upload_result.get('secure_url')

        product.name = name
        product.description = description
        
        try:
            product.price = float(price)
        except Exception:
            product.price = product.price  
        
        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

 
def get_products_by_seller():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    if payload.get('role') != 'Seller':
        return jsonify({"error": "Unauthorized access"}), 403

    user = User.query.get(payload['user_id'])
    if not user:
        return jsonify({"error": "User not found"}), 404

    name = request.args.get('name')
    if name:
        products = Product.query.filter(
            and_(
                Product.seller_id == user.id,
                Product.name.ilike(f"%{name}%")
            )
        ).all()
    else:
        products = Product.query.filter_by(seller_id=user.id).all()

    if not products:
        return jsonify({"error": "No products found"}), 404

    return jsonify([product.to_dict() for product in products]), 200





  # import your OrderItem model

def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

       
        ordered_item = OrderItem.query.filter_by(product_id=product_id).first()
        if ordered_item:
            return jsonify({"error": "Cannot delete product as it has already been ordered."}), 400

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

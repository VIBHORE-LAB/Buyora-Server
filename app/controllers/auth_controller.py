from flask import jsonify,request,current_app
from app.Models.user import User
from app.Models import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

def register_user():
    try:
        # Debug: Print request data
        print("Request method:", request.method)
        print("Request headers:", dict(request.headers))
        print("Request content type:", request.content_type)
        
        # Get JSON data
        data = request.get_json()
        print("Received data:", data)
        
        # Check if data exists
        if not data:
            print("Error: No JSON data received")
            return jsonify({"error": "No data provided"}), 400
        
        # Extract fields with validation
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'Customer')
        
        print(f"Extracted fields - Username: {username}, Email: {email}, Role: {role}")
        
        # Validate required fields
        if not username:
            print("Error: Username is required")
            return jsonify({"error": "Username is required"}), 400
        
        if not email:
            print("Error: Email is required")
            return jsonify({"error": "Email is required"}), 400
        
        if not password:
            print("Error: Password is required")
            return jsonify({"error": "Password is required"}), 400
        
        # Validate field lengths and formats
        if len(username.strip()) < 3:
            return jsonify({"error": "Username must be at least 3 characters long"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        
        # Basic email validation
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Clean up data
        username = username.strip()
        email = email.strip().lower()
        
        print(f"Cleaned data - Username: {username}, Email: {email}")
        
        # Check for existing user
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                print(f"Error: Username '{username}' already exists")
                return jsonify({"error": "Username already exists"}), 400
            else:
                print(f"Error: Email '{email}' already exists")
                return jsonify({"error": "Email already exists"}), 400
        
        # Hash password
        hashed_password = generate_password_hash(password)
        print("Password hashed successfully")
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            role=role
        )
        
        print("User object created")
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        print(f"User '{username}' registered successfully")
        return jsonify({"message": "User registered successfully"}), 201
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # Rollback database session on error
        db.session.rollback()
        
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

def login_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash,password):
            return jsonify({"error":"Invalid username or password"}), 401
        
        else:
             token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        print(f"User '{username}' logged in successfully, token generated")
        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200

    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

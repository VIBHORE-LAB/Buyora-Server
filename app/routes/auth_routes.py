from flask import Blueprint, request
from app.controllers.auth_controller import (
    register_user,
    login_user
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def handle_register_user():
    return register_user()

@auth_bp.route('/login', methods=['POST'])
def handle_login_user():
    return login_user()

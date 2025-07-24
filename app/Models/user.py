from datetime import datetime
from . import db
from sqlalchemy import Enum


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique= True, nullable= False)
    email = db.Column(db.String(120), unique=True, nullable= False)
    password_hash = db.Column(db.String(256), nullable= False)
    create_at = db.Column(db.DateTime, default = datetime.utcnow)

    role = db.Column(
        Enum('Customer', 'Seller', name = 'user_roles'),
        nullable = True,
        default = 'Customer'
    )
    def __repr__(self):
        return f'<User {self.username}'

    

from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from flask_sqlalchemy import SQLAlchemy
from . import db
from datetime import datetime


class CategoryEnum(Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    home = "home"
    other = "other"



category_enum = PGEnum(CategoryEnum, name="categoryenum", create_type=False)  

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    category = db.Column(category_enum, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= True)
    seller = db.relationship('User', backref='products')
    def to_dict(self): 
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at,
            'image_url': self.image_url,
            'category': self.category.value ,
            'seller_id': self.seller_id,
            'seller_username': self.seller.username if self.seller else None
        }

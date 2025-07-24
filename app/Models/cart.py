from . import db
from app.Models.user import User

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True, nullable = False)
    user = db.relationship('User', backref='cart', uselist=False)

    
class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key = True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)  # <-- Add this

    quantity = db.Column(db.Integer, nullable = False, default = 1)

    cart = db.relationship('Cart', backref='items')
    product = db.relationship('Product', backref=db.backref('cart_items', passive_deletes=True))

    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'name': self.product.name if self.product else None,
            'price': self.product.price if self.product else None,
            'image_url': self.product.image_url if self.product else None,
            'description': self.product.description if self.product else None,
            'category': self.product.category.value if self.product and self.product.category else None,  # <-- fix here
            'seller_username': self.product.seller.username if self.product and self.product.seller else None,
        }
    
    
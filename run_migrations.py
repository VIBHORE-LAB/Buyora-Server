from flask import Flask
from flask_migrate import Migrate, upgrade
from app.Models import db
from app.config.config import Config

# 👇 Import your models
from app.Models.user import User
from app.Models.product import Product
from app.Models.cart import Cart, CartItem
from app.Models.order import Order

app = Flask(__name__)
app.config.from_object(Config)

# initialize extensions
db.init_app(app)
migrate = Migrate(app, db)  

with app.app_context():
    upgrade()
    print("✅ Migrations applied successfully.")

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
import redis
import cloudinary

from app.Models import db
from app.routes.main_routes import main_bp
from app.routes.product_routes import product_bp
from app.routes.auth_routes import auth_bp
from app.routes.cart_routes import cart_bp
from app.routes.order_routes import order_bp
from app.config.config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(
    app,
    origins=["http://localhost:5173", "https://buyora.netlify.app"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

db.init_app(app)
migrate = Migrate(app, db)

cloudinary.config(
    cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
    api_key=app.config['CLOUDINARY_API_KEY'],
    api_secret=app.config['CLOUDINARY_API_SECRET']
)

app.register_blueprint(main_bp)
app.register_blueprint(product_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)

if __name__ == "__main__":
    with app.app_context():
        upgrade() 
    app.run(debug=True)

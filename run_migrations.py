# run_migrations.py
from flask import Flask
from flask_migrate import upgrade
from app.Models import db
from app.config.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    upgrade()
    print("✅ Migrations applied successfully.")

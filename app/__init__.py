# app/__init__.py
from flask import Flask
from .models import db
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Tablas creadas exitosamente")

from app import routes
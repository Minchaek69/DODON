# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))                # 대표 이미지
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.Integer)                  # 카테고리 ID (e.g. 상의=1)
    
    product_code = db.Column(db.String(50))              # 상품번호
    material = db.Column(db.String(100))                 # 소재
    color_options = db.Column(db.Text)                   # 색상 리스트
    size_options = db.Column(db.Text)                    # 사이즈 리스트
    detail_images = db.Column(db.Text)                   # 상세 이미지 리스트
    size_image = db.Column(db.String(255))               # 사이즈 도식 이미지
    is_visible = db.Column(db.Boolean, default=True)     # 상품 노출 여부

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'paid', 'shipped', 'cancelled'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
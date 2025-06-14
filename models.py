# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(255), unique=True, nullable=False)
    password    = db.Column(db.String(255), nullable=False)
    is_admin    = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
class Product(db.Model):
    __tablename__ = 'products'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(255), nullable=False)
    product_code  = db.Column(db.String(50), nullable=False)
    description   = db.Column(db.Text)
    price         = db.Column(db.Numeric(10,2), nullable=False)
    material      = db.Column(db.String(100))
    image_url     = db.Column(db.String(255))
    detail_images = db.Column(db.Text)   # CSV
    size_image    = db.Column(db.String(255))
    category      = db.Column(db.Integer)
    is_visible    = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # 新增：variants 关系
    variants = db.relationship(
        "Variant",
        back_populates="product",
        cascade="all, delete-orphan"
    )

class Variant(db.Model):
    __tablename__ = 'variants'

    id         = db.Column(db.Integer, primary_key=True)
    color      = db.Column(db.String(50), nullable=False)
    size       = db.Column(db.String(50), nullable=False)
    stock      = db.Column(db.Integer, nullable=False)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete='CASCADE'),
        nullable=False
    )

    product = db.relationship("Product", back_populates="variants")

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id  = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    # store the chosen color & size so we know which Variant to decrement
    color       = db.Column(db.String(50), nullable=False)
    size        = db.Column(db.String(50), nullable=False)
    quantity    = db.Column(db.Integer, default=1)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status       = db.Column(db.Enum('pending','paid','shipped','cancelled'), default='pending')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

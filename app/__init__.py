# app/__init__.py

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from flask import Flask, session
from models import db
from app.routes.cart import cart_bp # Make sure this is imported

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app) # db.init_app(app) should be called before filters/context processors that might use it implicitly

    # --- THIS PART IS CRUCIAL ---
    # Define template filters and context processors *after* 'app' is created
    # and *before* registering blueprints, but within the create_app function.

    @app.template_filter('lower_color_name')
    def lower_color_name_filter(color_name):
        color_map = {
            '블랙': '#000000',      # Black
            '아이보리': '#FFFFF0',  # Ivory
            '그레이': '#808080',    # Gray
            '레몬 옐로우': '#FFF000', # Lemon Yellow
            '스카이 블루': '#87CEEB', # Sky Blue
            '레드': '#FF0000',      # Red
            '화이트': '#FFFFFF',    # White
            # Add more mappings based on your actual Korean color names from the database...
        }
        # Safely get the mapped color or process the original if not found
        return color_map.get(color_name.strip(), color_name.strip().lower().replace(' ', '-'))

    @app.context_processor
    def inject_cart_count():
        cart = session.get('cart', {})
        # 假设 session['cart'] 结构是 { key: { 'quantity': x, … }, … }
        count = sum(item.get('quantity', 0) for item in cart.values())
        return {'cart_count': count}

    # Import Blueprints
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp

    # Register Blueprints
    app.register_blueprint(main_bp, url_prefix='/', name='main')
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp, url_prefix="/cart", name="cart")

    return app
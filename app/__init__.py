from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from flask import Flask
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY
    
    db.init_app(app)
    
    @app.template_filter('lower_color_name')
    def lower_color_name_filter(color_name):
            color_map = {
            '블랙': '#000000',      # 黑色
            '아이보리': '#FFFFF0',  # 象牙色 (近似白色，但有细微差别)
            '그레이': '#808080',    # 灰色
            '레몬 옐로우': '#FFF000', # Lemon Yellow
            '스카이 블루': '#87CEEB', # Sky Blue
            '레드': '#FF0000',      # Red
            }

            return color_map.get(color_name.strip(), color_name.strip().lower().replace(' ', '-'))
        # Load configuration from a config file or environment variables
        
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(main_bp, url_prefix='/', name='main')
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp)
    
    return app

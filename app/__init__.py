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
            # 这是一个示例映射，你可以根据你的实际颜色名称和对应的CSS值进行扩展
            color_map = {
                'Lemon Yellow': '#FFF000', # 例如，将 'Lemon Yellow' 映射到具体颜色代码
                'Sky Blue': '#87CEEB',
                'Red': '#FF0000',
                'Black': '#000000',
                'White': '#FFFFFF',
                'Gray': '#808080',
                # ... 添加更多你数据库中可能存在的颜色名称到 CSS 颜色值的映射
            }
            # 如果有映射，使用映射值；否则，尝试将名称转换为小写并替换空格为横线
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

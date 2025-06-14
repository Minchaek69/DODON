# app/__init__.py

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from models import db  # 你的 SQLAlchemy() 实例

# 新增这一行
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY

    # 初始化 db 和 migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # --- 下面保留你已有的 filter/context_processor ---
    @app.template_filter('lower_color_name')
    def lower_color_name_filter(color_name):
        color_map = {
            '블랙': '#000000',
            '아이보리': '#FFFFF0',
            '그레이': '#808080',
            '레몬 옐로우': '#FFF000',
            '스카이 블루': '#87CEEB',
            '레드': '#FF0000',
            '화이트': '#FFFFFF',
        }
        return color_map.get(color_name.strip(),
                             color_name.strip().lower().replace(' ', '-'))

    @app.context_processor
    def inject_cart_count():
        cart = session.get('cart', {})
        count = sum(item.get('quantity', 0) for item in cart.values())
        return {'cart_count': count}

    from app.routes.main     import main_bp
    from app.routes.products import products_bp
    from app.routes.auth     import auth_bp
    from app.routes.admin    import admin_bp
    from app.routes.cart     import cart_bp

    app.register_blueprint(main_bp,     url_prefix='/',         name='main')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(auth_bp,     url_prefix='/auth')
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp,     url_prefix='/cart',     name='cart')

    return app


# 如果你喜欢直接 python app/__init__.py 启动，可以加上：
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

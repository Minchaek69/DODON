from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from flask import Flask
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY
    
    db.init_app(app)

    # Load configuration from a config file or environment variables
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(main_bp, url_prefix='/', name='main')
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

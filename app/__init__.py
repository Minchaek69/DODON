from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "your-secret-key"  # Login session secret key

    # Load configuration from a config file or environment variables
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

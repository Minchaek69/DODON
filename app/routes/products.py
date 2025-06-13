from flask import Blueprint, render_template
from models import Product

products_bp = Blueprint('products_bp', __name__, url_prefix='/products')

@products_bp.route('/', endpoint='index')
def show_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

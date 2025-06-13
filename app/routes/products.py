from flask import Blueprint, render_template
from models import Product

products_bp = Blueprint('products_bp', __name__, url_prefix='/products')

@products_bp.route('/', endpoint='index')
def show_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/products_detail.html', product=product)

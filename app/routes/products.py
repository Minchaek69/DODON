from flask import Blueprint, render_template
from models import Product, Variant

products_bp = Blueprint('products_bp', __name__, url_prefix='/products')

@products_bp.route('/', endpoint='index')
def show_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)

    # 只保留有库存的 variants
    variants = Variant.query.\
        filter_by(product_id=product.id).\
        filter(Variant.stock>0).all()

    # 从 variants 提取唯一的颜色、尺寸
    colors = sorted({v.color for v in variants})
    sizes  = sorted({v.size  for v in variants})

    # 一并传给模板
    return render_template(
      'products/products_detail.html',
      product=product,
      variants=variants,
      colors=colors,
      sizes=sizes,
    )

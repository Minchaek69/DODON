from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os, datetime
from models import Product
from app import db
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_email') or not session.get('is_admin'):
            flash('Admin access required.')
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/products')
@admin_required
def admin_products():
    products = Product.query.all()
    return render_template('admin/product_list.html', products=products)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('admin_bp.admin_products'))

@admin_bp.route('/products/new', methods=['GET', 'POST'])
@admin_required
def new_product():
    if request.method == 'POST':
        name = request.form.get('name')
        product_code = request.form.get('product_code')
        price = request.form.get('price')
        stock = request.form.get('stock')
        material = request.form.get('material')
        category = int(request.form.get('category'))
        color_options = request.form.get('color_options')
        size_options = request.form.get('size_options')
        description = request.form.get('description')
        is_visible = bool(request.form.get('is_visible', True))
 # 대표 이미지
        main_image_file = request.files.get('main_image')
        main_image_filename = None
        if main_image_file and allowed_file(main_image_file.filename):
            main_image_filename = secure_filename(main_image_file.filename)
            main_image_path = os.path.join(UPLOAD_FOLDER, main_image_filename)
            main_image_file.save(main_image_path)

        # 상세 이미지 (여러 장)
        detail_files = request.files.getlist('detail_images')
        detail_filenames = []
        for file in detail_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                detail_filenames.append(filename)

        # 사이즈 이미지
        size_image_file = request.files.get('size_image')
        size_image_filename = None
        if size_image_file and allowed_file(size_image_file.filename):
            size_image_filename = secure_filename(size_image_file.filename)
            size_image_file.save(os.path.join(UPLOAD_FOLDER, size_image_filename))

        # DB 저장
        product = Product(
            name=name,
            product_code=product_code,
            price=price,
            stock=stock,
            material=material,
            category=category,
            color_options=color_options,
            size_options=size_options,
            description=description,
            image_url=main_image_filename,
            detail_images=','.join(detail_filenames),
            size_image=size_image_filename,
            is_visible=is_visible,
            created_at=datetime.datetime.utcnow()
        )

        db.session.add(product)
        db.session.commit()
        flash('상품이 성공적으로 업로드되었습니다.', 'success')
        return redirect(url_for('admin_bp.admin_products'))

    return render_template('admin/new_product.html')

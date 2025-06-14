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
@admin_bp.route('/products/new', methods=['GET','POST'])
@admin_required
def new_product():
    if request.method == 'POST':
        # --- 1) 基本字段 ---
        name         = request.form['name']
        code         = request.form['product_code']
        price        = request.form['price']
        material     = request.form['material']
        category     = int(request.form['category'])
        description  = request.form.get('description','')

        # --- 2) 处理图片 ---
        # （跟你之前一样，保存 main_image、detail_images、size_image 并获得各自的文件名）
        main_img_file = request.files['main_image']
        main_fname    = secure_filename(main_img_file.filename)
        main_img_file.save(os.path.join(UPLOAD_FOLDER, main_fname))

        detail_files  = request.files.getlist('detail_images')
        detail_fnames = []
        for f in detail_files:
            fn = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, fn))
            detail_fnames.append(fn)

        size_img_file = request.files.get('size_image')
        size_fname    = None
        if size_img_file:
            size_fname = secure_filename(size_img_file.filename)
            size_img_file.save(os.path.join(UPLOAD_FOLDER, size_fname))

        # --- 3) 写 Product （先不设 stock）---
        product = Product(
            name          = name,
            product_code  = code,
            price         = price,
            material      = material,
            category      = category,
            description   = description,
            image_url     = main_fname,
            detail_images = ",".join(detail_fnames),
            size_image    = size_fname,
            is_visible    = True
        )
        db.session.add(product)
        db.session.flush()  # 拿到 product.id

        # --- 4) 写 Variants ---
        colors = request.form.getlist('variant_color[]')
        sizes  = request.form.getlist('variant_size[]')
        stocks = request.form.getlist('variant_stock[]')

        for c, s, st in zip(colors, sizes, stocks):
            v = Variant(
                product_id = product.id,
                color      = c.strip(),
                size       = s.strip(),
                stock      = int(st)
            )
            db.session.add(v)

        db.session.commit()
        flash('상품이 성공적으로 업로드되었습니다.', 'success')
        return redirect(url_for('admin_bp.admin_products'))

    return render_template('admin/new_product.html')
# app/routes/cart.py

from flask import Blueprint, session, request, jsonify, render_template, flash
from models import Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    if not data:
        data = request.form

    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 1))
    color = data.get('color')
    size = data.get('size')

    if quantity <= 0:
        flash('Quantity must be 1 or more.', 'error')
        return jsonify({'success': False, 'message': 'Quantity must be 1 or more.'}), 400

    product = Product.query.get(product_id)
    if not product:
        flash('Product not found.', 'error')
        return jsonify({'success': False, 'message': 'Product not found.'}), 404

    if product.stock < quantity:
        flash('Not enough stock.', 'error')
        return jsonify({'success': False, 'message': 'Not enough stock.'}), 400
    
    item_key = f"{product_id}-{color if color else 'no_color'}-{size if size else 'no_size'}"

    cart = session.get('cart', {})
    if item_key in cart:
        if cart[item_key]['quantity'] + quantity > product.stock:
            flash('Requested quantity exceeds available stock.', 'error')
            return jsonify({'success': False, 'message': 'Requested quantity exceeds available stock.'}), 400
        cart[item_key]['quantity'] += quantity
    else:
        cart[item_key] = {
            'product_id': product_id,
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'color': color,
            'size': size,
            'image_url': product.image_url
        }

    session['cart'] = cart
    session.modified = True

    flash('Product successfully added to cart!', 'success')
    return jsonify({'success': True, 'message': 'Product successfully added to cart!'})

@cart_bp.route('/')
def view_cart():
    cart = session.get('cart', {})
    for item in cart.values():
        item['total_display'] = '{:,.0f}'.format(float(item['price']) * item['quantity'])
    # Calculate total price
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render_template('cart/cart.html', cart=cart, total_price=total_price)

@cart_bp.route('/update', methods=['POST'])
def update_cart_item():
    data = request.get_json()
    item_key = data.get('item_key')
    new_quantity = int(data.get('quantity'))

    cart = session.get('cart', {})

    if item_key not in cart:
        flash('Cart item not found.', 'error')
        return jsonify({'success': False, 'message': 'Cart item not found.'}), 404

    product_id = cart[item_key]['product_id']
    product = Product.query.get(product_id)

    if not product:
        flash('Product not found in database.', 'error')
        return jsonify({'success': False, 'message': 'Product not found.'}), 404

    if new_quantity > product.stock:
        flash('Requested quantity exceeds available stock.', 'error')
        return jsonify({'success': False, 'message': 'Requested quantity exceeds available stock.'}), 400

    if new_quantity <= 0:
        del cart[item_key]
        flash('Product removed from cart.', 'info')
    else:
        cart[item_key]['quantity'] = new_quantity
        flash('Cart quantity updated.', 'success')

    session['cart'] = cart
    session.modified = True
    return jsonify({'success': True, 'message': 'Cart updated successfully.'})

@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    item_key = data.get('item_key')

    cart = session.get('cart', {})
    if item_key in cart:
        del cart[item_key]
        session['cart'] = cart
        session.modified = True
        flash('Product removed from cart.', 'info') # Info message
        return jsonify({'success': True, 'message': 'Product removed from cart.'})
    flash('Cart item not found.', 'error') # Error message
    return jsonify({'success': False, 'message': 'Cart item not found.'}), 404
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, Sale
from app.employee.forms import SaleForm
from app.employee import bp

@bp.before_request
def employee_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    # Employee's recent sales
    recent_sales = Sale.query.filter_by(employee_id=current_user.id).order_by(Sale.timestamp.desc()).limit(10).all()
    
    # Total sales for employee
    total_sales = db.session.query(db.func.sum(Sale.total_amount)).filter_by(employee_id=current_user.id).scalar() or 0
    
    # Number of sales
    sales_count = Sale.query.filter_by(employee_id=current_user.id).count()
    
    # Available products
    available_products = Product.query.filter(Product.quantity_in_stock > 0).count()
    
    return render_template('employee/dashboard.html',
                         recent_sales=recent_sales,
                         total_sales=total_sales,
                         sales_count=sales_count,
                         available_products=available_products)

@bp.route('/products')
@login_required
def products():
    products = Product.query.filter(Product.quantity_in_stock > 0).all()
    return render_template('employee/products.html', products=products)

@bp.route('/add_sale', methods=['GET', 'POST'])
@login_required
def add_sale():
    form = SaleForm()
    form.product_id.choices = [(p.id, f"{p.name} ({p.sku}) - Stock: {p.quantity_in_stock}") 
                             for p in Product.query.filter(Product.quantity_in_stock > 0).all()]
    
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        if product and product.quantity_in_stock >= form.quantity.data:
            # Create sale
            sale = Sale(
                product_id=product.id,
                quantity_sold=form.quantity.data,
                price_per_unit=product.selling_price,
                employee_id=current_user.id
            )
            db.session.add(sale)
            
            # Update product quantity
            product.quantity_in_stock -= form.quantity.data
            db.session.commit()
            
            flash(f'Sale recorded successfully! Sold {form.quantity.data} units of {product.name}.', 'success')
            return redirect(url_for('employee.dashboard'))
        else:
            flash('Insufficient stock available!', 'danger')
    
    return render_template('employee/add_sale.html', form=form)

@bp.route('/sales')
@login_required
def sales():
    sales = Sale.query.filter_by(employee_id=current_user.id).order_by(Sale.timestamp.desc()).all()
    return render_template('employee/sales.html', sales=sales)
@bp.route('/search_products')
@login_required
def search_products():
    query = request.args.get('query', '').strip()
    
    if not query:
        return redirect(url_for('employee.products'))
    
    # Search for products by name or SKU (only in-stock products)
    products = Product.query.filter(
        db.and_(
            db.or_(
                Product.name.contains(query),
                Product.sku.contains(query)
            ),
            Product.quantity_in_stock > 0
        )
    ).all()
    
    return render_template('employee/search_results.html', 
                         products=products, 
                         query=query,
                         search_type='employee')
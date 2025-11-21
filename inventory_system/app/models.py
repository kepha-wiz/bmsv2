from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default='employee')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
#
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
#
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
#
    def is_admin(self):
        return self.role == 'admin'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    quantity_in_stock = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=10)  # Default threshold
    category = db.Column(db.String(50), default='General')
    description = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    stock_additions = db.relationship('StockAddition', backref='product', lazy=True)
    sales = db.relationship('Sale', backref='product', lazy=True)
    
    @property
    def total_value(self):
        return self.quantity_in_stock * self.cost_price
    
    @property
    def potential_revenue(self):
        return self.quantity_in_stock * self.selling_price
    
    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.low_stock_threshold
class StockAddition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity_added = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # New fields for price tracking
    old_cost_price = db.Column(db.Float, nullable=True)
    old_selling_price = db.Column(db.Float, nullable=True)
    new_cost_price = db.Column(db.Float, nullable=True)
    new_selling_price = db.Column(db.Float, nullable=True)
    price_change_reason = db.Column(db.String(200), nullable=True)
    
    user = db.relationship('User', backref='stock_additions')
    
    @property
    def cost_price_changed(self):
        return self.old_cost_price is not None and self.new_cost_price is not None and self.old_cost_price != self.new_cost_price
    
    @property
    def selling_price_changed(self):
        return self.old_selling_price is not None and self.new_selling_price is not None and self.old_selling_price != self.new_selling_price
    
    @property
    def any_price_changed(self):
        return self.cost_price_changed or self.selling_price_changed
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
    employee = db.relationship('User', backref='sales')
#
    def __init__(self, **kwargs):
        super(Sale, self).__init__(**kwargs)
        if self.quantity_sold and self.price_per_unit:
            self.total_amount = self.quantity_sold * self.price_per_unit
from flask_login import AnonymousUserMixin, UserMixin

class Anonymous(AnonymousUserMixin):
    def is_admin(self):
        return False

# Register as default anonymous user
from app import login_manager
login_manager.anonymous_user = Anonymous

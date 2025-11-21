from app import create_app, db
from app.models import User, Product, StockAddition, Sale
import os

app = create_app()

with app.app_context():
    # Ensure instance directory exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Create all database tables including new columns
    db.create_all()
    
    # Create default admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Database initialized with default users")
    
    # Create sample products with new fields
    if Product.query.count() == 0:
        sample_products = [
            Product(
                name="Laptop Computer",
                sku="LAPTOP001",
                cost_price=800.00,
                selling_price=1200.00,
                quantity_in_stock=15,
                category="Electronics",
                description="High-performance laptop with 16GB RAM and 512GB SSD",
                low_stock_threshold=5
            ),
            Product(
                name="Wireless Mouse",
                sku="MOUSE001",
                cost_price=15.00,
                selling_price=25.00,
                quantity_in_stock=50,
                category="Electronics",
                description="Ergonomic wireless mouse with 2.4GHz sensor",
                low_stock_threshold=10
            ),
            Product(
                name="Office Chair",
                sku="CHAIR001",
                cost_price=120.00,
                selling_price=199.99,
                quantity_in_stock=25,
                category="Office Supplies",
                description="Comfortable office chair with lumbar support",
                low_stock_threshold=5
            )
        ]
        
        for product in sample_products:
            db.session.add(product)
        
        db.session.commit()
        print("Sample products created")
    
    app.run(debug=True)
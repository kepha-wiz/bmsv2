from app import create_app, db
from app.models import User, Product, StockAddition, Sale
import os

def init_database():
    app = create_app()
    
    with app.app_context():
        # Ensure the instance directory exists
        os.makedirs(app.instance_path, exist_ok=True)
        
        # Create all database tables
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create a default employee user for testing
            employee = User(username='employee', email='employee@example.com', role='employee')
            employee.set_password('emp123')
            db.session.add(employee)
            
            # Create some sample products
            products = [
                Product(
                    name="Laptop Computer",
                    sku="LAPTOP001",
                    cost_price=800.00,
                    selling_price=1200.00,
                    quantity_in_stock=15
                ),
                Product(
                    name="Wireless Mouse",
                    sku="MOUSE001",
                    cost_price=15.00,
                    selling_price=25.00,
                    quantity_in_stock=50
                ),
                Product(
                    name="USB Keyboard",
                    sku="KEYBOARD001",
                    cost_price=25.00,
                    selling_price=40.00,
                    quantity_in_stock=30
                )
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print("Database initialized with default users and sample products")
        else:
            print("Database already initialized")

if __name__ == '__main__':
    init_database()
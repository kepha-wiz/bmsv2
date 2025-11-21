# Create a file called create_employee_users.py

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Create default employee users if they don't exist
    employees = [
        {
            'username': 'employee',
            'email': 'employee@example.com',
            'password': 'emp123',
            'role': 'employee'
        },
        {
            'username': 'sales1',
            'email': 'sales1@example.com',
            'password': 'sales123',
            'role': 'employee'
        },
        {
            'username': 'cashier1',
            'email': 'cashier1@example.com',
            'password': 'cash123',
            'role': 'employee'
        }
    ]
    
    for emp_data in employees:
        # Check if user already exists
        existing_user = User.query.filter_by(username=emp_data['username']).first()
        if not existing_user:
            # Create new user
            new_user = User(
                username=emp_data['username'],
                email=emp_data['email'],
                role=emp_data['role']
            )
            new_user.set_password(emp_data['password'])
            db.session.add(new_user)
            print(f"Created employee user: {emp_data['username']}")
        else:
            print(f"Employee user already exists: {emp_data['username']}")
    
    # Commit all changes
    db.session.commit()
    print("Employee user creation completed!")
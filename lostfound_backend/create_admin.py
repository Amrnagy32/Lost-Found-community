from app import create_app
from database import db
from models import User

app = create_app()

with app.app_context():
    # 1. Check if admin exists
    admin = User.query.filter_by(username="admin").first()
    
    if admin:
        # If exists, reset password
        print("Admin user already exists. Resetting password...")
        admin.set_password("admin123")
        admin.is_admin = True
    else:
        # If not, create new
        print("Creating new Admin user...")
        admin = User(username="admin", email="admin@test.com", is_verified=True, is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)

    db.session.commit()
    print("\nSUCCESS! Login details:")
    print("Username: admin")
    print("Password: admin123")
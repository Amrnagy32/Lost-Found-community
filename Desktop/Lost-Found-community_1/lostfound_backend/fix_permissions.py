from app import create_app
from database import db
from models import User

app = create_app()

with app.app_context():
    print("--- Fixing Permissions ---")
    
    # 1. Fix the Admin
    admin = User.query.filter_by(username="admin").first()
    if admin:
        admin.is_admin = True
        print("✓ User 'admin' set to SUPER ADMIN.")
    else:
        print("x User 'admin' not found.")

    # 2. Fix your Regular User (Change 'amrnagy' to your username if different)
    username_to_fix = "amrnagy"
    user = User.query.filter_by(username=username_to_fix).first()
    if user:
        user.is_admin = False
        print(f"✓ User '{username_to_fix}' set to REGULAR USER.")
    else:
        print(f"x User '{username_to_fix}' not found.")

    db.session.commit()
    print("--- Done! ---")
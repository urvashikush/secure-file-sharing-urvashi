from app import create_app, db, bcrypt
from app.models.user import User, UserRole
import os

def init_db():
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        # Check if ops user already exists
        ops_user = User.query.filter_by(email='ops@example.com').first()
        if not ops_user:
            # Create an operations user
            hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
            ops_user = User(
                email='ops@example.com',
                password=hashed_password,
                role=UserRole.OPS.value,
                is_verified=True
            )
            db.session.add(ops_user)
            db.session.commit()
            print("Operations user created successfully.")
        else:
            print("Operations user already exists.")
        
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(app.root_path, 'static/uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        print(f"Uploads directory created at {uploads_dir}")

if __name__ == '__main__':
    init_db() 
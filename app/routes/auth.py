from flask import Blueprint, request, jsonify, current_app
from app import db, bcrypt
from app.models.user import User, UserRole
from app.utils.email import send_verification_email
from app.utils.security import generate_verification_token
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400
    
    # Only client users can sign up through API
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    verification_token = generate_verification_token()
    
    new_user = User(
        email=data['email'],
        password=hashed_password,
        role=UserRole.CLIENT.value,
        verification_token=verification_token,
        is_verified=False
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Send verification email
    send_verification_email(new_user, verification_token)
    
    return jsonify({
        'message': 'User registered successfully. Please verify your email.',
        'user_id': new_user.id
    }), 201

@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()
    
    if not user:
        return jsonify({'message': 'Invalid verification token'}), 400
    
    user.is_verified = True
    user.verification_token = None
    db.session.commit()
    
    return jsonify({'message': 'Email verified successfully'}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    if user.role == UserRole.CLIENT.value and not user.is_verified:
        return jsonify({'message': 'Please verify your email before logging in'}), 401
    
    access_token = create_access_token(identity={
        'user_id': user.id,
        'role': user.role
    })
    
    return jsonify({
        'message': 'Login successful',
        'token': access_token,
        'role': user.role
    }), 200

@auth_bp.route('/create-ops-user', methods=['POST'])
def create_ops_user():
    data = request.json
    
    if not data or not data.get('email') or not data.get('password') or not data.get('admin_key'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Simple admin key check - in production, use a more secure approach
    if data['admin_key'] != current_app.config['SECRET_KEY']:
        return jsonify({'message': 'Unauthorized'}), 401
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        email=data['email'],
        password=hashed_password,
        role=UserRole.OPS.value,
        is_verified=True  # Ops users are verified by default
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'message': 'Operations user created successfully',
        'user_id': new_user.id
    }), 201 
import pytest
import json
from app import create_app, db
from app.models.user import User, UserRole

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test_secret_key',
        'SECRET_KEY': 'test_secret_key',
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_signup(client):
    response = client.post('/signup', 
                          json={
                              'email': 'test@example.com',
                              'password': 'password123'
                          })
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert 'User registered successfully' in data['message']
    assert 'user_id' in data
    
    with create_app().app_context():
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.role == UserRole.CLIENT.value
        assert user.is_verified is False

def test_login_unverified(client):
    client.post('/signup', 
               json={
                   'email': 'test@example.com',
                   'password': 'password123'
               })
    
    response = client.post('/login',
                          json={
                              'email': 'test@example.com',
                              'password': 'password123'
                          })
    data = json.loads(response.data)
    
    assert response.status_code == 401
    assert 'verify your email' in data['message']

def test_create_ops_user(client):
    response = client.post('/create-ops-user',
                          json={
                              'email': 'ops@example.com',
                              'password': 'password123',
                              'admin_key': 'test_secret_key'
                          })
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert 'Operations user created successfully' in data['message']
    
    with create_app().app_context():
        user = User.query.filter_by(email='ops@example.com').first()
        assert user is not None
        assert user.role == UserRole.OPS.value
        assert user.is_verified is True 
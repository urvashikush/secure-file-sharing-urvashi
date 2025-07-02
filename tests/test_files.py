import pytest
import json
import os
import io
from app import create_app, db, bcrypt
from app.models.user import User, UserRole
from app.models.file import File
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test_secret_key',
        'SECRET_KEY': 'test_secret_key',
        'UPLOAD_FOLDER': 'tests/uploads'
    })
    
    # Create test upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.app_context():
        db.create_all()
        
        # Create test users
        ops_user = User(
            email='ops@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8'),
            role=UserRole.OPS.value,
            is_verified=True
        )
        
        client_user = User(
            email='client@example.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8'),
            role=UserRole.CLIENT.value,
            is_verified=True
        )
        
        db.session.add(ops_user)
        db.session.add(client_user)
        db.session.commit()
        
        yield app
        
        # Clean up uploaded files
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
            
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def ops_token(app):
    with app.app_context():
        ops_user = User.query.filter_by(email='ops@example.com').first()
        return create_access_token(identity={
            'user_id': ops_user.id,
            'role': ops_user.role
        })

@pytest.fixture
def client_token(app):
    with app.app_context():
        client_user = User.query.filter_by(email='client@example.com').first()
        return create_access_token(identity={
            'user_id': client_user.id,
            'role': client_user.role
        })

def test_upload_file(client, ops_token):
    data = {}
    data['file'] = (io.BytesIO(b"test file content"), 'test.docx')
    
    response = client.post(
        '/upload-file',
        data=data,
        content_type='multipart/form-data',
        headers={'Authorization': f'Bearer {ops_token}'}
    )
    
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'File uploaded successfully'

def test_client_cannot_upload(client, client_token):
    data = {}
    data['file'] = (io.BytesIO(b"test file content"), 'test.docx')
    
    response = client.post(
        '/upload-file',
        data=data,
        content_type='multipart/form-data',
        headers={'Authorization': f'Bearer {client_token}'}
    )
    
    assert response.status_code == 403

def test_list_files(client, client_token, app, ops_token):
    # First upload a file as ops user
    data = {}
    data['file'] = (io.BytesIO(b"test file content"), 'test.docx')
    
    client.post(
        '/upload-file',
        data=data,
        content_type='multipart/form-data',
        headers={'Authorization': f'Bearer {ops_token}'}
    )
    
    # Then list files as client user
    response = client.get(
        '/list-files',
        headers={'Authorization': f'Bearer {client_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['files']) == 1
    assert data['files'][0]['filename'] == 'test.docx'

def test_get_download_link(client, client_token, app, ops_token):
    # First upload a file as ops user
    data = {}
    data['file'] = (io.BytesIO(b"test file content"), 'test.docx')
    
    upload_response = client.post(
        '/upload-file',
        data=data,
        content_type='multipart/form-data',
        headers={'Authorization': f'Bearer {ops_token}'}
    )
    
    file_id = json.loads(upload_response.data)['file_id']
    
    # Then get download link as client user
    response = client.get(
        f'/download-file/{file_id}',
        headers={'Authorization': f'Bearer {client_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'success'
    assert 'download-link' in data 
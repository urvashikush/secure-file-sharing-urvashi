import os
import secrets
import uuid
from cryptography.fernet import Fernet
from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_verification_token():
    return secrets.token_urlsafe(32)

def generate_secure_filename(filename):
    secure_name = secure_filename(filename)
    unique_id = str(uuid.uuid4())
    ext = secure_name.rsplit('.', 1)[1].lower() if '.' in secure_name else ''
    return f"{unique_id}.{ext}" if ext else unique_id

def encrypt_url(file_id, user_id):
    key = current_app.config['SECRET_KEY'].encode()
    # Pad the key to be 32 bytes for Fernet
    key = key.ljust(32)[:32]
    
    cipher = Fernet(Fernet.generate_key())
    data = f"{file_id}:{user_id}".encode()
    encrypted_data = cipher.encrypt(data)
    
    # Return the key and encrypted data as a token
    return f"{encrypted_data.decode()}"

def decrypt_url(token):
    try:
        key = current_app.config['SECRET_KEY'].encode()
        # Pad the key to be 32 bytes for Fernet
        key = key.ljust(32)[:32]
        
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(token.encode()).decode()
        file_id, user_id = decrypted_data.split(':')
        
        return int(file_id), int(user_id)
    except Exception:
        return None, None 
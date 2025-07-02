from app import db
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    OPS = 'ops'
    CLIENT = 'client'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    files = db.relationship('File', backref='uploader', lazy=True)
    
    def __repr__(self):
        return f"User('{self.email}', '{self.role}')" 
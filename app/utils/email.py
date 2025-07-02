from flask_mail import Message
from app import mail
from flask import current_app, url_for
import os

def send_verification_email(user, token):
    base_url = os.environ.get('BASE_URL', 'http://localhost:5000')
    verification_url = f"{base_url}/verify-email/{token}"
    
    msg = Message(
        'Verify Your Email',
        recipients=[user.email]
    )
    
    msg.body = f'''To verify your email, visit the following link:
{verification_url}

If you did not make this request, please ignore this email.
'''
    
    mail.send(msg)
    return True 
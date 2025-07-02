from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Welcome to the Secure File Sharing API',
        'endpoints': {
            'auth': [
                {'path': '/signup', 'method': 'POST', 'description': 'Register a new client user'},
                {'path': '/verify-email/<token>', 'method': 'GET', 'description': 'Verify email address'},
                {'path': '/login', 'method': 'POST', 'description': 'Login for both client and operations users'},
                {'path': '/create-ops-user', 'method': 'POST', 'description': 'Create an operations user (requires admin key)'}
            ],
            'files': [
                {'path': '/upload-file', 'method': 'POST', 'description': 'Upload a file (Operations users only)'},
                {'path': '/list-files', 'method': 'GET', 'description': 'List all uploaded files (Client users only)'},
                {'path': '/download-file/<file_id>', 'method': 'GET', 'description': 'Get a secure download link (Client users only)'},
                {'path': '/download-file/<token>', 'method': 'GET', 'description': 'Download a file using a secure token'}
            ]
        }
    }) 
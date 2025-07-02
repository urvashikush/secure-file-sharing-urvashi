import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app import db
from app.models.file import File
from app.models.user import User, UserRole
from app.utils.security import allowed_file, generate_secure_filename, encrypt_url, decrypt_url
from flask_jwt_extended import jwt_required, get_jwt_identity

files_bp = Blueprint('files', __name__)

@files_bp.route('/upload-file', methods=['POST'])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()
    
    if current_user.get('role') != UserRole.OPS.value:
        return jsonify({'message': 'Only operations users can upload files'}), 403
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'message': 'File type not allowed. Only pptx, docx, and xlsx are permitted'}), 400
    
    filename = generate_secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file.save(file_path)
    
    file_type = file.filename.rsplit('.', 1)[1].lower()
    
    new_file = File(
        filename=filename,
        original_filename=file.filename,
        file_type=file_type,
        file_path=file_path,
        user_id=current_user.get('user_id')
    )
    
    db.session.add(new_file)
    db.session.commit()
    
    return jsonify({
        'message': 'File uploaded successfully',
        'file_id': new_file.id,
        'filename': new_file.original_filename
    }), 201

@files_bp.route('/list-files', methods=['GET'])
@jwt_required()
def list_files():
    current_user = get_jwt_identity()
    
    if current_user.get('role') != UserRole.CLIENT.value:
        return jsonify({'message': 'Only client users can list files'}), 403
    
    files = File.query.all()
    
    file_list = []
    for file in files:
        file_list.append({
            'id': file.id,
            'filename': file.original_filename,
            'file_type': file.file_type,
            'upload_date': file.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({
        'message': 'Files retrieved successfully',
        'files': file_list
    }), 200

@files_bp.route('/download-file/<int:file_id>', methods=['GET'])
@jwt_required()
def get_download_link(file_id):
    current_user = get_jwt_identity()
    
    if current_user.get('role') != UserRole.CLIENT.value:
        return jsonify({'message': 'Only client users can download files'}), 403
    
    file = File.query.get_or_404(file_id)
    
    # Generate encrypted download URL
    encrypted_url = encrypt_url(file.id, current_user.get('user_id'))
    base_url = request.host_url.rstrip('/')
    
    download_link = f"{base_url}/download-file/{encrypted_url}"
    
    return jsonify({
        'message': 'success',
        'download-link': download_link
    }), 200

@files_bp.route('/download-file/<token>', methods=['GET'])
def download_file(token):
    file_id, user_id = decrypt_url(token)
    
    if not file_id or not user_id:
        return jsonify({'message': 'Invalid or expired download link'}), 400
    
    user = User.query.get(user_id)
    if not user or user.role != UserRole.CLIENT.value:
        return jsonify({'message': 'Access denied'}), 403
    
    file = File.query.get_or_404(file_id)
    
    directory = os.path.dirname(file.file_path)
    filename = os.path.basename(file.file_path)
    
    return send_from_directory(
        directory, 
        filename, 
        as_attachment=True, 
        download_name=file.original_filename
    ) 
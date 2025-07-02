# Secure File Sharing System

A secure file-sharing system between Operations Users and Client Users built with Flask.

## Features

- **User Authentication**:

  - Client User Signup with Email Verification
  - Login for both Client and Operations Users
  - JWT-based Authentication

- **File Operations**:

  - Upload Files (Operations Users only)
  - List Files (Client Users only)
  - Download Files with Secure URLs (Client Users only)

- **Security**:
  - Encrypted Download URLs
  - File Type Validation (only pptx, docx, xlsx allowed)
  - Role-based Access Control

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd secure-file-sharing
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///fileshare.db
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password(16 bit)
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=your_email@example.com
BASE_URL=http://localhost:5000
```

### Running the Application

1. Start the Flask application:

```bash
python run.py
```

2. The application will be available at `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /signup` - Register a new client user
- `GET /verify-email/<token>` - Verify email address
- `POST /login` - Login for both client and operations users
- `POST /create-ops-user` - Create an operations user (requires admin key)

### File Operations

- `POST /upload-file` - Upload a file (Operations users only)
- `GET /list-files` - List all uploaded files (Client users only)
- `GET /download-file/<file_id>` - Get a secure download link (Client users only)
- `GET /download-file/<token>` - Download a file using a secure token

## Running Tests

Run the tests using pytest:

```bash
pytest
```

## Deployment

For production deployment:

1. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 "app:create_app()"
```

2. Set up a reverse proxy with Nginx or Apache

3. Use environment variables for configuration instead of `.env` file

4. Consider using a managed database service instead of SQLite

5. Set up proper logging and monitoring

Postman screenshots
![img4](https://github.com/user-attachments/assets/1eabfcc5-8c2f-4e05-8d69-708059bdf851)
![img5](https://github.com/user-attachments/assets/21b5d08e-30b1-4300-be8c-05e7d802a7c3)
![ing2](https://github.com/user-attachments/assets/662f2f0d-6b8d-4069-86b6-498e7d7087ef)
![img1](https://github.com/user-attachments/assets/6cf29e8a-3b6c-4aca-949e-c7e84899ea18)
![img3](https://github.com/user-attachments/assets/59da9765-3d81-4d69-99cd-89c910086902)



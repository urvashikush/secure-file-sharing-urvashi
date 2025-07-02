# How to Run the Secure File Sharing System

## Quick Start

The easiest way to run the application is using the provided shell script:

```bash
./run.sh
```

This script will:

1. Create a virtual environment if it doesn't exist
2. Install all dependencies
3. Initialize the database with an operations user
4. Start the Flask development server

## Manual Setup

If you prefer to set up the application manually, follow these steps:

### 1. Set Up Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///fileshare.db
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=your_email@example.com
BASE_URL=http://localhost:5000
```

### 3. Initialize the Database

Run the initialization script to create the database and an operations user:

```bash
python init_db.py
```

### 4. Run the Application

Start the Flask development server:

```bash
python run.py
```

The application will be available at http://localhost:5000

## Default Users

The initialization script creates an operations user with the following credentials:

- Email: ops@example.com
- Password: password123

You can use these credentials to log in as an operations user and upload files.

## API Testing

Import the provided Postman collection (`postman_collection.json`) to test the API endpoints.

## Running Tests

Run the tests using pytest:

```bash
pytest
```

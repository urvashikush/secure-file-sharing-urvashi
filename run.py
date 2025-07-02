from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Create upload directory if it doesn't exist
    os.makedirs(os.path.join(app.root_path, 'static/uploads'), exist_ok=True)
    app.run(debug=True) 
"""Entry point for the Flask application."""
from app.api import create_app
from app.db import init_db

if __name__ == "__main__":
    init_db()
    app = create_app()
    app.run(host="0.0.0.0", port=8000)

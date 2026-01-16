"""API integration tests."""

import os
import tempfile
from app.api import create_app
from app.db import init_db


def test_health_endpoint():
    """Test health endpoint returns ok status."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        app = create_app()
        client = app.test_client()

        response = client.get("/health")
        assert response.status_code == 200
        assert response.json == {"status": "ok"}


def test_create_user_endpoint():
    """Test POST /users endpoint creates user."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        app = create_app()
        client = app.test_client()

        response = client.post("/users", json={"name": "Alice"})
        assert response.status_code == 201
        assert "id" in response.json
        assert response.json["id"] == 1


def test_get_user_endpoint():
    """Test GET /users/<id> endpoint retrieves user."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        app = create_app()
        client = app.test_client()

        # Create user
        client.post("/users", json={"name": "Bob"})

        # Get user
        response = client.get("/users/1")
        assert response.status_code == 200
        assert response.json["id"] == 1
        assert response.json["name"] == "Bob"


def test_get_nonexistent_user():
    """Test GET /users/<id> returns 404 for nonexistent user."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        app = create_app()
        client = app.test_client()

        response = client.get("/users/999")
        assert response.status_code == 404
        assert response.json == {"error": "not found"}


def test_dothing_endpoint_valid():
    """Test POST /dothing with valid meta data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        app = create_app()
        client = app.test_client()

        response = client.post(
            "/dothing", json={"name": "test_user", "meta": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
        )
        assert response.status_code == 200
        assert response.json["status"] == "ok"
        assert response.json["result"] is True


def test_dothing_endpoint_invalid_meta_count():
    """Test POST /dothing with wrong number of meta values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        app = create_app()
        client = app.test_client()

        response = client.post(
            "/dothing",
            json={"name": "test_user", "meta": [1, 2, 3]},  # Only 3 values instead of 9
        )
        assert response.status_code == 400
        assert "meta must be a list of 9 values" in response.json["error"]


def test_dothing_endpoint_invalid_meta_not_list():
    """Test POST /dothing with non-list meta data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        app = create_app()
        client = app.test_client()

        response = client.post(
            "/dothing", json={"name": "test_user", "meta": "not a list"}
        )
        assert response.status_code == 400

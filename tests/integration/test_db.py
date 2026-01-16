"""Integration tests for database and API."""

import os
import tempfile
import sqlite3
from app.db import init_db, add_user, get_user, User


def test_init_db():
    """Test database initialization creates users table."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path

        init_db()

        # Verify table exists
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        assert cur.fetchone() is not None
        con.close()


def test_add_user_success():
    """Test adding a user to database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        user_id = add_user("John Doe")

        assert user_id == 1
        user = get_user(user_id)
        assert user is not None
        assert user.name == "John Doe"


def test_add_user_empty_name_raises_error():
    """Test adding user with empty name raises ValueError."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        try:
            add_user("")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "name must be non-empty" in str(e)


def test_get_user_not_found():
    """Test getting non-existent user returns None."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        user = get_user(999)
        assert user is None


def test_add_multiple_users():
    """Test adding multiple users."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ["APP_DB_PATH"] = db_path
        init_db()

        id1 = add_user("Alice")
        id2 = add_user("Bob")
        id3 = add_user("Charlie")

        assert id1 == 1
        assert id2 == 2
        assert id3 == 3
        assert get_user(id1).name == "Alice"
        assert get_user(id2).name == "Bob"
        assert get_user(id3).name == "Charlie"


def test_user_dataclass():
    """Test User dataclass."""
    user = User(id=1, name="Test")
    assert user.id == 1
    assert user.name == "Test"

    # Test immutability
    try:
        user.name = "Modified"
        assert False, "User should be frozen"
    except AttributeError:
        pass

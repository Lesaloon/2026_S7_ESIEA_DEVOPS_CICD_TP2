"""Unit tests for data transformations (utils.py)."""

from app.utils import doThing, GLOBAL


def test_dothing_new_user():
    """Test doThing creates a new user."""
    GLOBAL["users"].clear()
    result = doThing("alice", 1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert result is True
    assert len(GLOBAL["users"]) == 1
    assert GLOBAL["users"][0]["name"] == "alice"
    assert GLOBAL["users"][0]["meta"] == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_dothing_update_existing_user():
    """Test doThing updates an existing user."""
    GLOBAL["users"].clear()
    doThing("bob", 1, 2, 3, 4, 5, 6, 7, 8, 9)
    result = doThing("bob", 10, 20, 30, 40, 50, 60, 70, 80, 90)
    assert result is True
    assert len(GLOBAL["users"]) == 1
    assert GLOBAL["users"][0]["meta"] == [10, 20, 30, 40, 50, 60, 70, 80, 90]


def test_dothing_multiple_users():
    """Test doThing handles multiple users."""
    GLOBAL["users"].clear()
    doThing("user1", 1, 2, 3, 4, 5, 6, 7, 8, 9)
    doThing("user2", 10, 20, 30, 40, 50, 60, 70, 80, 90)
    assert len(GLOBAL["users"]) == 2
    assert GLOBAL["users"][0]["name"] == "user1"
    assert GLOBAL["users"][1]["name"] == "user2"


def test_dothing_exception_handling():
    """Test doThing exception handling returns None."""
    GLOBAL["users"].clear()
    # Corrupt the GLOBAL state to cause an exception
    GLOBAL["users"] = None
    result = doThing("test", 1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert result is None

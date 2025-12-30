"""
Unit tests for core business logic and password hashing
"""

from werkzeug.security import generate_password_hash, check_password_hash

# Core logic function
def should_delete_post(status: str) -> bool:
    return status.strip().lower() == "claimed"

# Minimal User class for testing password logic
class UserTest:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.password_hash = None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def test_set_password_hashes_password():
    user = UserTest("testuser", "test@test.com")
    user.set_password("123456")
    assert user.password_hash is not None
    assert user.password_hash != "123456"


def test_check_password_validation():
    user = UserTest("testuser", "test@test.com")
    user.set_password("123456")
    assert user.check_password("123456") is True
    assert user.check_password("wrong") is False


def test_should_delete_post_when_claimed():
    assert should_delete_post("claimed") is True
    assert should_delete_post("CLAIMED") is True
    assert should_delete_post("lost") is False

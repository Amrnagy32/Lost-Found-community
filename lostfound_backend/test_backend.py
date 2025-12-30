"""
Unit tests for core business logic and security-related functions.

This file includes both:
1. The core function for deleting posts based on status.
2. Unit tests for password security and business logic.
"""

# --- Core function (service) ---
def should_delete_post(status: str) -> bool:
    """
    Determines whether a post should be deleted
    based on its status.
    """
    return status.strip().lower() == "claimed"


# --- Minimal User class for testing password logic ---
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.password_hash = None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# --- Unit Tests ---
def test_set_password_hashes_password():
    """
    Ensure that the password is stored as a hash
    and not as plain text.
    """
    user = User(username="testuser", email="test@test.com")
    user.set_password("123456")

    assert user.password_hash is not None
    assert user.password_hash != "123456"


def test_check_password_validation():
    """
    Verify that password checking works correctly
    for both valid and invalid passwords.
    """
    user = User(username="testuser", email="test@test.com")
    user.set_password("123456")

    assert user.check_password("123456") is True
    assert user.check_password("wrongpassword") is False


def test_should_delete_post_when_claimed():
    """
    Ensure that a post is deleted only when
    its status is set to 'claimed'.
    """
    assert should_delete_post("claimed") is True
    assert should_delete_post("CLAIMED") is True
    assert should_delete_post("lost") is False

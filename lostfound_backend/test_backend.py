"""
Unit tests for core business logic and password hashing
in the Lost‑Found‑community project.
"""

import pytest
from backend.models import User
from backend.utils import allowed_file  # example utility if exists

# Core logic: check claimed status
def should_delete_post(status: str) -> bool:
    return status.strip().lower() == "claimed"


def test_set_password_hashes_password():
    user = User(username="testuser", email="test@test.com")
    user.set_password("123456")

    assert user.password_hash is not None
    assert user.password_hash != "123456"


def test_check_password_validation():
    user = User(username="testuser", email="test@test.com")
    user.set_password("123456")

    assert user.check_password("123456") is True
    assert user.check_password("wrong") is False


def test_should_delete_post_when_claimed():
    assert should_delete_post("claimed") is True
    assert should_delete_post("CLAIMED") is True
    assert should_delete_post("lost") is False


import pytest
from app import app as flask_app  # Import the app that already has db registered
from database import db
from models import User, Post

@pytest.fixture
def client():
    # Configure the app for testing mode
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with flask_app.app_context():
        # We don't call init_app here because app.py already did it!
        db.create_all()  # Create tables in the in-memory DB
        
        # Ensure a clean test user exists
        if not User.query.filter_by(username="testuser").first():
            u = User(username="testuser", email="test@test.com")
            u.set_password("password123")
            db.session.add(u)
            db.session.commit()
            
    with flask_app.test_client() as client:
        yield client
    
    # Cleanup after test finishes
    with flask_app.app_context():
        db.drop_all()

def get_token(client):
    # Get JWT from the auth route
    res = client.post('/auth/login', json={
        "identifier": "testuser",
        "password": "password123"
    })
    return res.get_json()['access_token']

def test_claimed_status_deletes_from_db(client):
    """Verifies that 'claimed' status deletes the record"""
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    with flask_app.app_context():
        u = User.query.filter_by(username="testuser").first()
        post = Post(title="Test Item", category="Keys", status="lost", phone_number="123", reporter=u)
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    # Send PUT request with 'claimed' status as JSON
    response = client.put(f'/posts/{post_id}', headers=headers, json={"status": "claimed"})

    assert response.status_code == 200
    
    # Verify the post is deleted from the DB
    with flask_app.app_context():
        assert Post.query.get(post_id) is None
import pytest
from app import app as flask_app
from database import db
from models import User, Post

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with flask_app.app_context():
        db.create_all()
        if not User.query.filter_by(username="testuser").first():
            u = User(username="testuser", email="test@test.com")
            u.set_password("password123")
            db.session.add(u)
            db.session.commit()
            
    with flask_app.test_client() as client:
        yield client
    
    with flask_app.app_context():
        db.drop_all()

def get_token(client):
    res = client.post('/auth/login', json={
        "identifier": "testuser",
        "password": "password123"
    })
    return res.get_json()['access_token']

def test_claimed_status_deletes_from_db(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    with flask_app.app_context():
        u = User.query.filter_by(username="testuser").first()
        post = Post(title="Test Item", category="Keys", status="lost", phone_number="123", reporter=u)
        db.session.add(post)
        db.session.commit()
        post_id = post.id
    response = client.put(f'/posts/{post_id}', headers=headers, json={"status": "claimed"})
    assert response.status_code == 200
    with flask_app.app_context():
        assert Post.query.get(post_id) is None

def test_create_post(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    res = client.post('/posts', headers=headers, json={
        "title": "New Item",
        "category": "Wallet",
        "status": "lost",
        "phone_number": "456"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['title'] == "New Item"
    assert data['status'] == "lost"

def test_user_login(client):
    res = client.post('/auth/login', json={
        "identifier": "testuser",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data

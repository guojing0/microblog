import os
import tempfile

import pytest

from app import app, db
from app.models import Post, User


@pytest.fixture
def test_app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to serve as the database
    db_fd, db_path = tempfile.mkstemp()

    # Configure the app for testing
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(test_app):
    """A test client for the app."""
    return test_app.test_client()


@pytest.fixture
def runner(test_app):
    """A test runner for the app's Click commands."""
    return test_app.test_cli_runner()


@pytest.fixture
def auth(client):
    """Helper for authentication in tests."""
    class AuthActions:
        def __init__(self, client):
            self._client = client

        def register(self, username='test', email='test@example.com', password='test'):
            return self._client.post(
                '/register',
                data={'username': username, 'email': email, 'password': password, 'password2': password}
            )

        def login(self, username='test', password='test'):
            return self._client.post(
                '/login',
                data={'username': username, 'password': password, 'remember_me': False}
            )

        def logout(self):
            return self._client.get('/logout')

    return AuthActions(client)


@pytest.fixture
def sample_user(test_app):
    """Create a sample user for testing."""
    with test_app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def sample_post(test_app, sample_user):
    """Create a sample post for testing."""
    with test_app.app_context():
        post = Post(body='Test post content', user_id=sample_user.id)
        db.session.add(post)
        db.session.commit()
        return post

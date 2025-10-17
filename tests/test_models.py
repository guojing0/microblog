"""Tests for the models module."""

from datetime import UTC, datetime

from app.models import Post, User


class TestUser:
    """Test cases for the User model."""

    def test_user_creation(self, test_app):
        """Test creating a new user."""
        with test_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')

            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
            assert user.password_hash is not None
            assert user.password_hash != 'testpassword'  # Should be hashed

    def test_password_hashing(self, test_app):
        """Test password hashing and verification."""
        with test_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')

            # Test correct password
            assert user.check_password('testpassword') is True

            # Test incorrect password
            assert user.check_password('wrongpassword') is False

    def test_user_repr(self, test_app):
        """Test user string representation."""
        with test_app.app_context():
            user = User(username='testuser', email='test@example.com')
            assert repr(user) == '<User testuser>'

    def test_user_posts_relationship(self, test_app):
        """Test the relationship between User and Post."""
        with test_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')

            post = Post(body='Test post', user_id=user.id)

            # Test the relationship
            assert post.author == user
            assert post in user.posts


class TestPost:
    """Test cases for the Post model."""

    def test_post_creation(self, test_app):
        """Test creating a new post."""
        with test_app.app_context():
            post = Post(body='Test post content', user_id=1)

            assert post.body == 'Test post content'
            assert post.user_id == 1
            assert isinstance(post.timestamp, datetime)

    def test_post_timestamp(self, test_app):
        """Test that post timestamp is set correctly."""
        with test_app.app_context():
            before_creation = datetime.now(UTC)
            post = Post(body='Test post', user_id=1)
            after_creation = datetime.now(UTC)

            assert before_creation <= post.timestamp <= after_creation

    def test_post_repr(self, test_app):
        """Test post string representation."""
        with test_app.app_context():
            post = Post(body='Test post content', user_id=1)
            assert repr(post) == '<Post Test post content>'

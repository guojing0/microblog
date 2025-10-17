"""Tests for the routes module."""



class TestIndexRoute:
    """Test cases for the index route."""

    def test_index_redirects_when_not_logged_in(self, client):
        """Test that index redirects to login when user is not authenticated."""
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_index_redirects_when_not_logged_in_alt_route(self, client):
        """Test that /index redirects to login when user is not authenticated."""
        response = client.get('/index')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_index_loads_when_logged_in(self, client, auth, sample_user):
        """Test that index loads when user is logged in."""
        auth.login('testuser', 'testpassword')
        response = client.get('/')
        assert response.status_code == 200
        assert b'Home' in response.data


class TestLoginRoute:
    """Test cases for the login route."""

    def test_login_page_loads(self, client):
        """Test that login page loads correctly."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Sign In' in response.data

    def test_login_redirects_when_already_logged_in(self, client, auth, sample_user):
        """Test that login redirects when user is already logged in."""
        auth.login('testuser', 'testpassword')
        response = client.get('/login')
        assert response.status_code == 302
        assert '/' in response.location

    def test_login_with_valid_credentials(self, client, sample_user):
        """Test login with valid credentials."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword',
            'remember_me': False
        })
        assert response.status_code == 302
        assert '/' in response.location

    def test_login_with_invalid_credentials(self, client, sample_user):
        """Test login with invalid credentials."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword',
            'remember_me': False
        })
        assert response.status_code == 302
        assert '/login' in response.location


class TestLogoutRoute:
    """Test cases for the logout route."""

    def test_logout_redirects_to_index(self, client, auth, sample_user):
        """Test that logout redirects to index."""
        auth.login('testuser', 'testpassword')
        response = client.get('/logout')
        assert response.status_code == 302
        assert '/' in response.location


class TestRegisterRoute:
    """Test cases for the register route."""

    def test_register_page_loads(self, client):
        """Test that register page loads correctly."""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Register' in response.data

    def test_register_redirects_when_already_logged_in(self, client, auth, sample_user):
        """Test that register redirects when user is already logged in."""
        auth.login('testuser', 'testpassword')
        response = client.get('/register')
        assert response.status_code == 302
        assert '/' in response.location

    def test_register_with_valid_data(self, client):
        """Test registration with valid data."""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'newpassword'
        })
        assert response.status_code == 302
        assert '/login' in response.location

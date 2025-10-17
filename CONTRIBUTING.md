# Contributing to Microblog

## Development Setup

### Prerequisites
- Python 3.11+ (3.13 recommended)
- uv package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd microblog
   ```

2. **Install dependencies**
   ```bash
   uv sync --dev
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations**
   ```bash
   uv run flask db upgrade
   ```

5. **Run the development server**
   ```bash
   uv run flask run
   ```

## Testing

### Running Tests
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/test_models.py

# Run with verbose output
uv run pytest -v
```

### Test Structure
- `tests/` - Test directory
- `tests/conftest.py` - Pytest configuration and fixtures
- `tests/test_models.py` - Model tests
- `tests/test_routes.py` - Route tests

## Code Quality

### Linting and Formatting
```bash
# Run linting
uv run ruff check .

# Auto-fix linting issues
uv run ruff check . --fix

# Format code
uv run ruff format .

# Type checking
uv run mypy app/
```

### Pre-commit Hooks
Install pre-commit hooks to automatically run checks before commits:
```bash
uv run pre-commit install
```

## CI/CD

### GitHub Actions Workflows

1. **CI Workflow** (`.github/workflows/ci.yml`)
   - Runs on every push and pull request
   - Tests on Python 3.11, 3.12, and 3.13
   - Runs linting, type checking, and tests
   - Generates coverage reports

2. **Security Workflow** (`.github/workflows/security.yml`)
   - Runs weekly and on main branch changes
   - Performs security scans with Bandit, Safety, and Semgrep
   - Uploads results to GitHub Security tab

3. **Deploy Workflow** (`.github/workflows/deploy.yml`)
   - Runs on pushes to main branch
   - Handles database migrations
   - Ready for deployment to various platforms

### Required Secrets
For deployment, set these secrets in your GitHub repository:
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Production database URL
- Platform-specific secrets (Heroku, Railway, etc.)

## Database Migrations

### Creating Migrations
```bash
# After making model changes
uv run flask db migrate -m "Description of changes"
```

### Applying Migrations
```bash
# Apply all pending migrations
uv run flask db upgrade

# Downgrade to previous migration
uv run flask db downgrade
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write tests for new functionality
   - Ensure all tests pass
   - Run linting and type checking

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add your feature"
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Ensure CI passes**
   - All GitHub Actions workflows must pass
   - Code coverage should not decrease
   - Security scans must pass

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for classes and functions
- Keep functions small and focused
- Use meaningful variable and function names

## Security

- Never commit secrets or API keys
- Use environment variables for configuration
- Keep dependencies updated
- Run security scans regularly
- Follow OWASP guidelines for web security

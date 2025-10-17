.PHONY: help install test lint format type-check security clean run migrate

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	uv sync --dev

test:  ## Run tests
	uv run pytest tests/ -v --cov=app --cov-report=html --cov-report=term

test-fast:  ## Run tests without coverage
	uv run pytest tests/ -v

lint:  ## Run linting
	uv run ruff check .

lint-fix:  ## Fix linting issues
	uv run ruff check . --fix

format:  ## Format code
	uv run ruff format .

type-check:  ## Run type checking
	uv run mypy app/

security:  ## Run security checks
	uv run bandit -r app/
	uv run safety check

check: lint type-check security  ## Run all checks

run:  ## Run the development server
	uv run flask run

migrate:  ## Create a new migration
	uv run flask db migrate -m "$(msg)"

upgrade:  ## Apply database migrations
	uv run flask db upgrade

downgrade:  ## Rollback database migrations
	uv run flask db downgrade

clean:  ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/

setup: install migrate  ## Initial setup for development
	@echo "Setup complete! Run 'make run' to start the development server."

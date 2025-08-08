.PHONY: install install-dev test lint format clean

install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

lint: ## Run linting checks
	flake8 src/
	mypy src/

format: ## Format code with black and isort
	black src/
	isort src/

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# CLI commands are now available globally via 'zn' command
# run-new: zn --new
# run-mr: zn --mr

setup: install install-dev ## Set up the development environment
	@echo "Development environment set up successfully!" 
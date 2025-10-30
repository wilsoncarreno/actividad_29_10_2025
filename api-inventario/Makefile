.PHONY: install test test-unit test-bdd test-load coverage coverage-html behave behave-html locust run clean help

# Variables
PYTHON := python
POETRY := poetry
FLASK_APP := src/inventario/app.py
LOCUST_FILE := locustfile.py
HOST := http://localhost:5000
WEB_HOST := 127.0.0.1
WEB_PORT := 8089

# Install dependencies
install:
	$(POETRY) install

# Run all tests
test: test-unit test-bdd

# Run unit tests with coverage
test-unit:
	$(POETRY) run coverage run -m pytest
	$(POETRY) run coverage report --include=src/*

# Run BDD tests
test-bdd:
	$(POETRY) run behave

# Run load tests (requires running server first)
test-load:
	@echo "Make sure the Flask server is running on $(HOST)"
	@echo "Then access Locust web interface at http://$(WEB_HOST):$(WEB_PORT)"
	$(POETRY) run locust -f $(LOCUST_FILE) --host=$(HOST) --web-host=$(WEB_HOST) --web-port=$(WEB_PORT)

# Generate coverage reports
coverage:
	$(POETRY) run coverage run -m pytest
	$(POETRY) run coverage report --include=src/*

coverage-html:
	$(POETRY) run coverage run -m pytest
	$(POETRY) run coverage html --include=src/*
	@echo "HTML coverage report generated in htmlcov/index.html"

# Run BDD tests (alias for test-bdd)
behave: test-bdd

# Run Flask application
run:
	$(POETRY) run python $(FLASK_APP)

# Clean up generated files
clean:
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf __pycache__/
	rm -rf *.pyc
	rm -rf .pytest_cache/
	rm -rf features/reports/

# Show help
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies with Poetry"
	@echo "  test         - Run all tests (unit + BDD)"
	@echo "  test-unit    - Run unit tests with coverage"
	@echo "  test-bdd     - Run BDD tests with Behave"
	@echo "  test-load    - Run Locust load tests (requires running server)"
	@echo "  coverage     - Generate coverage report"
	@echo "  coverage-html- Generate HTML coverage report"
	@echo "  behave       - Run BDD tests"
	@echo "  run          - Run Flask application"
	@echo "  clean        - Clean up generated files"
	@echo "  help         - Show this help message"
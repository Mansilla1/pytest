.DEFAULT_GOAL := help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: ## Install dependencies
	poetry install --no-interaction --no-root

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	poetry run pre-commit run --all-files --show-diff-on-failure

.PHONY: ruff-checker
ruff-checker: ## Run Ruffus checker
	poetry run ruff check . && poetry run ruff format . --diff

.PHONY: mypy
mypy: ## Run mypy
	poetry run mypy src/

.PHONY: test
test: ## Run tests
	poetry run pytest

.PHONY: coverage-report
coverage-report: ## Run tests with coverage report
	open htmlcov/index.html

.PHONY: talisman-report
talisman-report: ## Run Talisman scan and serve the HTML report
	@echo "Running Talisman security scan..."
	talisman --scanWithHtml || true
	@echo "Starting local server for Talisman report..."
	@cd talisman_html_report && python3 -m http.server 8081

.PHONY: lizard-report
lizard-report: ## Run Lizard scan and serve the HTML report
	poetry run lizard -l python --output_file lizard-report.html src/

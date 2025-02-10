.DEFAULT_GOAL := help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	poetry run pre-commit run --all-files --show-diff-on-failure

.PHONY: test
test: ## Run tests
	poetry run pytest

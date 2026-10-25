.PHONY: help
help:
	@echo "init - initialize a clean clone"
	@echo "lint - run prek on all files"
	@echo "update-precommit - update pre-commit config"

.PHONY: init
init:
	uv sync --frozen
	uv run prek install

.PHONY: lint
lint:
	uv run prek run --all-files

.PHONY: update-precommit
update-precommit:
	uv run prek autoupdate

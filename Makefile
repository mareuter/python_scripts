.PHONY: help
help:
	@echo "init - initialize a clean clone"
	@echo "update-precommit - update pre-commit config"


.PHONY: init
init:
	uv sync --frozen
	uv run prek install

.PHONY: update-precommit
update-precommit:
	uv run prek autoupdate

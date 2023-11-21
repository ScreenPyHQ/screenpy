# shortcuts to help manage flipping between branches with different dependencies
sync:
	poetry install --extras dev_all --sync

update_lock_only:
	poetry update --lock

update: update_lock_only
	poetry install --extras dev_all

check:
	poetry check

requirements:
	poetry export --without-hashes --with dev -f requirements.txt > requirements.txt

.PHONY: sync update_lock_only update check requirements

black-check:
	black --check .

black:
	black .

ruff:
	ruff check .

ruff-fix:
	ruff check . --fix --show-fixes

mypy:
	mypy .

lint: ruff mypy

.PHONY: black-check black ruff ruff-fix mypy lint

pre-check-in: black-check lint

pre-check-in-fix: black ruff-fix mypy

.PHONY: pre-check-in pre-check-in-fix

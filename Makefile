# shortcuts to help manage flipping between branches with different dependencies
sync:
	poetry install --extras dev_all --sync

update:
	poetry update --extras dev_all

requirements:
	poetry export --without-hashes --with dev -f requirements.txt > requirements.txt

.PHONY: sync update requirements

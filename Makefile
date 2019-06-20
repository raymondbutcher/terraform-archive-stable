.PHONY: all
all: format test

.PHONY: format
format:
	isort *.py tests/*.py
	black *.py tests/*.py
	flake8 --ignore E501 *.py tests/*.py
	terraform fmt

.PHONY: test
test:
	pytest -v

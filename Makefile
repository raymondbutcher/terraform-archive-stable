.PHONY: all
all:
	isort *.py tests/*.py
	black *.py tests/*.py
	flake8 --ignore E501 *.py tests/*.py
	terraform fmt

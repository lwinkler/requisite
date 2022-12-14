PYTHON=python3
ALL_FILES=$(shell git ls-files | grep "\.py\>")

all: run

lint: pylint flake8 mypy black
format: black_format


pylint:
	${PYTHON} -m pylint ${ALL_FILES}

flake8:
	${PYTHON} -m flake8 .

mypy:
	${PYTHON} -m mypy .

mypy-strict:
	${PYTHON} -m mypy --strict .

black:
	${PYTHON} -m black --check .

format_black:
	${PYTHON} -m black .

run:
	${PYTHON} parse.py -e specs/requisite.yaml -o out.yaml -O report.html

tests:
	${PYTHON} -m unittest discover

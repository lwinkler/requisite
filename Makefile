PYTHON=python3
ALL_FILES=$(shell git ls-files | grep "\.py\>")

all: check testing tests

lint: pylint flake8 mypy black
format: black_format


pylint:
	${PYTHON} -m pylint ${ALL_FILES}

flake8:
	${PYTHON} -m flake8 .

mypy:
	# TODO: fix properly ?
	${PYTHON} -m mypy . --explicit-package-bases

mypy-strict:
	${PYTHON} -m mypy --strict . --explicit-package-bases

black:
	${PYTHON} -m black --check .

format_black:
	${PYTHON} -m black .

check:
	${PYTHON} release.py specs/setup.py specs/requisite.yaml -o out.yaml -O report.html

testing:
	${PYTHON} release.py specs/setup.py specs/requisite.yaml -d releases/dummy

tests:
	${PYTHON} -m unittest discover

PYTHON=python3
ALL_FILES=$(shell git ls-files | grep "\.py\>")



all: check release run_tests

lint: pylint flake8 mypy black
format: black_format


pylint:
	PYTHONPATH=./src/requisite ${PYTHON} -m pylint ${ALL_FILES}

flake8:
	${PYTHON} -m flake8 .

mypy:
	MYPYPATH=./src/requisite ${PYTHON} -m mypy src
	# --explicit-package-bases
	MYPYPATH=./src/requisite ${PYTHON} -m mypy tests
	# --explicit-package-bases

mypy-strict:
	MYPYPATH=./src/requisite ${PYTHON} -m mypy --strict . --explicit-package-bases

black:
	${PYTHON} -m black --check .

format_black:
	${PYTHON} -m black .

check:
	${PYTHON} src/requisite/__main__.py specs/setup.py specs/requisite.yaml --output-yaml out.yaml
	${PYTHON} src/requisite/__main__.py specs/setup.py specs/requisite.yaml --report report.html

release:
	${PYTHON} src/requisite/__main__.py specs/setup.py specs/requisite.yaml -r releases/dummy

run_tests:
	(cd tests/ && PYTHONPATH=../src/requisite ${PYTHON} -m unittest discover)

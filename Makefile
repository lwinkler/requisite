PYTHON=python3
ALL_FILES=$(shell git ls-files | grep "\.py\>")

all: run

lint: pylint flake8 mypy 
format: black


pylint:
	${PYTHON} -m pylint ${ALL_FILES}

flake8:
	${PYTHON} -m flake8 .

mypy:
	${PYTHON} -m mypy .

black:
	${PYTHON} -m black

run:
	${PYTHON} main.py

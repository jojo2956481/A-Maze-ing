PYTHON = python3
FILE = config.txt

run: name

install:
	python3 -m pip install flake8
	python3 -m pip install mypy
	./.install_mlx

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untypes-defs --check-untypes-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict

name:
	@$(PYTHON) genere_maze.py $(FILE)

clean:
	rm -f *.pyc __pycache__/*
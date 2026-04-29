PYTHON = python3
FILE = config.txt

run: name

debug:
	@$(PYTHON) -m pdb a_maze_ing.py $(FILE)

install:
	python3 -m pip install flake8
	python3 -m pip install pydantic
	python3 -m pip install mypy
	pip install mlx-2.2-py3-none-any.whl

lint:
	flake8 srcs a_maze_ing.py
	mypy srcs a_maze_ing.py --warn-return-any --warn-unused-ignores --ignore-missing-imports  --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 srcs a_maze_ing.py
	mypy srcs a_maze_ing.py --strict

build: 
	pip install poetry && poetry build --output .

name:
	@$(PYTHON) a_maze_ing.py $(FILE)

clean:
	rm -rf */*/__pycache__/ */*/*/__pycache__ */*__pycache__
	rm -rf .mypy_cache/
	rm -f *.xpm
	rm -f maze.txt
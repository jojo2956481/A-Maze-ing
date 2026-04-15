PYTHON = python3
FILE = config.txt

run: name

install:
	python3 -m pip install flake8
	python3 -m pip install mypy
	pip install mlx-2.2-py3-none-any.whl

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untypes-defs --check-untypes-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict

build: 
	pip install poetry && poetry build --output .

name:
	@$(PYTHON) srcs/main.py $(FILE)

clean:
	rm -rf */*/__pycache__/
	rm -rf .mypy_cache/
	rm -f *.xpm
	rm -f maze.txt
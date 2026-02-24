PYTHON = python3
FILE = config.txt

run: name

name:
	@$(PYTHON) genere_maze.py $(FILE)

clean:
	rm -f *.pyc __pycache__/*
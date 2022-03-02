PIPENV = pipenv
PYTHON = $(PIPENV) run python

.PHONY: run preview_cmaps install

all: run

run:
	$(PYTHON) src/main.py

preview_cmaps: 
	$(PYTHON) src/colormaps.py

install:
	$(PIPENV) install

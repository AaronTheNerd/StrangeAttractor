# Written by Aaron Barge
# Copyright 2022

PIPENV = pipenv
PYTHON = $(PIPENV) run python
PDOC = pdoc
PDOC_FLAGS = --force --config latex_math=True --config sort_identifiers=False --output-dir docs --html

.PHONY: run preview_cmaps test install docs clean

all: run

run:
	$(PYTHON) -m src.main
	
preview_cmaps: 
	$(PYTHON) -m src.colormaps

test:
	$(PYTHON) -m src.test.main

install:
	$(PIPENV) install

docs: 
	$(PYTHON) -m $(PDOC) $(PDOC_FLAGS) src
	mv -v docs/src/* docs
	rm -r docs/src


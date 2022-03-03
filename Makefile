# Written by Aaron Barge
# Copyright 2022

PIPENV = pipenv
PYTHON = $(PIPENV) run python
PDOC = pdoc
PDOC_FLAGS = --force --config latex_math=True --config sort_identifiers=False --output-dir docs --html

SRC_FILES = $(wildcard src/*.py)
DOC_FILES = $(subst py,html,$(subst src,html,$(SRC_FILES)))

.PHONY: run preview_cmaps install docs clean

all: run docs

run:
	$(PYTHON) -m src.main
	
preview_cmaps: 
	$(PYTHON) -m src.colormaps

install:
	$(PIPENV) install

docs: 
	$(PYTHON) -m $(PDOC) $(PDOC_FLAGS) src
	mv -v docs/src/* docs
	rm -r docs/src

clean:
	rm -rf html

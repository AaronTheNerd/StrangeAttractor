# Written by Aaron Barge
# Copyright 2022

PIPENV = pipenv
PYTHON = $(PIPENV) run python

.PHONY: run preview_cmaps install

all: run

run:
	$(PYTHON) -m src.main
	
preview_cmaps: 
	$(PYTHON) -m src.colormaps

install:
	$(PIPENV) install

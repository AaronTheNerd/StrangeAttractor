# Written by Aaron Barge
# Copyright 2022

PIPENV = pipenv
PYTHON = $(PIPENV) run python
PDOC = pdoc
PDOC_FLAGS = --force --config latex_math=True --config sort_identifiers=False --output-dir docs --html
CONFIGS = $(wildcard maps/*/configs.yml)
IMAGES = $(wildcard maps/*/*.png)
LEGACY_CONFIGS = $(patsubst %.yml, %_legacy.yml, $(CONFIGS))
LEGACY_IMAGES = $(patsubst %.png, %_legacy.png, $(IMAGES))

.PHONY: run preview_cmaps preview_starscape test install update clean_legacy docs backup

all: run

run:
	$(PYTHON) -m src.main
	
preview_cmaps: 
	$(PYTHON) -m src.colormaps

test:
	$(PYTHON) -m src.test.main

install:
	$(PIPENV) install

maps/%/configs_legacy.yml: maps/%/configs.yml
	mv $^ $@

maps/%_legacy.png: maps/%.png
	mv $^ $@

update: $(LEGACY_CONFIGS) $(LEGACY_IMAGES)

clean_legacy:
	rm -I $(LEGACY_CONFIGS) $(LEGACY_IMAGES)

docs: 
	$(PYTHON) -m $(PDOC) $(PDOC_FLAGS) src
	mv -v docs/src/* docs
	rm -r docs/src

backup:
	tar -czvf $@.tar.gz Makefile Pipfile* README.md configs.yml .gitignore docs maps src 

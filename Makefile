SHELL := /bin/bash

APP_VERSION_STR = "v1-0"

PYLINT = pylint
PYLINTFLAGS = -rn

PYTHONFILES := $(wildcard *.py)

pylint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

.PHONY: all
all: help
.DEFAULT_GOAL:=help

.PHONY: help
help: ## show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: setup
setup: ## setup the project for development
	python3 -m pip install --user pylint
	python3 -m pip install --user autopep8

.PHONY: setup-venv
setup-venv: ## create virtual environment for this project
	python3 -m venv env
	source ./env/bin/activate ; pip install -r requirements.txt

.PHONY: diagrams
diagrams: ## generate plantuml diagrams
	bash ./docs/diagrams/generate_diagrams.sh

.PHONY: lint
lint: ## lint the source code - (without tests)
	$(PYLINT) $(PYLINTFLAGS) main.py pime2

.PHONY: format
format: ## auto-format the code
	autopep8 --in-place --aggressive -r main.py pime2

.PHONY: test
test: ## run unit tests
	python3 -m unittest test/*.py

.PHONY: runtest
runtest: setup-venv ## run app for 15 secs - if possible
	source env/bin/activate ; export me_runtest=$$(timeout 10 python3 main.py) ; if [[ $$me_runtest -eq 143 || $$me_runtest -eq 0 ]]; then exit 0; else exit 1; fi

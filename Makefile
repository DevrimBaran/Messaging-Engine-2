SHELL := /bin/bash

APP_VERSION_STR = "v1-0"

PYLINT = pylint
PYLINTFLAGS = -rn

PYTHONFILES := $(wildcard *.py)
ifdef OS
PYTHON = python
else
PYTHON = python3
endif

pylint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

.PHONY: all
all: help
.DEFAULT_GOAL:=help

.PHONY: help
help: ## show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: setup
setup: ## setup the project for development
	$(PYTHON) -m pip install --user pylint
	$(PYTHON) -m pip install --user autopep8

.PHONY: setup-venv
setup-venv: ## create virtual environment for this project
	$(PYTHON) -m venv env
ifdef OS
	powershell Set-ExecutionPolicy AllSigned -Scope Process; ./env/Scripts/activate ; pip install -r .\requirements.txt; Set-ExecutionPolicy Default -Scope Process
else
	source ./env/bin/activate ; pip install -r requirements.txt
endif

.PHONY: setup-venv-raspi
setup-venv-raspi: ## create virtual environment for this project
	python3 -m venv env
	source ./env/bin/activate ; pip install -r requirements-raspi.txt

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
	$(PYTHON) -m unittest test/*.py

.PHONY: runtest
runtest: setup-venv ## run app for 10 secs - if possible
	source env/bin/activate ; export me_runtest=$(timeout 10 python3 main.py || echo "$$?") ; if [[ $$me_runtest -eq 143 || $$me_runtest -eq 0 ]]; then exit 0; else exit 1; fi ; unset $$me_runtest
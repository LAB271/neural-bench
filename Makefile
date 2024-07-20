PACKAGE=bench
# This works with Visual Studio Code
VIRTUALENV=./.$(PACKAGE)
PYTHON=$(VIRTUALENV)/bin/python
.PHONY: test lint coverage help

default: clean env

all: $(TARGETS)

clean: ## Clean all build files
	@find . -name *.pyc -delete
	@rm -rdf build dist
	@rm -rdf $(VIRTUALENV)
	@rm -frd .pytest_cache .ruff_cache .coverage
	@rm -rfd __pycache__

dev: $(PYTHON) ## Install this for development
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -r requirements.txt
	@$(PYTHON) -m pip install -e .

venv: $(PYTHON) dev ## create the local virtualenv

upgrade: $(PYTHON) ## update from requirements.txt
	@$(PYTHON) -m pip install --upgrade -r requirements.txt
	
$(PYTHON):
	virtualenv $(VIRTUALENV)
	echo "To activate 'source $(VIRTUALENV)/bin/activate'"

freeze:  ## Freezes pip requirements
	echo "# Generated on `date`" >| requirements.txt
	$(PYTHON) -m pip freeze | grep -v "$(PACKAGE)" >> requirements.txt

hello:  ## Run my first playbook
	ansible-playbook playbooks/hello.yml

help: ## Shows help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
	@echo ""

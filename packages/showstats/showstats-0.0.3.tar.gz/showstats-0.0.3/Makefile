# Targets

## Install Python Dependencies
.PHONY: reqs
reqs:
	uv pip install -r dev-requirements.txt

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf ./README.quarto_ipynb
	
## Fix code using ruff
.PHONY: fix
fix:
	ruff check --select I --fix
	ruff check --fix
	ruff format

## Time show_stats
.PHONY: timing
timing:
	cd notebooks && jupyter nbconvert --to notebook --execute --inplace --ClearMetadataPreprocessor.enabled=True timing.ipynb

docs: README.md timing

## Run pytests
.PHONY: test
test:
	pytest

test2: reqs test


## Make README 
.PHONY: README.md
README.md: README.qmd src/showstats/showstats.py
	quarto render README.qmd

## Run nox
.PHONY: nox
nox: 
	nox

## Build package
.PHONY: build
build: 
	python3 -m build

## Upload to pypi
.PHONY: upload-pypi
upload-pypi: 
	python3 -m twine upload --repository pypi dist/*

## Upload to test-pypi
.PHONY: upload-testpypi
upload-testpypi: 
	python3 -m twine upload --repository testpypi dist/*


## Test install
.PHONY: test-inst
test-inst:
	uv pip install -i https://test.pypi.org/simple/ showstats

# Self Documenting Commands #
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

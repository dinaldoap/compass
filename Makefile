PACKAGE_SRC=$(shell find compass -type f -name '*.py' ! -name 'version.py')
TESTS_SRC=$(shell find tests -type f -name '*.py')
TESTS_DATA=$(shell find tests -type f -name '*.xlsx' -name '*.ini')

main: clean install lock sync format secure lint test package smoke
.PHONY: main

.cache/make/clean:
	rm -rf .cache/make compass.egg-info .pytest_cache tests/.pytest_cache dist
	mkdir --parents .cache/make
	@date > $@
.PHONY: clean
clean: .cache/make/clean

.cache/make/install: .cache/make/clean requirements-dev-editable.txt pyproject.toml requirements-dev.txt constraints.txt
	pip install --quiet --requirement=requirements-dev-editable.txt --requirement=requirements-dev.txt
	@date > $@
.PHONY: install
install: .cache/make/install

requirements-dev.lock: .cache/make/install requirements-dev.txt constraints.txt pyproject.toml requirements-dev-constraints.txt
	pip-compile --quiet --resolver=backtracking --generate-hashes --strip-extras --allow-unsafe --output-file=requirements-dev.lock --no-header --no-annotate requirements-dev.txt pyproject.toml
requirements-prod.lock: requirements-dev.lock pyproject.toml requirements-dev-constraints.txt
	pip-compile --quiet --resolver=backtracking --generate-hashes --strip-extras --allow-unsafe --output-file=requirements-prod.lock --no-header --no-annotate pyproject.toml requirements-dev-constraints.txt
.PHONY: lock
lock: requirements-dev.lock requirements-prod.lock

.PHONY: unlock
unlock:
	rm -rf requirements-*.lock

.cache/make/sync: requirements-dev-editable.txt pyproject.toml requirements-dev.lock
	pip-sync --quiet requirements-dev.lock
	pip install --quiet --requirement=requirements-dev-editable.txt
	@date > $@
.PHONY: sync
sync: .cache/make/sync

.cache/make/format: .cache/make/sync ${PACKAGE_SRC} ${TESTS_SRC}
	isort --profile black compass tests
	black compass tests
	docformatter --in-place --recursive compass tests
	@date > $@
.PHONY: format
format: .cache/make/format

.cache/make/pip-audit: .cache/make/sync requirements-prod.lock
	pip-audit --cache-dir=${HOME}/.cache/pip-audit --requirement=requirements-prod.lock
	@date > $@
.cache/make/bandit: .cache/make/sync ${PACKAGE_SRC}
	bandit --recursive compass
	@date > $@
.PHONY: secure
secure: .cache/make/pip-audit .cache/make/bandit

.cache/make/lint: .cache/make/sync ${PACKAGE_SRC} .pylintrc
	pylint compass
	@date > $@
.PHONY: lint
lint: .cache/make/lint

.cache/make/test: .cache/make/sync ${PACKAGE_SRC} ${TESTS_SRC} ${TESTS_DATA}
	pytest --cov=compass --cov-report=term-missing tests
	@date > $@
.PHONY: test
test: .cache/make/test
	
.cache/make/package: .cache/make/sync ${PACKAGE_SRC} pyproject.toml
	rm -rf dist/
	python -m build
	@date > $@
.PHONY: package
package: .cache/make/package

.cache/make/smoke: .cache/make/package
	pip install --quiet dist/*.whl
	compass --help
	compass --version
	pip install --quiet --requirement=requirements-dev-editable.txt
	@date > $@
.PHONY: smoke
smoke: .cache/make/smoke

.PHONY: venv
venv:
	bash make/venv.sh

.PHONY: bash
bash:
	bash .devcontainer/bash.sh

.PHONY: devcontainer
devcontainer:
	bash .devcontainer/devcontainer.sh

.PHONY: testpypi
testpypi:
	twine upload --repository testpypi dist/*.whl

.PHONY: cookie
cookie:
	cookiecutter --overwrite-if-exists --output-dir=.. --no-input --config-file=cookiecutter.yaml $$(cookiecutter-python-vscode-github)

.PHONY: prettier
prettier:
	prettier . --write

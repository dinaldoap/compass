PACKAGE_SRC=$(shell find compass -type f -name '*.py')
PACKAGE_CFG=pyproject.toml setup.cfg
TESTS_SRC=$(shell find tests -type f -name '*.py')
TESTS_DATA=$(shell find tests -type f -name '*.xlsx' -name '*.ini')

main: clean build
.PHONY: main

.PHONY: clean
clean:
	rm -rf compass.egg-info build dist

.PHONY: build
build: install lock sync format secure lint test package smoke

build/setup:
	mkdir --parents build
	@date > $@

build/install: requirements-editable.txt ${PACKAGE_CFG} requirements-dev.txt constraints.txt build/setup
	pip install --quiet --requirement=requirements-editable.txt --requirement=requirements-dev.txt
	@date > $@
.PHONY: install
install: build/install

build/lock: requirements-dev.txt constraints.txt ${PACKAGE_CFG} requirements-bridge.txt build/install
	pip-compile --quiet --resolver=backtracking --generate-hashes --strip-extras --output-file=requirements-dev.lock --no-header --no-annotate requirements-dev.txt pyproject.toml
	pip-compile --quiet --resolver=backtracking --generate-hashes --strip-extras --output-file=requirements-prod.lock --no-header --no-annotate pyproject.toml requirements-bridge.txt
	@date > $@
.PHONY: lock
lock: build/lock

.PHONY: unlock
unlock:
	rm --force requirements-*.lock

build/sync: requirements-editable.txt ${PACKAGE_CFG} requirements-dev.lock build/lock
	pip-sync --quiet requirements-dev.lock
	pip install --quiet --requirement=requirements-editable.txt
	@date > $@
.PHONY: sync
sync: build/sync

build/format: ${PACKAGE_SRC} ${TESTS_SRC} build/sync
	isort --profile black compass tests
	black compass tests
	docformatter --in-place --recursive compass tests
	@date > $@
.PHONY: format
format: build/format

build/pip-audit: build/sync
	pip-audit --cache-dir=${HOME}/.cache/pip-audit --requirement=requirements-prod.lock
	@date > $@
build/bandit: ${PACKAGE_SRC} build/sync
	bandit --recursive compass
	@date > $@
.PHONY: secure
secure: build/pip-audit build/bandit

build/lint: ${PACKAGE_SRC} .pylintrc build/sync
	pylint compass
	@date > $@
.PHONY: lint
lint: build/lint

build/test: ${PACKAGE_SRC} ${TESTS_SRC} ${TESTS_DATA} build/sync
	pytest --cov=compass --cov-report=term-missing tests
	@date > $@
.PHONY: test
test: build/test
	
build/package: ${PACKAGE_SRC} ${PACKAGE_CFG} build/sync
	python -m build
	@date > $@
.PHONY: package
package: build/package

build/smoke: build/package
#	./dist/compass --help
	pip install --quiet dist/compass*.whl
	compass --help
	pip install --quiet --requirement=requirements-editable.txt
	@date > $@
.PHONY: smoke
smoke: build/smoke

.PHONY: venv
venv:
	bash make/venv.sh

.PHONY: venv-init
venv-init:
	bash make/venv-init.sh

.PHONY: docker
docker:
	bash .devcontainer/devcontainer.sh
PACKAGE_SRC=$(shell find compass -type f -name '*.py')
PACKAGE_CFG=pyproject.toml
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

build/install: build/setup requirements-editable.txt ${PACKAGE_CFG} requirements-dev.txt constraints.txt
	pip install --quiet --requirement=requirements-editable.txt --requirement=requirements-dev.txt
	@date > $@
.PHONY: install
install: build/install

build/lock: build/install requirements-dev.txt constraints.txt ${PACKAGE_CFG} requirements-bridge.txt
	pip-compile --quiet --resolver=backtracking --generate-hashes --strip-extras --output-file=requirements-dev.lock --no-header --no-annotate requirements-dev.txt pyproject.toml
	pip-compile --quiet --resolver=backtracking --generate-hashes --strip-extras --output-file=requirements-prod.lock --no-header --no-annotate pyproject.toml requirements-bridge.txt
	@date > $@
.PHONY: lock
lock: build/lock

.PHONY: unlock
unlock:
	rm --force requirements-*.lock

build/sync: build/lock requirements-editable.txt ${PACKAGE_CFG} requirements-dev.lock
	pip-sync --quiet requirements-dev.lock
	pip install --quiet --requirement=requirements-editable.txt
	@date > $@
.PHONY: sync
sync: build/sync

build/format: build/sync ${PACKAGE_SRC} ${TESTS_SRC}
	isort --profile black compass tests
	black compass tests
	docformatter --in-place --recursive compass tests
	@date > $@
.PHONY: format
format: build/format

build/pip-audit: build/sync
	pip-audit --cache-dir=${HOME}/.cache/pip-audit --requirement=requirements-prod.lock
	@date > $@
build/bandit: build/sync ${PACKAGE_SRC}
	bandit --recursive compass
	@date > $@
.PHONY: secure
secure: build/pip-audit build/bandit

build/lint: build/sync ${PACKAGE_SRC} .pylintrc
	pylint compass
	@date > $@
.PHONY: lint
lint: build/lint

build/test: build/sync ${PACKAGE_SRC} ${TESTS_SRC} ${TESTS_DATA}
	pytest --cov=compass --cov-report=term-missing tests
	@date > $@
.PHONY: test
test: build/test
	
build/package: build/sync ${PACKAGE_SRC} ${PACKAGE_CFG}
	rm -rf dist/
	python -m build
	@date > $@
.PHONY: package
package: build/package

build/smoke: build/package
	pip install --quiet dist/compass_investor*.whl
	compass --help
	compass --version
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

.PHONY: testpypi
testpypi:
	twine upload --repository testpypi dist/compass*.whl
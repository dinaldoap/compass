main: clean smoke
.PHONY: main

.PHONY: clean
clean:
	rm -rf compass.egg-info build dist

build/setup:
	mkdir --parents build
	@date > $@

build/install: requirements-editable.txt pyproject.toml requirements-dev.txt constraints.txt build/setup
	pip install --quiet --requirement=requirements-editable.txt --requirement=requirements-dev.txt
	@date > $@
.PHONY: install
install: build/install

build/lock: requirements-dev.txt constraints.txt pyproject.toml requirements-bridge.txt build/install
	pip-compile --quiet --strip-extras --output-file=requirements-dev.lock --no-header --no-annotate requirements-dev.txt pyproject.toml
	pip-compile --quiet --strip-extras --output-file=requirements-prod.lock --no-header --no-annotate pyproject.toml requirements-bridge.txt
	@date > $@
.PHONY: lock
lock: build/lock

.PHONY: unlock
unlock:
	rm requirements-*.lock

build/sync: requirements-editable.txt pyproject.toml requirements-dev.lock build/lock
	pip-sync --quiet requirements-editable.txt requirements-dev.lock
	@date > $@
.PHONY: sync
sync: build/sync

PACKAGE_SRC=$(shell find compass -type f -name '*.py')
TESTS_SRC=$(shell find tests -type f -name '*.py')
TESTS_DATA=$(shell find tests -type f -name '*.xlsx' -name '*.ini')
build/format: $(PACKAGE_SRC) $(TESTS_SRC) build/sync
	isort --profile black compass tests
	black compass tests
	docformatter --in-place --recursive compass tests
	@date > $@
.PHONY: format
format: build/format

build/pip-audit: build/sync
	pip-audit --ignore-vuln GHSA-hcpj-qp55-gfph
	@date > $@
build/bandit: $(PACKAGE_SRC) build/sync
	bandit --recursive compass
	@date > $@
.PHONY: secure
secure: build/bandit

build/lint: $(PACKAGE_SRC) build/sync
	pylint compass
	@date > $@
.PHONY: lint
lint: build/lint

build/test: $(PACKAGE_SRC) $(TESTS_SRC) $(TESTS_DATA) build/format build/pip-audit build/bandit build/lint
	pytest --cov=compass --cov-report=term-missing tests
	@date > $@
.PHONY: test
test: build/test
	
build/package: $(PACKAGE_SRC) pyproject.toml build/sync
	python -m build
	@date > $@
.PHONY: package
package: build/package

build/smoke: build/test build/package
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
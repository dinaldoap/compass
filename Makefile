main: clean install lock sync format secure lint test package smoke
.PHONY: main

.PHONY: clean
clean:
	rm -rf compass.egg-info build dist

build/install: requirements-editable.txt pyproject.toml requirements-dev.txt constraints.txt
	pip install --quiet --requirement=requirements-editable.txt --requirement=requirements-dev.txt
	mkdir --parents build
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

.PHONY: format
format: build/sync
	isort --profile black compass tests
	black compass tests
	docformatter --in-place --recursive compass tests

build/pip-audit: build/sync
	pip-audit --ignore-vuln GHSA-hcpj-qp55-gfph
	@date > $@
.PHONY: secure
secure: build/pip-audit format
	bandit --recursive compass

.PHONY: lint
lint: format
	pylint compass
	
.PHONY: test
test: secure lint
	pytest --cov=compass --cov-report=term-missing tests
	
.PHONY: package
package: test
	python -m build

.PHONY: smoke
smoke: package
#	./dist/compass --help
	pip install --quiet dist/compass*.whl
	compass --help
	pip install --quiet --requirement=requirements-editable.txt

.PHONY: venv
venv:
	bash make/venv.sh

.PHONY: venv-init
venv-init:
	bash make/venv-init.sh

.PHONY: docker
docker:
	bash .devcontainer/devcontainer.sh
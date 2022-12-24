main: clean install lock sync format secure lint test package run

clean:
	rm -rf compass.egg-info build dist

install:
	pip install --quiet --requirement=requirements-editable.txt --requirement=requirements-dev.txt

lock:
	pip-compile --quiet --strip-extras --output-file=requirements-dev.lock --no-header --no-annotate requirements-dev.txt setup.py
	pip-compile --quiet --strip-extras --output-file=requirements-prod.lock --no-header --no-annotate setup.py requirements-bridge.txt

unlock:
	rm requirements-*.lock

sync:
	pip-sync --quiet requirements-editable.txt requirements-dev.lock

format:
	isort --profile black compass tests setup.py
	black compass setup.py tests
	docformatter --in-place --recursive compass tests setup.py

secure:
	pip-audit --ignore-vuln GHSA-hcpj-qp55-gfph
	bandit --recursive compass setup.py

lint:
	pylint compass setup.py

test: 
	pytest --cov=compass --cov-report=term-missing tests

package:
	python -m build

run:
#	./dist/compass --help
	pip install --quiet dist/compass*.whl
	compass --help
	pip install --quiet --requirement=requirements-dev.txt

venv:
	bash make/venv.sh

venv-init:
	bash make/venv-init.sh

docker:
	bash .devcontainer/devcontainer.sh
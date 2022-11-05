main: clean install lock sync format secure test package run

clean:
	rm -rf compass.egg-info build dist

install:
	pip install --quiet --requirement=requirements-dev.txt

lock:
	pip-compile --quiet --strip-extras --output-file=requirements-prod.lock --no-header --no-annotate requirements-prod.txt
	pip-compile --quiet --strip-extras --output-file=requirements-dev.lock --no-header --no-annotate requirements-dev.txt

unlock:
	rm requirements-*.lock

sync:
	pip-sync --quiet requirements-dev.lock

format:
	isort --profile black compass tests setup.py
	black compass setup.py tests
	docformatter --in-place --recursive compass tests setup.py

secure:
	pip-audit
	bandit --recursive compass

test: 
	pytest --cov=compass --cov-report=term-missing tests

package:
	bash package.sh

run:
#	./dist/compass --help
	pip install --quiet dist/compass*.whl
	compass --help
	pip install --quiet --requirement=requirements-dev.txt

venv:
	rm -rf .venv
	python -m venv .venv

docker:
	bash .devcontainer/devcontainer.sh
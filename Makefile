main: clean install format test package run

clean:
	rm -rf compass.egg-info build dist

format:
	black compass setup.py tests

install:
	pip-sync --quiet requirements.lock

test: 
	pytest --cov=compass --cov-report=term-missing tests

package:
	bash package.sh

run:
#	./dist/compass --help
	pip install --quiet dist/compass*.whl
	compass --help
	pip install --quiet -r requirements.txt

init:
	conda env update --file conda.yml --prune

lock:
	pip-compile --quiet --strip-extras --output-file=requirements-prod.lock --no-header --no-annotate requirements-prod.txt
	pip-compile --quiet --strip-extras --output-file=requirements.lock --no-header requirements.txt
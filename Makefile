main: clean install lock sync format test package run

clean:
	rm -rf compass.egg-info build dist

format:
	black compass setup.py tests

install:
	pip install --quiet --requirement=requirements-dev.txt

lock:
	pip-compile --quiet --strip-extras --output-file=requirements-prod.lock --no-header --no-annotate requirements-prod.txt
	pip-compile --quiet --strip-extras --output-file=requirements-dev.lock --no-header --no-annotate requirements-dev.txt

sync:
	pip-sync --quiet requirements-dev.lock

test: 
	pytest --cov=compass --cov-report=term-missing tests

package:
	bash package.sh

run:
#	./dist/compass --help
	pip install --quiet dist/compass*.whl
	compass --help
	pip install --quiet --requirement=requirements-dev.txt

conda:
	conda env update --file conda.yml --prune

build: clean format install test package run

clean:
	rm -rf compass.egg-info

format:
	black compass setup.py tests

install:
	pip install --quiet -r requirements.txt

test: 
	pytest tests

package:
	bash package.sh

run:
	./dist/compass --help
	pip install --quiet dist/compass-0.1.0-py2.py3-none-any.whl
	compass --help
	pip install --quiet -r requirements.txt

init:
	conda env update --file conda.yml --prune
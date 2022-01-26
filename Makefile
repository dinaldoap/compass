build: clean format install test package run

clean:
	rm -rf compass.egg-info build dist

format:
	black compass setup.py tests

install:
	pip install --quiet -r requirements.txt

test: 
	pytest tests

package:
	bash package.sh

run:
#	./dist/compass --help
	pip install --quiet dist/compass*.whl
	compass --help
	pip install --quiet -r requirements.txt

init:
	conda env update --file conda.yml --prune
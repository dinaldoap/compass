build: clean format install test package run

clean:
	rm -rf compass.egg-info

format:
	autopep8 --in-place --recursive compass setup.py

install:
	pip install -r requirements.txt

test: 
	pytest tests

package:
	bash package.sh

run:
	./dist/compass --help
build: clean format install test

clean:
	rm -rf compass.egg-info

format:
	autopep8 --in-place --recursive compass setup.py

install:
	pip install -r requirements.txt

test: 
	pytest tests

run:
	compass
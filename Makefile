build: clean format test

clean:

format:
	autopep8 --in-place --recursive compass setup.py

test: 
	pytest tests

run:
	compass
build: clean format test

clean:

format:
	autopep8 --in-place --recursive template setup.py

test: 
	pytest tests

run:
	template
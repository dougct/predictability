.PHONY: test install

test:
	python -m pytest tests.py

install:
	python setup.py install

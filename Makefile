init:
	python setup.py install

test:
	nosetests --rednose --with-coverage --cover-erase --cover-package=opentsdb_importer tests

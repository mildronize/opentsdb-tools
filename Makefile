develop:
	python setup.py develop

test:
	nosetests --rednose --with-coverage --cover-erase --cover-package=opentsdb_importer opentsdb_importer/tests/*

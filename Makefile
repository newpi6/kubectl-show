upload:
	rm -rf dist kubectl_show.egg-info ;
	python setup.py sdist;
	python3 -m twine upload dist/*.gz --verbose
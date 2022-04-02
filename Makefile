clean:
	rm -rf dist kubectl_show.egg-info build;

upload:
	rm -rf dist kubectl_show.egg-info ;
	python3 setup.py sdist;
	python3 -m twine upload dist/*.gz --verbose

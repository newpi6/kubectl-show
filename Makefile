clean:
	rm -rf dist kubectl_show.egg-info build;

upload:
	rm -rf dist kubectl_show.egg-info ;
	python3 setup.py sdist bdist_wheel;
	python3 -m twine upload dist/{*.gz,*.whl} --verbose

upload-test:
	rm -rf dist kubectl_show.egg-info ;
	python3 setup.py sdist bdist_wheel;
	python3 -m twine  upload -r testpypi dist/{*.gz,*.whl} --verbose
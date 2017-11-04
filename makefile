.PHONY: dist upload bump

dist:
	@ python setup.py sdist
	@ rm -r testindicator.egg-info

upload:
	@ twine upload dist/$(shell ls dist/ -1 | tail -n 1)

bump:
	@ ./bump_version

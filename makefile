.PHONY: dist

dist:
	@ python setup.py sdist
	#@ mv ./dist/*.egg ./dist/eggs/

deploy:
	#LATEST=$(shell ls -t1 dist/ | head -n 1)
	#@ ls -t1 dist/ | head -n 1
	#ARCHIVE := $(shell ls dist/ -1 | tail -n 1)
	#@echo UPLOADING $(ARCHIVE)
	@ twine upload dist/$(FILE)

#all:
	#@ FILE=$(shell ls dist/ -1 | tail -n 1)
#	@ echo "uploading " $(FILE))
	#@echo $(LATEST)
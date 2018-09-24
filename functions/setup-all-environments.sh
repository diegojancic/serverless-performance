#!/bin/bash
set -x

export initialDir=$PWD
# Remove existent environments

cd ./chalice/ && \
	rm -f -r ./env/ && \
	virtualenv env && \
	source env/bin/activate && \
	pip install -r requirements.txt && \
	deactivate

cd $initialDir

cd ./chalice/extras1/ && \
	rm -f -r ./env/ && \
	virtualenv env && \
	source env/bin/activate && \
	pip install -r requirements.txt && \
	deactivate

cd $initialDir

cd ./zappa-django/ && \
	rm -f -r ./env/ && \
	virtualenv env && \
	source env/bin/activate && \
	pip install -r requirements.txt && \
	deactivate

cd $initialDir

cd ./zappa-flask/ && \
	rm -f -r ./env/ && \
	virtualenv env && \
	source env/bin/activate && \
	pip install -r requirements.txt && \
	deactivate



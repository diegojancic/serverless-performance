#!/bin/bash
set -x

export initialDir=$PWD
# Remove existent environments

cd ./chalice/ && \
	source env/bin/activate && \
	cd base && \
	chalice delete && \
	deactivate

cd $initialDir

cd ./chalice/ && \
	source env/bin/activate && \
	cd extras1 && \
	chalice delete && \
	deactivate

cd $initialDir

cd ./zappa-django/ && \
	source env/bin/activate && \
	zappa undeploy && \
	deactivate

cd $initialDir

cd ./zappa-flask/ && \
	source env/bin/activate && \
	zappa undeploy && \
	deactivate



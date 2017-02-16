all: test clean package

codegen:
	protoc -I=./protobuf --python_out=./metronome/models/ ./protobuf/metronome.proto

itests: codegen
	tox -e itest-py27
	tox -e itest-py33

test: codegen
	tox -e pep8
	tox -e test-py27
	tox -e test-py33

clean:
	rm -rf dist/ build/

package: clean
	pip install wheel
	python setup.py sdist bdist_wheel

publish: package
	pip install twine
	twine upload dist/*

.PHONY: codegen itests test clean package publish

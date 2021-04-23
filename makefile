# build everything
all: test deployment

# build the LaiNES CPP code
lib_ntsc:
	scons -C ntsc_py/ntsc
	mv ntsc_py/ntsc/lib_ntsc*.so ntsc_py

# run the Python test suite
test: lib_ntsc
	python3 -m unittest discover .

# clean the build directory
clean:
	rm -rf build/ dist/ .eggs/ *.egg-info/ || true
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name ".sconsign.dblite" -delete
	find . -name "build" | rm -rf
	find . -name "lib_ntsc.so" -delete

# build the deployment package
deployment: clean
	python3 setup.py sdist bdist_wheel

# ship the deployment package to PyPi
ship: test deployment
	twine upload dist/*

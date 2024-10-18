#!make
compile:
	pyinstaller --clean compiler.spec

compiler_dev:
	pyinstaller --clean compiler_dev.spec -y

#!make
prod:
	pyinstaller --clean compiler.spec -y

dev:
	pyinstaller --clean compiler_dev.spec -y


tr:
	./timer_app/i18nget.sh > rawtrads.txt
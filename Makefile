#!/usr/bin/make -f

all: build

build:
	python setup.py build

install: build
	sudo python setup.py install

uninstall:
	sudo rm -vrf /usr/lib/python2.5/site-packages/gstmanager
	sudo rm -v /usr/lib/python2.5/site-packages/gstmanager*.egg-info

clean:
	rm -vrf build

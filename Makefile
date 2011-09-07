#
# A basic Makefile for sshfp
#

BIN     = $(DESTDIR)/usr/bin
MAN     = $(DESTDIR)/usr/share/man/man1

all: man daneldnsx
	
install:
	install -m 0755 -d $(BIN)
	install -m 0755 sshfp $(BIN)
	install -m 0755 dane $(BIN)
	install -m 0755 -d $(MAN)
	install -m 0644 sshfp.1 $(MAN)
	install -m 0644 dane.1 $(MAN)
	python -mcompileall daneldnsx.py
	gzip $(MAN)/sshfp.1
	gzip $(MAN)/dane.1

sshfp.1: sshfp.1.xml
	xmlto man sshfp.1.xml

dane.1: dane.1.xml
	xmlto man dane.1.xml

daneldnsx:
	python -mcompileall daneldnsx.py
	
man:	man-page
man-page: sshfp.1 dane.1

clean:
	-rm -f sshfp.1 dane.1 daneldnsx.pyc

dist-clean:
	@echo Nothing to dist-clean - This is a python script

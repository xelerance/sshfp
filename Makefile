#
# A basic Makefile for sshfp
# by Jacob Appelbaum <jacob@appelbaum.net>
#
#

BIN     = $(DESTDIR)/usr/bin
MAN     = $(DESTDIR)/usr/share/man/man1

build:
	@echo Nothing to build - This is a python script

install:
	install -d $(BIN)
	install sshfp $(BIN)
	install -d $(MAN)
	install sshfp.1 $(MAN)

clean:
	@echo Nothing to clean - This is a python script
dist-clean:
	@echo Nothing to dist-clean - This is a python script

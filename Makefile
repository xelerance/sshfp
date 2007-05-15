#
# A basic Makefile for sshfp
# by Jacob Appelbaum <jacob@appelbaum.net>
#
#

BIN     = $(DESTDIR)/usr/bin
MAN     = $(DESTDIR)/usr/share/man/man1

all: man-page
	
install:
	install -d 0755 $(BIN)
	install -m 0755 sshfp $(BIN)
	install -d 0755 $(MAN)
	install -m 0644 sshfp.1 $(MAN)
	gzip $(MAN)/sshfp.1

man-page:
	nroff -man sshfp.1 > sshfp.1.txt

clean:
	rm sshfp.1.txt

dist-clean:
	@echo Nothing to dist-clean - This is a python script

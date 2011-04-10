#
# A basic Makefile for sshfp
#

BIN     = $(DESTDIR)/usr/bin
MAN     = $(DESTDIR)/usr/share/man/man1

all: man
	
install:
	install -m 0755 -d $(BIN)
	install -m 0755 sshfp $(BIN)
	install -m 0755 -d $(MAN)
	install -m 0644 sshfp.1 $(MAN)
	gzip $(MAN)/sshfp.1

sshfp.1: sshfp.1.xml
	xmlto man sshfp.1.xml

man:	man-page
man-page: sshfp.1

clean:
	-rm -f sshfp.1

dist-clean:
	@echo Nothing to dist-clean - This is a python script

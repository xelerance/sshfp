#
# A basic Makefile for sshfp
# by Jacob Appelbaum <jacob@appelbaum.net>
#
#

BIN     = $(DESTDIR)/usr/bin
MAN     = $(DESTDIR)/usr/share/man/man1

install:
        install -d $(BIN)
        install sshfp $(BIN)
        install -d $(MAN)
        install sshfp.1 $(MAN)
clean:
        -rm out
dist-clean:
        @echo Nothing to dist-clean - This is a python script

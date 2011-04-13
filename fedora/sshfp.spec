Summary: Generate RFC-4255 SSHFP DNS records from knownhosts files or ssh-keyscan
Name: sshfp
Version: 1.2.0
Release: 1%{?dist}
License: GPL
Url:  http://www.xelerance.com/software/%{name}/
Source: ftp://ftp.xelerance.com/%{name}/%{name}-%{version}.tar.gz
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#Only to regenerate the man page
#Buildrequires: xmlto
Requires: python-dns, openssh-clients >= 4, python-argparse
BuildArch: noarch

%description
sshfp generates DNS SSHFP records from SSH public keys. sshfp can take
public keys from a knownhosts file or from scanning the host's sshd daemon.
The ssh client can use these SSHFP records if you set "VerifyHostKeyDNS yes"
in the file /etc/ssh/ssh_config or in your .ssh/config. See RFC-4255

%prep
%setup -q 

%build
make all

%install
rm -rf ${RPM_BUILD_ROOT}
export DESTDIR=${RPM_BUILD_ROOT}
make install

%clean
rm -rf ${RPM_BUILD_ROOT}

%files 
%defattr(-,root,root)
%doc BUGS CHANGES README COPYING
%{_bindir}/*
%doc %{_mandir}/man1/*

%changelog
* Tue Apr 12 2011 Paul Wouters <paul@xelerance.com> - 1.2.0-1
- Released 1.2.0.
- Added the dane command

* Wed Oct 13 2010 Paul Wouters <paul@xelerance.com> - 1.1.6-1
- Upgraded to 1.1.6

* Thu Apr 19 2007 Paul Wouters <paul@xelerance.com> - 1.1.3-1
- Upgraded to 1.1.3

* Wed Oct  4 2006 Paul Wouters <paul@xelerance.com> - 1.1.1-1
- Upgraded to 1.1.1

* Tue Sep 26 2006 Paul Wouters <paul@xelerance.com> - 1.1.0-1
- Mistakingly ran the sha1() call on the uuencoded keyblob, which
  generated wrong SSHFP records.

* Mon Sep 25 2006 Paul Wouters <paul@xelerance.com> - 1.0.6-2
- Don't change VerifyHostKeyDNS in /etc/ssh/ssh_config anymore

* Tue Sep 19 2006 Paul Wouters <paul@xelerance.com> - 1.0.6-1
- Initial release for Fedora Extras

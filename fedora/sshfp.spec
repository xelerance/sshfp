Summary: Generate SSHFP DNS records from knownhosts files or ssh-keyscan
Name: sshfp
Version: 1.1.1
Release: 1%{?dist}
License: GPL
Url:  ftp://ftp.xelerance.com/%{name}/
Source: ftp://ftp.xelerance.com/%{name}/%{name}-%{version}.tar.gz
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: python-dns, openssh-clients >= 4
BuildArch: noarch

%description
sshfp generates DNS SSHFP records from SSH public keys. sshfp can take
public keys from a knownhosts file or from scanning the host's sshd daemon.
The ssh client can use these SSHFP records if you set "VerifyHostKeyDNS yes"
in the file /etc/ssh/ssh_config.
enable this per default.

%prep
%setup -q 

%build

%install
rm -rf ${RPM_BUILD_ROOT}
install -d 0755 ${RPM_BUILD_ROOT}%{_bindir} 
install -d 0755 ${RPM_BUILD_ROOT}%{_mandir}/man1
install -m 0755 sshfp ${RPM_BUILD_ROOT}%{_bindir}
install -m 0644 sshfp.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/
gzip ${RPM_BUILD_ROOT}%{_mandir}/man1/sshfp.1

%clean
rm -rf ${RPM_BUILD_ROOT}

%files 
%defattr(-,root,root)
%doc BUGS CHANGES README COPYING
%{_bindir}/*
%doc %{_mandir}/man1/*

%changelog
* Wed Oct  4 2006 Paul Wouters <paul@xelerance.com> - 1.1.1-1
- Upgraded to 1.1.1

* Tue Sep 26 2006 Paul Wouters <paul@xelerance.com> - 1.1.0-1
- Mistakingly ran the sha1() call on the uuencoded keyblob, which
  generated wrong SSHFP records.

* Mon Sep 25 2006 Paul Wouters <paul@xelerance.com> - 1.0.6-2
- Don't change VerifyHostKeyDNS in /etc/ssh/ssh_config anymore

* Tue Sep 19 2006 Paul Wouters <paul@xelerance.com> - 1.0.6-1
- Initial release for Fedora Extras

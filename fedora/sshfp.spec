Summary: Generate SSHFP DNS records from knownhosts files or ssh-keyscan
Name: sshfp
Version: 1.0.6
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
in the file /etc/ssh/ssh_config. I have not managed to convince RedHat to
enable this per default. This package enables VerifyHostKeyDNS.

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

%post
if [ -e /etc/ssh/ssh_config ]; then
        grep VerifyHostKeyDNS /etc/ssh/ssh_config > /dev/null
        RETVAL=$?
        if [ $RETVAL -ne 0 ]; then
                echo 'VerifyHostKeyDNS        yes' >> /etc/ssh/ssh_config
        fi
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files 
%defattr(-,root,root)
%doc BUGS CHANGES README COPYING
%{_bindir}/*
%doc %{_mandir}/man1/*

%changelog
* Tue Sep 19 2006 Paul Wouters <paul@xelerance.com> - 1.0.6-1
- Initial release for Fedora Extras

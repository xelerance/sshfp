# Origin

```
Software	: sshfp
URL		    : http://www.xelerance.com/software/sshfp/
Source		: ftp://ftp.xelerance.com/sshfp/
License		: GPLv2+
Mailinglist	: http://lists.xelerance.com/mailman/listinfo/sshfp/
Authors		: Paul Wouters, Chrisopher Olah
Summary		: Generate RFC-4255 SSHFP DNS records from known_hosts files or ssh-keyscan
```

sshfp generates DNS SSHFP records from SSH public keys. sshfp can take
public keys from a known_hosts file or from scanning the host's sshd daemon.
The ssh client can use these SSHFP records if you set "VerifyHostKeyDNS yes"
in the file /etc/ssh/ssh_config or ~/.ssh/config. See RFC-4255

# Differences from upstream

This fork has the following additional features implemented:

- IPv6 AAAA host lookups
- Support for multiple ports to be listed on the CLI
- Regex filtering of included hosts
- Only output unique results

These are only tested when using the AFXR method and not the known_hosts file.

# Requirements

sshfp requires python-dns: http://www.pythondns.org

```
pip install dnspython
```

# Quickstart

## On OSX

```
git clone git@github.com:jinnko/sshfp.git
cd sshfp
virtualenv -p python2.7 ./
bin/pip install dnspython
bin/python sshfp --port 22 --port 2022 --scan --all-hosts --regex '^(aws|do|gce)' example.com
```
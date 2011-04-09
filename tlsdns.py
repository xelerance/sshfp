#!/usr/bin/python
#
# tlsdns is a tool to generate and verify HASTLS and TLSA records
# By Paul Wouters <paul@xelerance.com> 
# Copyright 2010-2011 by Xelerance http://www.xelerance.com/
# License: GNU GENERAL PUBLIC LICENSE Version 2

import os
import sys
import getopt
import base64
import time
import socket
# We want ldns for AD flag support - maybe we will add libunbound later to not need to depend on
# DNSSEC capable resolver in /etc/resolv.conf
try:
	import ldns
except ImportError:
	print "dnstls requires the ldns-python sub-package from http://www.nlnetlabs.nl/projects/ldns/"
	print "Fedora: yum install ldns-python"
	print "Debian: apt-get install python-ldns"
	sys.exit()

# crypto stuff to do minimal TLS to get server certs
import ssl

# hashing functions depend on python version used - 
try:
	import hashlib
	digest = hashlib.sha1
except ImportError:
	import sha
	digest = sha.new

try:
	from subprocess import Popen, PIPE
	use_subprocess = True
except ImportError:
	use_subprocess = False

def usage():
	"""Print usage information"""

	print "usage: dnstls -raw -hastls -tlsa [--without-fallback|--with-fallback] -h <hostname> [ <hostname> ...] [-a <alias [<alias> ...]] --services <service> [ <service> ...]"
	
	print "Defaults are to generate only for https, and no fallback"
	print ""
	print "examples:"
	print "          dnstls www.xelerance.com (hastls and tlsa, no fallback, https only)"
	print "          dnstls --with-fallback --service smtp --service http --withoutfallback www.xelerance.com"
	print "		 (smtp may be plaintext, http not)"
	print " -raw is used to generate HASTLS/TLSA records in 'generic record' form for use on older nameservers"
	print " -probe will check for services on host - currently only checks SMTP/STARTTLS/HTTP/HTTPS"
	print " -verify will check HASTLS for 'lies' and TLSA to be the right cert as found on the server's services"


def create_txt(hostname, pubkey):
	""" Kaminsky / Gilmore type TLS pubkey in TXT RRtype """

def create_hastls(hostname, fallback_default, services):
	""" Creates a HASTLS RRtype """

def create_tlsa(hostname, certtype, hashtype, certblob):
	"""Creates a TLSA RRtype"""

	# https://datatracker.ietf.org/doc/draft-ietf-dane-protocol/?include_text=1
	# IN TLSA <certtype> <hashtype> <cert|hash>
	#
	# certtype can be 
	# 1 -- Hash of an end-entity certificate
	# 2 -- Full end-entity certificate
	# 3 -- Hash of an certification authority's certificate
	# 4 -- Full certification authority's certificate

	# hash type : http://www.iana.org/assignments/tls-parameters
	# eg 2 = sha1
	# hastype = 0 for cert type 2 and 4
	# recommended: use same hash type here as in the Cert signature 

	rawkey = base64.b64decode(keyblob)
	return rawkey

def ldnsLookups(hostname):
	""" get all TLSA/HASTLS/A/AAAA records for hostname """
	if validIP(hostname):
		return hostname
	else:
		# do ldns work, complain if no AD bit
		resolver = ldns.ldns_resolver.new_frm_file("/etc/resolv.conf")
		resolver.set_dnssec(True)
		pkt = resolver.query(name, ldns.LDNS_RR_TYPE_ANY, ldns.LDNS_RR_CLASS_IN)
		if pkt.get_rcode() is ldns.LDNS_RCODE_SERVFAIL:
			print "%s lookup failed (server error or dnssec validation failed)"%name
			print "use -cd to bypass dnssec validation - NOT RECOMMENDED!!"
			sys.exit(1)
		if pkt.get_rcode() is ldns.LDNS_RCODE_NXDOMAIN:
			if pkt.ad():
				confidence = "(non-existence proven by DNSSEC)"
			else:
				confidence = ""
			print "%s lookup failed %s"%(name,confidence)
		# we now have a valid answer, CNAME's got expanded, so we have one or more A/AAAA records
		 
			

def checkExistingTLSA(address):
	""" check if a TLSA record already exists, to compare and notify if update is needed """

def checkExistingHASTLS(address):
	""" check if a HASTLS record already exists, to compare and notify if update is needed """

def validIP(address):
	""" check if valid IP. Returns 0 (no) 4 or 6 """
	try:
		socket.inet_pton(socket.AF_INET,address)
		return 4
	except:
		try:
			socket.inet_pton(socket.AF_INET6,address)
			return 6
		except:
			pass
	return 0

# return the record
def genTLSA(hostname):
	return genTLSAFormat(hostname,sha256Cert(getHTTPSCert(hostname,44)))

# returns PEM encoded EE-cert
def getHTTPSCert(address,port=443):
	""" Get SSL cert from webserver, default port 443 """
	# lookup address with ldns python
	return ssl.get_server_certificate((address,port))

# take PEM encoded EE-cert and DER encode it, then sha256 it
def sha256Cert(certblob):
	hashobj = hashlib.sha256()
	hashobj.update(ssl.PEM_cert_to_DER_cert(certblob))
	return hashobj.hexdigest().upper()

# Output the RRTYPE record
#
def genTLSAFormat(hostname,certhash):
	return "_443._tcp.%s. IN TYPE65468 \# 34 0101%s"%(hostname,certhash)


# to be converted still
def main(argv=None):

	if argv is None:
		argv = sys.argv
	try:
		opts, args = getopt.getopt(argv[1:], "qhdvsT:t:a:o:k:p:", ["quiet", "help", "trailing-dot", "version", "scan", "timeout:", "type:", "all:", "output:", "knownhosts:", "port:"])
	except getopt.error, msg:
		#print >> sys.stderr, err.msg
		print >> sys.stderr, "ERROR parsing options"
		usage()
		sys.exit(2) 

	# parse options
	khfile = ""
	dodns = 0
	dofile = 0
	nameserver = ""
	domain = ""
	output = ""
	quiet = 0
	version = "1.1.5"
	data = ""
	trailing = 0
	timeout = "5"
	algo = "dsa,rsa"
	all_hosts = 0
	port = 22
	hostnames = ()
	#if not opts and not args:
	#	usage()
	#	sys.exit()

	for o, a in opts:
		if o in ("-v", "--version"):
			print "sshfp version: "+version
			print "Authors:\n Paul Wouters <paul@xelerance.com>\n Jake Appelbaum <jacob@appelbaum.net>"
			print "Source : http://www.xelerance.com/software/sshfp/"
			sys.exit()
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		if o in ("-d", "--trailling-dot"):
			trailing = 1
		if o in ("-T", "--timeout"):
			if not a:
				print "error: no timeout specified"
				sys.exit()
			try:
				timeout = str(int(a))
			except:
				print "error: timeout not specified in seconds"
				sys.exit()
		if o in ("-t", "--type"):
			if not a:
				print "error: no type specified"
				sys.exit()
			if (a == "rsa") or (a == "dsa"):
				algo = a
			else:
				print "error: invalid type"
				sys.exit()
		if o in ("-q", "--quiet"):
			quiet = 1
		if o in ("-p", "--port"):
			if a:
				try:
					port = int(a)
					if not quiet and port != 22:
						print "WARNING: non-standard port numbers are not designated in SSHFP records"
				except:
					print "error: port must be a number"
					sys.exit()
		if o in ("-a", "--all"):
			all_hosts = 1
			if a:
				domain = a
		if o in ("-o", "--output"):
			if not a:
				print "error: no output file specified"
				sys.exit()
			else:
				output = a
		if o in ("-k", "--knownhosts"):
			dofile = 1
			# optional arguments dont work cleanly in python??
			if not a:
				khfile = "~/.ssh/known_hosts"
			else:
				if os.path.isfile(a):
					khfile = a 
				else:
					try:
						arec =  getRecord(a, "A")
						if arec:
							# it's really a hostname argument, not a known_hosts file.
							args.append(a)
							khfile = "~/.ssh/known_hosts"
					except:
						# no file and no domain, prob an arg mistaken as option
						if a[0] == "-":
							khfile = "~/.ssh/known_hosts"
							opts.append(a)
							# I guess we can't append opts for processing within
							# the loop. Guess we need to exec a new sshfp or refactor.
							# catch most commonly used options, eg "sshfp -k -a"
							if a == "-a":
								all_hosts = 1
							if a == "-t":
								trailing = 1
						else:
							print "error: "+a+" is neither a known_hosts file or hostname"
							sys.exit()

		if o in ("-s", "--scan"):
			dodns = 1
			# add any args to -s as arguments
			# currently not possible in getopts call
			if (a):
				args.append(a)

		# print "DEBUG: opts"				
		# print opts
		# print "DEBUG: args"				
		# print args

	if (not dodns and not dofile):
		if not args:
			# use default
			all_hosts = 1
			dofile = 1
			trailing = 1
			if not khfile:
				khfile = "~/.ssh/known_hosts"
		else:
			dodns = 1

	if (dodns and dofile):
		print "use either -k or -s"
		usage()
		sys.exit()
		
	if dodns:

		# filter special case for using @nameserver, verify for misinterpreted options as args
		newargs = ""
		for arg in args:
			if arg != "":
				if arg[0] == "@":
					#print "found ns:"+arg[1:]
					nameserver = arg[1:]
					if not all_hosts:
						print "WARNING: ssh-keyscan does not support @nameserver syntax, ignoring"
				else:
					newargs = newargs + arg +" "
				if arg[0] == "-":
					# shit, misinterpreted option as argument. We'll try to be more clever in the future.
					usage()
					sys.exit()
		if not newargs:
			print "error: No hostnames specified"
			sys.exit()
		if all_hosts:
			data = sshfpFromAXFR(newargs, nameserver)
			if not quiet:
				data = ";\n; Generated by sshfp "+ version +" from " + nameserver + " at "+ time.ctime() +"\n;\n" + data
		else:
			data = sshfpFromDNS(newargs)

	if dofile:
		data = sshfpFromFile(khfile, args)

	if not data:
		sys.exit()

	if output:
		try:
			fp = open(output, "w")
		except IOError:
			print "error: can't open '"+output+"' for writing"
			sys.exit()
		else:
			fp.write(data)
			fp.close()
	else:
		print data[:-1]

if __name__ == "__main__":
	sys.exit(main())

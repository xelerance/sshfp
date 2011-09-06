import sys
import binascii
import ssl, socket
import hashlib
import ldnsx
import warnings

secure, transport, quiet, fmt = True, "both", False, "draft"

def create_txt(hostname, pubkey):
	""" Kaminsky / Gilmore type TLS pubkey in TXT RRtype -- testing version"""
	warnings.warn("create_txt is untested...")
	hashobj = hashlib.sha1() #Are there other valid hashes?
	hashobj.update(pubkey) #Should we try and get the pubkey ourselves, like in create_TLSA?
	result = hashobj.hexdigest().upper()
	return "%s IN TXT \"v=key1 ha=sha1 h=%s\"" % (hostname, result)

def create_hastls(hostname, fallback_default, services):
	""" Creates a HASTLS RRtype """

def checkExistingTLSA(hostname, certtype, reftype):
	""" check if a TLSA record already exists, to compare and notify if update is needed 
	    UNTESTED!!!! """
	
	warnings.warn("checkExistingTLSA is untested...")
	res = ldnsx.resolver() #Get the appropriate resource records...
	pkt = res.query(hostname, "TYPE65468", tries = 3)
	pres_TLSAs=set(pkt.answer(rr_type="TYPE65468"))
	pres_TLSAs = map(lambda rr: str(rr).strip(), pres_TLSAs)
	
	TLSAs = set(create_TLSAs(hostname, certtype,reftype).split('\n'))
	
	return TLSAs == pres_TLSAs # are things the same as before?
	

def checkExistingHASTLS(address):
	""" check if a HASTLS record already exists, to compare and notify if update is needed """


def create_tlsa(hostname, certtype, reftype):
	"""Creates a TLSA RRtype"""
	""" get all A/AAAA records for hostname """
	if secure:
		pkt = ldnsx.secure_query(hostname, "ANY", flex=quiet)
	else:
		pkt = ldnsx.query(hostname, "ANY")
	records = pkt.answer( rr_type = { "ipv4":"A",  "ipv6":"AAAA",  "both":"A|AAAA" }[transport] )

	drafts, rfcs = [], []

	for rr in records:
		draft = genTLSA(hostname, rr.ip(), certtype, reftype, draft=True).strip()
		rfc = genTLSA(hostname, rr.ip(), certtype, reftype, draft=False).strip()
		if draft and not (draft in drafts):
			drafts.append(draft)
			rfcs.append(rfc)
	ret = ""
	if not fmt == "rfc":
		ret += "\n".join(drafts)
	if not fmt == "draft":
		ret += "\n".join(rfcs)
	return ret

def genTLSA(hostname, address, certtype, reftype, draft=True):
	dercert = get_cert(hostname, address)
	if certtype != 1:
		raise Exception("Only EE-cert supported right now")
	certhex = hashCert(reftype, dercert)
	if draft:
		# octet length is half of the string length; remember certtype and reftype are part of the length so +2
		return "_443._tcp.%s IN TYPE65468 \# %s 0%s0%s%s"%(hostname, len(certhex)/2+2, certtype, reftype, certhex )
	else:
		return "_443._tcp.%s IN TLSA %s %s %s"%(hostname, certtype, reftype, certhex)

def get_cert(hostname, address):
	# We don't use ssl.get_server_certificate because it does not support IPv6, and it converts DER to PEM, which
	# we would just have to convert back to DER using ssl.PEM_cert_to_DER_cert()
	try:
		# kinda ugly kludge
		if ":" in address:
			conn = socket.socket(socket.AF_INET6)
		else:
			conn = socket.socket(socket.AF_INET)
		conn.connect((address, 443))
	except socket.error as e:
		raise Exception("%s (%s): %s"%(hostname, address, str(e)))
	try:
		sock = ssl.wrap_socket(conn)
	except ssl.SSLError as e:
		raise Exception("%s (%s): %s"%(hostname, address, str(e)))
	dercert = sock.getpeercert(True)
	sock.close()
	conn.close()
	return dercert

# take PEM encoded EE-cert and DER encode it, then sha256 it
def hashCert(reftype,certblob):
	if reftype == 0:
		return binascii.b2a_hex(certblob).upper()
	elif reftype == 1:
		hashobj = hashlib.sha256()
		hashobj.update(certblob)
	elif reftype == 2:
		hashobj = hashlib.sha512()
		hashobj.update(certblob)
	else:
		return 0
	return hashobj.hexdigest().upper()


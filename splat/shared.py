import httplib, re


def getIP(online):
	# This is statement is only used for 
	if online == "0":
		return "localhost"
	try:
		conn = httplib.HTTPConnection("www.showmyip.com")
		conn.request("GET","/")
		r1 = conn.getresponse()
		data1 = r1.read()
		p = re.compile("[\d\+\.]{7,15}")
		results = p.findall(data1)
		ip = results[0]
		return ip
	except:
		return "-1"
		raise

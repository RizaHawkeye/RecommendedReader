import json,httplib

host = "theoldreader.com"
account = "qr2434061@gmai.com"
password = "theoldreader789456"
conn = httplib.HTTPConnection(host,80)

conn.connect()
body = "client=MyAppName&accountType=HOSTED_OR_GOOGLE&service=reader&Email=%s&Passwd=%s&output=json" % (account,password)
url = "reader/api/0/accounts/ClientLogin"
#conn.request(method='POST',url=url,body=body)
conn.request(method='POST',url=url,body=body)
response = conn.getresponse()
#print response.getheaders()
msg = response.read()	
print "msg: " + msg

try:
	result = json.load(msg)
except Exception,e:
	#TODO:toast account or passrowd error
	print e

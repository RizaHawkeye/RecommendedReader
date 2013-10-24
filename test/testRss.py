import json,httplib

host = "theoldreader.com"

conn = httplib.HTTPConnection(host,80)

conn.connect()
body = "client=MyAppName&accountType=HOSTED_OR_GOOGLE&service=reader&Email=%s&Passwd=%s&output=json" % (account,password)
#url = "/reader/api/0/accounts/ClientLogin"
url = "/accounts/ClientLogin"

#TODO:must add "User-Agent" header, or the server will return: "Error=ClientRequired". I know this by analyse the package of curl and httplib
header={}
header['User-Agent'] = "reader"
#header['Content-Type'] = "application"
conn.request(method='POST',url=url,body=body,headers=header)
response = conn.getresponse()
#print response.getheaders()
msg = response.read()	
print "msg: " + msg

try:
	result = json.load(msg)
except Exception,e:
	#TODO:toast account or passrowd error
	print e

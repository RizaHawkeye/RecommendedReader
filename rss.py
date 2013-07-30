__metaclass__=type
import json,httplib

class TheoldreaderRSS:
		#private or public?  __account is private? have try

	def __init__(self,account,password):
		self.__account = account
		self.__password = password
		self.__host = "theoldreader.com"
		#need init self.auth?	

		#conn = httplib.HTTPSConnection()  
		self.conn = HTTPSConnection(self.host,80)
		conn.connect()

	def login(self):
		body = "client=YourAppName&accountType=HOSTED_OR_GOOGLE&service=reader&Email=" + self.account + "&Passwd=" + self.password + "&output=json"
		url = "/accounts/ClientLogin"
		conn.request('POST',url,body)
		
		result = json.load(conn.getresponse().read())

		self.auth = result["Auth"]
		
		if self is not None:
			return true
		else:
			return false
	
	def getUnreadCount(self):
		url = "/reader/api/0/unread-count?output=json"
		headers = "Authorization: GoogleLogin auth=" + self.auth
		conne.request(method='GET',url=url,headers=headers)

		result = json.load(conn.getresponse().read)
		return result["max"]
	

	def getUnreadIds(self,count):
		#TODO:could string plus int in python?
		ulr = "/reader/api/0/stream/items/ids?output=json&s=user/-/state/com.google/reading-list&xt=user/-/state/com.google/read" + "n=" + count
		headers = "Authorization: GoogleLogin auth=" + self.auth
		conn.request(method='GET',url=url,headers=headers)

		ids = []
		result = json.load(conn.getresponse().read)
		unReadcount = len(result["itemRefs"])
		for i in range(0,unReadcount):
			ids.append(result["itemRefs"][i]["id"])

		return ids
	
	def getUnreadContent(self,id):
		url = "/reader/api/0/stream/items/contents?output=json&i=" + id
		headers = "Authorization: GoogleLogin auth=" + self.auth
		conn.request(method='GET',url=url,headers=headers)
		
		result = json.load(conn.getresponse().read)
		
		#title = result["title"]
		title = result["items"][0]["title"]
		content = result["items"][0]["content"]
		href = result["items"][0]["canonical"][0]["href"]
		author = result["items"][0]["author"]
		timestampUsec = result["items"][0]["timestampUsec"]

		return author,title,content,author,timestampUsec

	def close(self):
		#TODO:self.conn.close()
		conn.close()

	

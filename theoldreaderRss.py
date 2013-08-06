__metaclass__=type
import json,httplib
import database
from source import Source

class TheoldreaderRss(Source):
		#private or public?  __account is private? have try

	def __init__(self):
		Source.__init__(self)
		self.__host = "theoldreader.com"
		#need init self.auth?	

		#conn = httplib.HTTPSConnection()  
		self.__conn = httplib.HTTPSConnection(self.__host,80)

		self.__db = database.Database()

	def login(self,account,password):
		self.__conn.connect()
		self.__account = account
		self.__password = password
		body = "client=YourAppName&accountType=HOSTED_OR_GOOGLE&service=reader&Email=" + self.account + "&Passwd=" + self.password + "&output=json"
		url = "/accounts/ClientLogin"
		self.__conn.request('POST',url,body)
		
		result = json.load(conn.getresponse().read())

		self.auth = result["Auth"]
		
		if self is not None:
			website = "theoldreader"
			sql = "insert into Accounts values('" + account + "','" + password + "','" + website + "')"
			self.__db.executeWithoutQuery(sql)
			return True
		else:
			return False
	
	def getUnreadCount(self):
		url = "/reader/api/0/unread-count?output=json"
		headers = "Authorization: GoogleLogin auth=" + self.auth
		self.__conn.request(method='GET',url=url,headers=headers)

		result = json.load(conn.getresponse().read)
		return result["max"]
	

	def getUnreadIds(self,count):
		#TODO:could string plus int in python?
		ulr = "/reader/api/0/stream/items/ids?output=json&s=user/-/state/com.google/reading-list&xt=user/-/state/com.google/read" + "n=" + count
		headers = "Authorization: GoogleLogin auth=" + self.auth
		self.__conn.request(method='GET',url=url,headers=headers)

		ids = []
		result = json.load(conn.getresponse().read)
		unReadcount = len(result["itemRefs"])
		for i in range(0,unReadcount):
			ids.append(result["itemRefs"][i]["id"])

		return ids
	
	def getUnreadContent(self,id):
		url = "/reader/api/0/stream/items/contents?output=json&i=" + id
		headers = "Authorization: GoogleLogin auth=" + self.auth
		self.__conn.request(method='GET',url=url,headers=headers)
		
		result = json.load(conn.getresponse().read)
		
		#title = result["title"]
		title = result["items"][0]["title"]
		content = result["items"][0]["content"]
		href = result["items"][0]["canonical"][0]["href"]
		author = result["items"][0]["author"]
		timestampUsec = result["items"][0]["timestampUsec"]

		sql = "insert into Articals values(\'" + id +  "\',\'" + author + "\',\'" + title + "\'," + content + ",\'" + href + "\',\'" + timestampUsec + "\')"
		
		self.__db.executeWithoutQuery(sql)

	def getAllUnreadContentFromWeb(self):
		unreadCount = getUnreadCount()
		ids = getUnreadIds(unreadCount)

		unreadCountGot = len(ids)
		for id in ids:
			getUnreadContent(i)


	def close(self):
		#TODO:self.conn.close()
		self.__conn.close()
		self.__db.close()


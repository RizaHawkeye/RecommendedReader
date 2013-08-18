__metaclass__=type
import json,httplib
import database
import source
import log
from log import Log
import os

class TheoldreaderRss(source.Source):
		#private or public?  __account is private? have try

	def __init__(self):
		source.Source.__init__(self)
		self.__host = "theoldreader.com"
		#need init self.__auth?	

		#conn = httplib.HTTPSConnection()  
		#TODO : i have to change https to http because https can't connect to the server
		#self.__conn = httplib.HTTPSConnection(self.__host,80)
		self.__conn = httplib.HTTPConnection(self.__host,80)

		self.__db = database.Database()

		self.__errmsg = "Module: %s    Function: %s\n"
	
	
	def login(self,account,password):
		self.__conn.connect()
		self.__account = account
		self.__password = password
		#body = "client=YourAppName&accountType=HOSTED_OR_GOOGLE&service=reader&Email=" + self.account + "&Passwd=" + self.password + "&output=json"
		body = "client=YourAppName&accountType=HOSTED_OR_GOOGLE&service=reader&Email=%s&Passwd=%s&output=json" % (self.__account,self.__password)
		url = "/accounts/ClientLogin"
		#TODO:what is the difference of default header between curl and httplib.request 
		self.__conn.request('POST',url,body)
		response = self.__conn.getresponse()
		msg = response.read()	
		try:
			result = json.loads(msg)
		except Exception,e:
			#TODO:toast account or passrowd error
			log = Log()
			log.error(str(e))
			return False

		self.__auth = result["Auth"]
		
		if self is not None:
			website = "theoldreader"
			sql = "insert into Accounts values('" + account + "','" + password + "','" + website + "')"
			self.__db.executeWithoutQuery(sql)
			return True
		else:
			Log.warn(str(result))
			#TODO:add log
			return False
	
	def loginWithCurl(self,account,password):
		#self.__conn.connect()
		self.__account = account
		self.__password = password

		curlCmd = '''curl -d "client=YourAppName&accountType=HOSTED_OR_GOOGLE&service=reader&Email=%s&Passwd=%s&output=json" https://theoldreader.com/accounts/ClientLogin''' % (self.__account,self.__password)

		msg = os.popen(curlCmd).read()

		try:
			result = json.loads(msg)
			
		except Exception,e:
			#TODO:toast account or passrowd error
			log = Log()

			errmsg = self.__errmsg % (__name__,"loginWithCurl")
			errmsg = errmsg + str(e)
			log.error(errmsg)
			return False

		self.__auth = result["Auth"]
		
		if self is not None:
			website = "theoldreader"
			querysql = "select * from ProxyAccounts where account='%s'" % self.__account

			res = self.__db.query(querysql)
			if res is None:
				insertProxy = '''insert into ProxyAccounts values("%s","%s","%s") ''' % (account,password,website)
				self.__db.executeWithoutQuery(insertProxy)

			return True
		else:
			errmsg = self.__errmsg % (__name__,"loginWithCurl")
			errmsg = errmsg + str(e)
			Log.warn(errmsg)
			#TODO:add log,tell user maybe acc or passwd error
			return False
	

	def getUnreadCount(self):
		url = "/reader/api/0/unread-count?output=json"
		headers = {"Authorization":"GoogleLogin auth=%s" % self.__auth}
		self.__conn.request(method='GET',url=url,headers=headers)
		
		msg = self.__conn.getresponse().read()
		result = json.loads(msg)
		return result["max"]
	

	def getUnreadIds(self,count):
		#TODO:only get 10 items
		url = "/reader/api/0/stream/items/ids?output=json&s=user/-/state/com.google/reading-list&xt=user/-/state/com.google/read" + "&n=10" 
		#url = "/reader/api/0/stream/items/ids?output=json&s=user/-/state/com.google/reading-list&xt=user/-/state/com.google/read" + "&n=" + str(count)
		headers = {"Authorization":"GoogleLogin auth=%s" % self.__auth}
		self.__conn.request(method='GET',url=url,headers=headers)

		ids = []
		jsonmsg = self.__conn.getresponse().read()
		try:
			result = json.loads(jsonmsg)
		except Exception,e:
			log = Log()
			errmsg = self.__errmsg % (__name__,"getUnreadIds")
			errmsg = errmsg + str(e)
			log.error(errmsg)
			
		unReadcount = len(result["itemRefs"])
		for i in range(0,unReadcount):
			ids.append(result["itemRefs"][i]["id"])

		return ids
	
	def getUnreadContent(self,id):
		url = "/reader/api/0/stream/items/contents?output=json&i=" + id
		headers = {"Authorization":"GoogleLogin auth=%s" % self.__auth}
		self.__conn.request(method='GET',url=url,headers=headers)
		
		jsonmsg = self.__conn.getresponse().read()
		try:
			result = json.loads(jsonmsg)
		except Exception,e:
			log = Log()
			errmsg = self.__errmsg % (__name__,"getUnreadIds")
			errmsg = errmsg + str(e)
			log.error(errmsg)
			
		#title = result["title"]
		title = result["items"][0]["title"]
		content = result["items"][0]["summary"]["content"]
		href = result["items"][0]["canonical"][0]["href"]
		author = result["items"][0]["author"]
		timestampUsec = result["items"][0]["timestampUsec"]
		website = "THEOLDREADER"

		title.replace("'","''")
		content.replace("'","''")
		href.replace("'","''")
		author.replace("'","''")
		timestampUsec.replace("'","''")


		sql = '''insert into Articals(id,author,title,website,content,href,timestampUsec) values('%s','%s','%s','%s','%s','%s','%s')''' % (id,author,title,website,content,href,timestampUsec)
		
		self.__db.executeWithoutQuery(sql)

	def getAllUnreadContentFromWeb(self):
		unreadCount = self.getUnreadCount()
		ids = self.getUnreadIds(unreadCount)

		unreadCountGot = len(ids)
		for id in ids:
			self.getUnreadContent(id)


	def close(self):
		#TODO:self.conn.close()
		self.__conn.close()
		self.__db.close()


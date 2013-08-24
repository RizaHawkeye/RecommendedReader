#send and recv are static class, add some what to identify them
#parameters of send and recv are changable
#method in base class is identify as @staticmethod, then method in derived class should be mark as @staticmerhod?
__metaclass__=type
import socket
import database
import json
from log import Log
import traceback
import account

ITEM_NUMBER_RETURN = 20
class Server:
	def __init__(self):
		pass


	def __getAndStoreRssData(self,account,passwd):
		rss = theoldreaderRss.TheoldreaderRss()
		account = "qr2434061@gmail.com"
		password = "theoldreader789456"
		if rss.loginWithCurl(account,password) == True:
			rss.getAllUnreadContentFromWeb()


	def __getProxyAccount(self,db,mainAccount,website):
		sql = "select account,password from ProxyAccounts where mainAccount = '%s' and website = '%s'" % (mainAccount,'THEOLDREADER')
		result = db.query(sql)
		return result[0]["account"],result[0]["password"]


	def __processWithML():
		#TODO:
		pass
	
	def checkAccount(self,account,passwd):
		mainAcc = account.MainAccount(mainAccount,mainPasswd)
		ret = mainAcc.verify()
		if ret == 0:
			err = {}
			err["error"] = "account is not exist"
			return err
		elif ret == -1:
			err = {}
			err["error"] = "account or password is not right"
			return err
		elif ret == 1:
			return None
	

	def getDataToSend(self,buf):
		try:
			(actionType,earliestTime,order,mainAccount,mainPasswd) = __getHeader(buf)
			
			if actionType == 'REG':
				return register(mainAccount,mainPasswd)


			retmsg = checkAccount(mainAccount,mainPasswd)
			if retmsg is not None:
				msg = json.dumps(rermsg)
				return msg


			(rssAccount,rssPasswd) = __getProxyAccount(db,mainAccount,"THEOLDREADER")
			__storeRssData(rssAccount,rssPasswd)
			__processWithML()


			begin = (int(order) - 1) * ITEM_NUMBER_RETURN
			end = int(order) * ITEM_NUMBER_RETURN - 1
			#limit count from 1 not 0

			sql = "select * from Articals where timestampUsec > '%s' order by weight limit %d,%d" % (earliestTime,begin,end)

			#print sql		

			result = db.query(sql)
			rowcount = len(result)
			
			print "rowcount: " + str(rowcount)
			#alldata = ""
			alldata = [] 
			for row in result:
				#TODO:
				item = {}
				item["id"] = row["id"]
				item["author"] = row["author"]
				item["title"] = row["title"]
				item["website"] = row["website"]
				item["content"] = row["content"]
				item["href"] = row["href"]
				item["timestampUsec"] = row["timestampUsec"]
				
				alldata.append(item)

			#convert string to json
			info = json.dumps(alldata)
			
			return info
		except Exception,e:
			#expand this error msg 
			errinfo = {}
			errinfo["error"] = "error"
			info = json.dumps(errinfo)
			errmsg = traceback.format_exc()
			log = Log()
			log.error(errmsg)
			return info
		finally:	
			db.close()

	@staticmethod
	def register(account,passwd):
		mainAcc = account.MainAccount(account,passwd)
		retmsg = mainAcc.storeAccount()
		if retmsg is not None:
			err = {}
			err["error"] = retmsg
			errmsg = json.dumps(err)
			return errmsg
		else:
			ok = {}
			ok["ok"] = "ok"
			msg = json.dumps(ok)
			return msg
			


	#derived class should rewrite this method
	@staticmethod
	def __getHeader(**param):
		pass

	@staticmethod
	def recv(**param):
		pass
	#derived class should rewrite this method

	@staticmethod
	def send(**param):
		pass
	
	def startServer():
		pass

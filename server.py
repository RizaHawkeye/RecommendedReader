#send and recv are static class, add some what to identify them
#parameters of send and recv are changable
#method in base class is identify as @staticmethod, then method in derived class should be mark as @staticmerhod?
#---------------------------------------------
#one server have many service, one service is a thread for one socket connect
#---------------------------------------------
__metaclass__=type
import socket
import database
import json
from log import Log
import traceback
import account as acc

ITEM_NUMBER_RETURN = 20
class Service:
	def __init__(self):
		pass

	def __getAndStoreRssData(self,account,passwd):
		rss = theoldreaderRss.TheoldreaderRss()
		account = "qr2434061@gmail.com"
		password = "theoldreader789456"
		if rss.loginWithCurl(account,password) == True:
			rss.getAllUnreadContentFromWeb()


	def __getProxyAccount(self,db,mainAccount):
		sql = "select distinct website from ProxyAccounts where mainAccount='%s'" % mainAccount
		resWebsites = db.query(sql)

		allProAcc = []
		for website in resWebsites:
			sql = "select account,password from ProxyAccounts where mainAccount = '%s' and website = '%s'" % (mainAccount,website)
			result = db.query(sql)

			onePair =  (result[0]["account"],result[0]["password"])
			allProAcc.add(onePair)

		return allProAcc


	def __processWithML(self):
		#TODO:
		pass
	
	def checkAccount(self,account,passwd):
		'''
		check if main account is correct
		'''
		mainAcc = acc.MainAccount(account,passwd)
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
			db = database.Database()
			args = self.getHeader(buf=buf)

			actionType = args[0]
			
			if actionType == 'ERR':  
				#TODO:process error
				pass

			elif actionType == 'REG':  
				mainAccount = args[1]
				mainPasswd = args[2]
				return self.register(mainAccount,mainPasswd)
			elif actionType == 'UPD':
				mainAccount = args[1]
				website = args[2]
				proAccount = args[3]
				proPasswd = args[4]
				return self.updateProAccount(mainAccount,website,proAccount,proPasswd)


			#actionType = 'GET'
			earliest = args[1]
			order = args[2]
			mainAccount = args[3]
			mainPasswd = args[4]
				
			retmsg = self.checkAccount(mainAccount,mainPasswd)
			if retmsg is not None:
				msg = json.dumps(rermsg)
				return msg


			allProAcc = __getProxyAccount(db,mainAccount)
			for (rssAccount,rssPasswd) in allProAcc:
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


	def register(self,account,passwd):
		mainAcc = acc.MainAccount(account,passwd)
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
			
	def updateProAccount(self,mainAccount,website,proAccount,proPasswd):
		'''
		'''
		if isExist(proAccount,mainAccount,website) == True:
			update(proAccount,proPasswd)
		else:
			storeAccount(proAccount,proPasswd,mainAccount,website)


	#derived class should rewrite this method
	def getHeader(self,**param):
		pass

	def recv(self,**param):
		pass
	#derived class should rewrite this method

	def send(self,**param):
		pass
	
class Server:
	def startServer():
		pass

__metaclass__=type
from database import Database
from log import Log
import traceback

class Account:
	def __init__(self,account,passwd):
		self.account = account
		self.passwd = passwd
	
	def verify(self,**param):
		'''
		return 1 means equal
		return 0 means don't have in db
		return -1 means don't equal
		'''
		pass

	def __isEqual(self,sql):
		'''
		return 1 means equal
		return 0 means don't have in db
		return -1 means don't equal
		'''
		try:
			db = Database()
			result = db.query(sql)
			if result is None:
				return 0
			dbAccount = result[0]["account"]
			dbPasswd = result[0]["passwd"]

			if account == dbAccount and passwd == dbPasswd:
				return 1
			else:
				return -1
		except:
			log = Log()
			errmsg = traceback.format_exc()
			log.error(errmsg)
		finally:
			#define db in try, then it can be access in finally?
			db.close()
	
	def isExist(self,account,**param):
		pass


	def __isExist(self,sql):
		try:
			db = Database()
			result = db.query(sql)
			if result is None:
				return 0

			if len(result) == 0:
				return False
			else:
				return True
		except:
			log = Log()
			errmsg = traceback.format_exc()
			log.error(errmsg)
		finally:
			#define db in try, then it can be access in finally?
			db.close()
	

		
	def storeAccount(self,account,password,*param):
		'''
		return None if ok
		return error msg if error
		'''
		pass
	
	def __storeAccount(self,sql):
		try:
			db = Database()
			db.executeWithoutQuery(sql)
			return None
		except Exception,e:
			#TODO:if have any duplicated account
			log = Log()
			errmsg = traceback.format_exec()
			log.error(errmsg)
			return str(e)
		finally:
			db.close()

	def update(self,account,password,**param):
		pass

	def __update(self,sql):
		try:
			db = Database()
			db.executeWithoutQuery(sql)
			return None
		except Exception,e:
			#TODO:if have any duplicated account
			log = Log()
			errmsg = traceback.format_exec()
			log.error(errmsg)
			return str(e)
		finally:
			db.close()



class MainAccount(Account):
	def __init__(self,account,passwd):
		print "-----------------------------"
		print type(account)
		print type(passwd)
		print "-----------------------------"
		super(MainAccount,self).__init__(account,passwd)

	
	def verify(self,**param):
		sql = "select * from MainAccounts where account = '%s' and password = '%s'" % (self.account,self.passwd)
		return __isEqual(sql)


	def storeAccount(self,account,password,**param):
		sql = "insert into MainAccount values('%s','%s')" % (self.account,self.passwd)

		return __storeAccount(sql)


	def isExist(self,account,**param):
		sql = "select * from MainAccount where account = '%s'" % account

	def updata(self,account,password):
		sql = "update MainAccount set account='%s',password='%s' where account='%s'" % (account,password,account)
		return __update(sql)


class ProxyAccount(Account):
	def __init__(self):
		super(ProxyAccount,self).__init__(account,passwd)
	
	def verify(self,**param):
		'''
		mainAccount=xxx
		website=xxx
		'''
		sql = "select * from ProxyAccounts where account = '%s' and password = '%s' and mainAccount = '%s' and website = '%s'" % (self.account,self.passwd,mainAccount,website)
		return __isEqual(sql)


	def storeAccount(self,account,password,**param):
		'''
		param is like is:
		mainAccount=xxx
		website=xxx
		'''
		sql = "insert into ProxyAccounts values('%s','%s','%s','%s')" % (self.account,self.passwd,mainAccount,website)

		return __storeAccount(sql)


	def isExist(self,account,**param):
		'''
		account=xxx
		mainAccount=xxx
		website=xxx
		'''
		sql = "select * from ProxyAccount where account = '%s' and mainAccount = '%s' and website = '%s'" % (account,mainAccount,website)
		return __isExist(sql)

	def update(self,account,password,**param):
		'''
		param is like this:
		mainAccount=xxx
		website=xxx
		'''
		sql = "update ProxyAccount set account='%s',password='%s' where mainAccount='%s' and website='%s'" % (account,password,mainAccount,website)
		return __update(sql)

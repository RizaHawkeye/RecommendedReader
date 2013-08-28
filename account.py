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

	def _isEqual(self,sql):
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
			dbPasswd = result[0]["password"]

			if self.account == dbAccount and self.passwd == dbPasswd:
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


	def _isExist(self,sql):
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
	
	def _storeAccount(self,sql):
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

	def _update(self,sql):
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
		super(MainAccount,self).__init__(account,passwd)

	
	def verify(self,**param):
		sql = "select * from MainAccounts where account = '%s' and password = '%s'" % (self.account,self.passwd)
		return self._isEqual(sql)


	def storeAccount(self,account,password,**param):
		sql = "insert into MainAccounts values('%s','%s')" % (self.account,self.passwd)

		return self._storeAccount(sql)


	def isExist(self,account,**param):
		sql = "select * from MainAccounts where account = '%s'" % account
		return self._isExist(sql)

	def updata(self,account,password):
		sql = "update MainAccounts set account='%s',password='%s' where account='%s'" % (account,password,account)
		return self._update(sql)


class ProxyAccount(Account):
	def __init__(self):
		super(ProxyAccount,self).__init__(account,passwd)
	
	def verify(self,**param):
		'''
		mainAccount=xxx
		website=xxx
		'''
		sql = "select * from ProxyAccounts where account = '%s' and password = '%s' and mainAccount = '%s' and website = '%s'" % (self.account,self.passwd,mainAccount,website)
		return self._isEqual(sql)


	def storeAccount(self,account,password,**param):
		'''
		param is like is:
		mainAccount=xxx
		website=xxx
		'''
		sql = "insert into ProxyAccounts values('%s','%s','%s','%s')" % (self.account,self.passwd,mainAccount,website)

		return self._storeAccount(sql)


	def isExist(self,account,**param):
		'''
		account=xxx
		mainAccount=xxx
		website=xxx
		'''
		sql = "select * from ProxyAccount where account = '%s' and mainAccount = '%s' and website = '%s'" % (account,mainAccount,website)
		return self._isExist(sql)

	def update(self,account,password,**param):
		'''
		param is like this:
		mainAccount=xxx
		website=xxx
		'''
		sql = "update ProxyAccount set account='%s',password='%s' where mainAccount='%s' and website='%s'" % (account,password,mainAccount,website)
		return self._update(sql)

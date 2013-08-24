__metaclass__=type
from database import Database
from log import Log
import traceback

class Account:
	def __init__(self,account,passwd):
		self.__account = ""
		self.__passwd = ""
	
	def verify(self):
		'''
		return 1 means equal
		return 0 means don't have in db
		return -1 means don't equal
		'''
		pass

	def isEqual(self,sql)
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
		
	def storeAccount(self):
		'''
		return None if ok
		return error msg if error
		'''
		pass
	
	def __storeAccount(self,sql)
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
		super(MainAccount).__init__(account,passwd)
	
	def verify(self):
		sql = "select * from MainAccounts where account = '%s' and password = '%s'" % (self.__account,self.__passwd)
		return isEqual(sql)


	def storeAccount(self)
		sql = "insert into MainAccount values('%s','%s')" % (self.__account,self.__passwd)

		return __storeAccount(sql)


class ProxyAccount(Account):
	def __init__(self):
		super(ProxyAccount).__init__(account,passwd)
	
	def verify(self):
		#sql = "select * from MainAccounts where account = '%s'"	
		return isEqual(sql)

	def storeAccount(self)
		sql = 




#in this class, I add conn.commit() after execute, some people say that it is not necessary, but if i don't add commit() the sql won't execute in my computer
__mataclass__=type
import MySQLdb as mdb
from log import Log

class Database:
	def __init__(self):
		try:
			self.__conn = mdb.connect("localhost","root","root","reader")
		except mdb.Error,e:
			log = Log()
			log.error(str(e))
	
	def executeWithoutQuery(self,sql):
		try:
			cursor = self.__conn.cursor()
			cursor.execute(sql)
			self.__conn.commit()
		except mdb.Error,e:
			log = Log()
			log.error(str(e))
		finally:
			cursor.close()
	
	def query(self,sql):
		try:
			cursor = self.__conn.cursor(mdb.cursors.DictCursor)
			cursor.execute(sql)
			result = cursor.fetchall()
			self.__conn.commit()
			return result
		except mdb.Error,e:
			log = Log()
			log.error(str(e))
		finally:
			cursor.close()

	def close(self):
		try:
			self.__conn.close()
		except mdb.Error,e:
			log = Log()
			log.error(str(e))


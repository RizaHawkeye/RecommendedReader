#in this class, I add conn.commit() after execute, some people say that it is not necessary, but if i don't add commit() the sql won't execute in my computer
__mataclass__=type
import MySQLdb as mdb
from log import Log
import traceback

class Database:
	def __init__(self):
		try:
			self.__conn = mdb.connect(host="localhost",user="root",passwd="root",db="reader",charset="utf8")
		except mdb.Error,e:
			log = Log()
			errmsg = traceback.format_exc()
			log.error(errmsg)

	def __setCharset(self,cursor):
		cursor.execute("SET NAMES utf8")
		cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
		cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
		self.__conn.commit()
	
	def executeWithoutQuery(self,sql):
		try:
			cursor = self.__conn.cursor()
			self.__setCharset(cursor)
			cursor.execute(sql)
			self.__conn.commit()
		except mdb.Error,e:
			log = Log()
			errmsg = traceback.format_exc()
			log.error(errmsg)
		finally:
			cursor.close()
	
	def query(self,sql):
		try:
			cursor = self.__conn.cursor(mdb.cursors.DictCursor)
			self.__setCharset(cursor)
			cursor.execute(sql)
			result = cursor.fetchall()

			return result
		except mdb.Error,e:
			log = Log()
			errmsg = traceback.format_exc()
			log.error(errmsg)
		finally:
			cursor.close()

	def close(self):
		try:
			self.__conn.close()
		except mdb.Error,e:
			log = Log()
			errmsg = traceback.format_exc()
			log.error(errmsg)

#	def __del__(self):
#		try:
#			if self.__conn is not None:
#				self.__conn.close()
#		except mdb.Error,e:
#			log = Log()
#			errmsg = traceback.format_exc()
#			log.error(errmsg)




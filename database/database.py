__mataclass__=type
import MySQLdb as mdb

class Database:
	def __init__(self):
		self.conn = mdb.connect("localhost","root","root","reader")
	
	def executeWithoutQuery(self,sql):
		cursor = conn.cursor()
		cursor.execute(sql)
	
	def query(self,sql):
		cursor = conn.cursor()
		cursor.execute(sql)
		result = cursor.fetchall()
		return result
	
	def close(self):
		conn.close()


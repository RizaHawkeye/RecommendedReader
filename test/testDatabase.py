from database import Database
import MySQLdb as mdb

def test():
	id = "111112"
	author = "quanrui"
	title = "helle"
	content = "hello world"
	href = "www.sina.com.cn"
	timestampUsec = "123123123"
	website = "THEOLDREADER"

	insertArt = '''insert into Articals(id,author,title,website,content,href,timestampUsec) values("%s","%s","%s","%s","%s","%s","%s")''' % (id,author,title,website,content,href,timestampUsec)

	account = "qr"
	password = "789"
	website = "THEOLDREADER"

	insertProxy = '''insert into ProxyAccounts values("%s","%s","%s") ''' % (account,password,website)

	insertMain = '''insert into MainAccounts values("%s","%s")''' % (account,password)

	selectsql = '''select * from Articals'''

	deleteArt = '''delete from Articals'''
	deleteProxy = '''delete from ProxyAccounts'''
	deleteMain = '''delete from MainAccounts'''


	db = Database()

	db.executeWithoutQuery(insertArt)
	db.executeWithoutQuery(insertProxy)
	db.executeWithoutQuery(insertMain)

	res = db.query(selectsql)
	print res

#	db.executeWithoutQuery(deleteArt)
#	db.executeWithoutQuery(deleteProxy)
#	db.executeWithoutQuery(deleteMain)
#
#	res = db.query(selectsql)
#	print res

	db.close()

test()
#conn = mdb.connect("localhost","root","root","reader")
#
#cursor = conn.cursor()
#
#account = "qr"
#password = "789"
#website = "THEOLDREADER"
#
#sql = '''insert into ProxyAccounts values("%s","%s","%s") ''' % (account,password,website)
#
#cursor.execute(sql)
#conn.commit()
#cursor.close()
#conn.close()

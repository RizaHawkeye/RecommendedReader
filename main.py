__metaclass__=type
import theoldreaderRss

rss = theoldreaderRss.TheoldreaderRss()
account = "qr2434061"
password = "theoldreader789456"
if rss.login(account,password) == False:
	print 

rss.getAllUnreadContentFromWeb()


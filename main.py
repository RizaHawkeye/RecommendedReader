__metaclass__=type
import rss

account = "qr2434061"
password = "theoldreader789456"
rss = RSS(account,password)
rss.login()
unreadCount =rss.getUnreadCount()
ids = rss.getUnreadItems(unreadCount)

unreadCountGot = len(ids)
for i in ids:
	author,title,content,href,timestampUsec = rss.getUnreadContent(ids[i])
	

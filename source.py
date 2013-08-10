__metaclass__=type
import json,httplib

class Source:
	'''base class of rss,douban,and zhihu'''
		#private or public?  __account is private? have try

	def __init__(self):
		self.__account = None
		self.__password = None

	def login(self,account,password):
		pass

	def getUnreadCount(self):
		pass

	def getUnreadIds(self,count):
		pass

	def getUnreadContent(self,id):
		pass

	def close(self):
		pass
	

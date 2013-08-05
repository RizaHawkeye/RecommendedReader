__metaclass__=type
import json,httplib

class Source:
	'''base class of rss,douban,and zhihu'''
		#private or public?  __account is private? have try

	def __init__(self):
		self.__account = None
		self.__password = None

	def login(self,account,password):
		return false

	def getUnreadCount(self):
		return -1

	def getUnreadIds(self,count):
		ret = []
		return ret
	
	def getUnreadContent(self,id):
		ret = []
		return ret 

	def close(self):
		pass
	

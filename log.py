__metaclass__=type

import logging
'''
example:
import log

log = log.Log("test.log")
log.debug("debug")
log.info("info")
log.warn("warn")
log.error("error")
log.critical("critical")
'''
class Log:
	def __init__(self,filename):
		formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

		self.__logger = logging.getLogger("mylog")
		self.__logger.setLevel(logging.DEBUG)

		self.__createConsoleLog(formatter)
		self.__createFileLog(filename,formatter)

	def __createConsoleLog(self,formatter):
		consolelog = logging.StreamHandler()
		consolelog.setLevel(logging.DEBUG)

		consolelog.setFormatter(formatter)

		self.__logger.addHandler(consolelog)
		
	def __createFileLog(self,filename,formatter):
		filelog = logging.FileHandler(filename)
		filelog.setLevel(logging.DEBUG)
		
		filelog.setFormatter(formatter)

		self.__logger.addHandler(filelog)
		
	def debug(self,msg):
		self.__logger.debug(msg)

	def info(self,msg):
		self.__logger.info(msg)

	def warn(self,msg):
		self.__logger.warn(msg)

	def error(self,msg):
		self.__logger.error(msg)

	def critical(self,msg):
		self.__logger.critical(msg)




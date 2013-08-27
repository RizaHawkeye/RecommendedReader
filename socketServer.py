#------------------------------------
#json.dumps() changes duild-in data structure to string
#json.loads() changes string to build-in data struct
#------------------------------------
import threading
import Queue
import theoldreaderRss
import server
from log import Log
import socket
import traceback
import json

class socketServerSendThread(threading.Thread):
	def __init__(self,sockQueue):
		super(socketServerSendThread,self).__init__()
		self.queue = sockQueue

	def run(self):
		try:
			if __name__ == '__main__':
				print "waiting for recv"
			sock = self.queue.get()

			service = SocketService()
			buf = service.recv(sock=sock)
			service.send(sock=sock,buf=buf)

			self.queue.task_done()
		except socket.error, e:
			errmsg = traceback.format_exc()
			log = Log()
			log.error(errmsg)
		finally:
			sock.close()

class SocketService(server.Service):
	def __init__(self):
		super(SocketService,self).__init__()
	
	def getHeader(self,**param):
		'''
		call __getHeaders should like this:
		__getHeaders(buf=xxx)

		type:GET   #get articals
		earliestTime:xxx
		order:XXX  (begin with 1)
		account:xxx
		passwd:xxx
		OR
		type:REG    #register
		account:xxx
		passwd:xxx
		OR
		type:UPD   #add or update proxy account
		mainAccount:xxx
		website:xxx
		proAccount:xxx
		proPasswd:xxx
		'''
		info = "";
		buf = param["buf"]
		try:
			clientJsonObj = json.loads(buf)
			actionType = clientJsonObj["type"]
			if actionType == 'GET':
				earliestTime = clientJsonObj["earliestTime"]
				order = clientJsonObj["order"]
				mainAccount = clientJsonObj["account"]
				mainPasswd = clientJsonObj["passwd"]
				return (actionType,earliestTime,order,mainAccount,mainPasswd)
			elif actionType == 'REG':
				mainAccount = clientJsonObj["account"]
				mainPasswd = clientJsonObj["passwd"]
				return (actionType,mainAccount,mainPasswd)
			elif actionType == 'UPD':
				mainAccount = clientJsonObj["mainAccount"]
				website = clientJsonObj["website"]
				proAccount = clientJsonObj["proAccount"]
				proPasswd = clientJsonObj["proPasswd"]
				return (actionType,mainAccount,website,proAccount,proPasswd)
		except:
			#expand this error msg 
			errmsg = traceback.format_exc()
			log = Log()
			log.error(errmsg)
			return ("ERR",)
	
	def recv(self,**param):
		'''param is sock=xxx'''
		recvBuf = 1024*1024
		sock = param["sock"]
		buf = sock.recv(recvBuf)
		return buf
		
	
	#def send(self,sock,buf):
	def send(self,**param):
		'''param is sock=xxx,buf=xxx'''
		buf = param["buf"]
		sock = param["sock"]
		info = self.getDataToSend(buf)

		sock.sendall(info)

	
class SocketServer(server.Server):
	def startServer(self):
		port = 1989
		buffer_size = 4098
		log = Log()
		sockQueue = Queue.Queue()
		try:
			sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			sock.bind(('localhost',port))
			sock.listen(0)
		except socket.error, e:
			errmsg = traceback.format_exc()
			log.error(errmsg)
			return #TODO:???ok


		while True:
			try:
				sockAccept,address = sock.accept()
				
			except socket.error, e:
				errmsg = traceback.format_exc()
				log.err(errmsg)

			sockQueue.put(sockAccept)
			t = socketServerSendThread(sockQueue)
			t.Daemon = True
			t.start()


def startSocketServer():
	server = SocketServer()
	server.startServer()

if __name__ == '__main__':
	startSocketServer()
	

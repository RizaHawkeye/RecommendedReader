#------------------------------------
#json.dumps() changes duild-in data structure to string
#json.loads() changes string to build-in data struct
#------------------------------------
import threading
import Queue
import theoldreaderRss
import server

class socketServerSendThread(threading.Thread):
	def __init__(self,sockQueue):
		super(SendInfoThread,self).__init__()
		self.queue = sockQueue

	def run(self):
		try:
			if __name__ == '__main__':
				print "waiting for recv"
			sock = self.queue.get()
			buf = socketServer.recv(sock)
			socketServer.send(sock,buf)

			self.queue.task_done()
		except socket.error, e:
			errmsg = traceback.format_exc()
			log = Log()
			log.error(errmsg)
		finally:
			sock.close()

class socketServer(Server):
	def __init__(self):
		super(socketServer).__init__()
	
	def __getHeaders(**param):
		'''
		call __getHeaders should like this:
		__getHeaders(buf=xxx)

		type:GET
		earliestTime:xxx
		order:XXX  (begin with 1)
		account:xxx
		passwd:xxx
		OR
		type:REG    #register
		account:xxx
		passwd:xxx
		'''
		info = "";

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
				return (actionType,None,None,mainAccount,mainPasswd)
		except:
			#expand this error msg 
			errmsg = traceback.format_exc()
			log = Log()
			log.error(errmsg)
	
	def recv(**param):
		'''param is sock=xxx'''
		recvBuf = 1024*1024
		buf =sock.recv(recvBuf)
		return buf
		
	
	#def send(self,sock,buf):
	def send(**param):
		'''param is sock=xxx,buf=xxx'''
		info = self.getDataToSend(buf)

		sock.sendall(info)

	
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
	

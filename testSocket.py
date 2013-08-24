import socket
import json
import threading
import socketServer
import time

class ConnectServerThread(threading.Thread):
	def __init__(self):
		super(ConnectServerThread,self).__init__()

	def run(self):
		port = 1989
		try:
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			server_ip = socket.gethostbyname('localhost')

			sock.connect((server_ip,port))

			recvThread = RecvServerInfoThread(sock)
			recvThread.Daemon = True
			recvThread.start()

			earliestTime = "1376665266000000"
			order = "1"

			info={}
			info["earliestTime"] = "1376665266000000"
			info["order"] = order

			data_to_server=json.dumps(info)
			#print "data_to_server: " + data_to_server

			sock.sendall(data_to_server)
		except Exception,e:
			print str(e)
	
class RecvServerInfoThread(threading.Thread):
	def __init__(self,sock):
		self.sock = sock
		super(RecvServerInfoThread,self).__init__()

	def run(self):
		try:
			recvBuf = 1024*1024
			buf = self.sock.recv(recvBuf)
			allContent = json.loads(buf)

			for content in allContent:
				print "-----------------------------"
				print "id---" + content["id"]
				print "author---" + content["author"]
				print "title---" + content["title"]
				print "website---" + content["website"]
				#print "content---" + content["content"]
				print "href---" + content["href"]
				print "timestampUsec---" + content["timestampUsec"]
				print "-----------------------------"

		except Exception,e:
			print str(e)

class RunServerThread(threading.Thread):
	def __init__(self):
		super(RunServerThread,self).__init__()

	def run(self):
		socketServer.startSocketServer()


if __name__ == '__main__':
	server = RunServerThread()
	server.Daemon = True
	server.start()
	
	time.sleep(1)
	
	client = ConnectServerThread()
	client.Daemon = True
	client.start()

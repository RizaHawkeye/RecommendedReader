#------------------------------------
#json.dumps() changes duild-in data structure to string
#json.loads() changes string to build-in data struct
#------------------------------------
__metaclass__=type
import socket
import threading
import Queue
import json
import database
import traceback
from log import Log

ITEM_NUMBER_RETURN = 20
class SendInfoThread(threading.Thread):
	def __init__(self,sockQueue):
		super(SendInfoThread,self).__init__()
		self.queue = sockQueue

	def run(self):
		try:
			sock = self.queue.get()
			recvBuf = 1024*1024
			buf =sock.recv(recvBuf)
			if __name__ == '__main__':
				print "waiting for recv"

			info = self.process(buf)

			sock.sendall(info)
			self.queue.task_done()
		except socket.error, e:
			errmsg = traceback.format_exc()
			log = Log()
			log.error(errmsg)
		finally:
			sock.close()
	
	def process(self,buf):
		'''
		earliestTime:XXX
		order:XXX  (begin with 1)
		'''
		#print "in process buf is: " + buf

		info = "";

		try:
			clientJsonObj = json.loads(buf)
			db = database.Database()
			earliestTime = clientJsonObj["earliestTime"]
			order = clientJsonObj["order"]

			begin = (int(order) - 1) * ITEM_NUMBER_RETURN + 1
			end = int(order) * ITEM_NUMBER_RETURN
			#limit count from 1 not 0
			#sql = "select * from reader limit " + begin + "," + end+ " where timestampUsec > \'" +  beginTime + "\' order by weight"

			sql = "select * from Articals order by weight limit %d,%d" % (begin,end)

#			if method == "NEW":
#				earliestTime = clientJsonObj["earliestTime"]
#
#			elif flag == "MORE"
#				earliestTime = clientJsonObj["earliestTime"]
#				latestTime = clientJsonObj["latest"]
#				sql = "select * from reader limit " + ITEM_NUMBER_RETURN +" where timestampUsec > \'" + beginTime + "\' and timestampUsec < \'" + endTime + "\'" 
			print sql		

			cursor = db.query(sql)
			rowcount = cursor.rowcount
			result = cursor.fetchall()
			
			#alldata = ""
			alldata = [] 
			for row in result:
				#TODO:
				#item = '''["id":"%s","author":"%s","title":"%s","website":"%s","content":"%s","href":"%s","timestampUsec":"%s"]\n''' % (row["id"],row["author"],row["title"],row["website"],row["content"],row["href"],row["timestampUsec"])
				item = {}
				item["id"] = row["id"]
				item["author"] = row["author"]
				item["title"] = row["title"]
				item["website"] = row["website"]
				item["content"] = row["content"]
				item["href"] = row["href"]
				item["timestampUsec"] = row["timestampUsec"]
				
				alldata.append(item)

			#convert string to json
			info = json.dumps(alldata)
			
			db.close()
		except Exception,e:
			#expand this error msg 
			errinfo = {}
			errinfo["error"] = "error"
			info = json.dumps(errinfo)
			errmsg = traceback.format_exc()
			log = Log()
			log.error(errmsg)

		
		return info

def startSocketServer():
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
		t = SendInfoThread(sockQueue)
		t.Daemon = True
		t.start()


if __name__ == '__main__':
	startSocketServer()
	

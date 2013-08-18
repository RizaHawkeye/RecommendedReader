#------------------------------------
#json.dumps() changes duild-in data structure to string
#json.loads() changes string to build-in data struct
#------------------------------------
__metaclass__=type
import socket
import threading
import Queue
import json
from log import Log

ITEM_NUMBER_RETURN = 20
class SendInfoThread(threading.Thread):
	def __inti__(self,queue):
		super(SendInfoThread,self).__init__()
		self.queue = sockQueue

	def run(self):
		try:
			socket = self.queue.get()
			recvBuf = 1024*1024
			buf =scoket.recv(recvBuf)
			if __name__ == '__main__':
				print "waiting for recv"

			info = process(buf)

			socket.sendall(info)
			self.queue.task_done()
		except socket.err, e:
			log = Log()
			log.error(str(e))
	
	def process(self,buf):
		'''
		earliestTime:XXX
		order:XXX
		'''
		clientJsonObj = json.load(buf)


		db = database.Database()
		earliestTime = clientJsonObj["earliestTime"]
		order = clientJsonObj["order"]

		begin = (order - 1) * ITEM_NUMBER_RETURN + 1
		end = order * ITEM_NUMBER_RETURN
		#limit count from 1 not 0
		#sql = "select * from reader limit " + begin + "," + end+ " where timestampUsec > \'" +  beginTime + "\' order by weight"

		sql = "select * from reader limit %d,%d order by weight" % (begin,end)

#		if method == "NEW":
#			earliestTime = clientJsonObj["earliestTime"]
#
#		elif flag == "MORE"
#			earliestTime = clientJsonObj["earliestTime"]
#			latestTime = clientJsonObj["latest"]
#			sql = "select * from reader limit " + ITEM_NUMBER_RETURN +" where timestampUsec > \'" + beginTime + "\' and timestampUsec < \'" + endTime + "\'" 
#		
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
		log.error(str(e))
		return #TODO:???ok


	while True:
		try:
			sockAccept,address = sock.accept()
			
		except socket.error, e:
			log.err(str(e))

		sockQueue.put(sockAccept)
		t = SendInfoThread(sockQueue)
		t.Daemon = True
		t.start()


if __name__ == '__main__':
	startSocketServer()
	

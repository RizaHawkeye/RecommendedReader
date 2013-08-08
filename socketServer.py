__metaclass__=type
import socket
import threading
import log
import Queue
import json

ITEM_NUMBER_RETURN = 20
class SendInfoThread(threading.Thread):
	def __inti__(self,queue):
		super(SendInfoThread,self).__init__()
		self.queue = sockQueue

	def run(self):
		try:
			socket = self.queue.get()
			buf =scoket.recv()

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
		sql = "select * from reader limit " + begin + "," + end+ " where timestampUsec > \'" +  beginTime + "\' order by weight"
#		if method == "NEW":
#			earliestTime = clientJsonObj["earliestTime"]
#			#TODO:sort
#
#		elif flag == "MORE"
#			earliestTime = clientJsonObj["earliestTime"]
#			latestTime = clientJsonObj["latest"]
#			sql = "select * from reader limit " + ITEM_NUMBER_RETURN +" where timestampUsec > \'" + beginTime + "\' and timestampUsec < \'" + endTime + "\'" 
#		
		cursor = db.query(sql)
		rowcount = cursor.rowcount
		result = cursor.fetchall()

		for row in result:
			#TODO:

		db.close()

def startSocketServer():
	port = 1989
	buffer_size = 4098
	log = log.Log()
	sockQueue = Queue.Queue()
	try:
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.bind('localhost',port)
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
		t = SendInfoThread(queue)
		t.Daemon = True
		t.start()

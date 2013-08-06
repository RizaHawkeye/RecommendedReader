__metaclass__=type
import socket

port = 1989
buffer_size = 4098
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind('localhost',port)
sock.listen(0)



while True:
	sockAccept,address = sock.accept()
	try:
		buf = sockAccept.recv(buffer_size)
		
	except socket.error 

import socket
from _thread import *
from sys import argv

HOST="127.0.0.1"
PORT=8080
RECV_BYTES=100
REQ_NO=1

if len(argv) > 0:
	try:
		if (len(argv[1]) > 0):
			HOST = argv[1]
			
		if (len(argv[2]) > 0):
			PORT = argv[2]
		
		if (len(argv[3]) > 0):
			RECV_BYTES = argv[3]
		
	except Exception as e:
		print("")
		print("!---Some of the arguments are not specified. Using default values---!") 
		print("")
		
def respond(c,addr,recv_bytes):
	global REQ_NO
	
	msg = "Thanks for connecting!"
	
	response_headers = {
		'Content-Type': 'text/html; encoding=utf8',
		'Content-Length': len(msg),
		'Connection': 'close',
	}

	response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())

	response_proto = 'HTTP/1.1'
	response_status = '200'
	response_status_text = 'OK' # this can be random

	r = ('%s %s %s\r\n' % (response_proto, response_status, response_status_text) + response_headers_raw + '\r\n' + msg)
	c.send(r.encode("utf-8"))
	#c.send(response_headers_raw.encode("utf-8"))
	#c.send('\r\n'.encode("utf-8"))
	#c.send(msg.encode(encoding="utf-8"))
	print("")	
	print("------{}------".format(REQ_NO))
	print(str(c.recv(recv_bytes).decode("utf-8")))
	print("-------------")
	REQ_NO += 1
	c.close()
	
s=socket.socket()
s.bind((HOST,PORT))
s.listen(5)
print("Server Started at\nHOST: {}\nPORT: {}\nRECV_BYTES: {}".format(HOST,PORT,RECV_BYTES))	
while True:
	c,addr = s.accept()
	start_new_thread(respond,(c,addr,RECV_BYTES))

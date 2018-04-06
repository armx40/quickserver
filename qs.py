import socket
from _thread import *
import argparse

HOST="127.0.0.1"
PORT=8080
RECV_BYTES=100
REQ_NO=1
MSG="hello client"

parser = argparse.ArgumentParser(description='quickserver arguments')

parser.add_argument('-H',help="Host")
parser.add_argument('-P',help="Port")
parser.add_argument('-M',help="Message to client")
parser.add_argument('-B',help="Number of bytes to receive from the client")

args = parser.parse_args()
args = vars(args)

if args['H'] is not None:
	HOST = args['H']
if args['P'] is not None:
	PORT = int(args['P'])
if args['M'] is not None:
	MSG = args['M']
if args['B'] is not None:
	RECV_BYTES = int(args['B'])

def respond(c,addr,recv_bytes):
	global REQ_NO
	response_headers = {
		'Content-Type': 'text/html; encoding=utf8',
		'Content-Length': len(MSG),
		'Connection': 'close',
	}

	response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())

	response_proto = 'HTTP/1.1'
	response_status = '200'
	response_status_text = 'OK' # this can be random

	r = ('%s %s %s\r\n' % (response_proto, response_status, response_status_text) + response_headers_raw + '\r\n' + MSG)
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
print("server started at\nHOST: {}\nPORT: {}\nRECV_BYTES: {}\nMESSAGE: {}".format(HOST,PORT,RECV_BYTES,MSG))	
while True:
	c,addr = s.accept()
	start_new_thread(respond,(c,addr,RECV_BYTES))

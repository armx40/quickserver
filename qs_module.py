import socket
from _thread import *

global counter_count


def print_log(log_item_, log_file_):
    f = open(log_file_, 'a')
    f.write(log_item_)
    f.close()


def respond(c, addr, RECV_BYTES_, response_function_, http_response_, log_, log_file_):
    global counter_count
    item_received = c.recv(RECV_BYTES_).decode("utf-8")
    res = response_function_(item_received)

    if (http_response_):
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(res),
            'Connection': 'close',
        }

        response_headers_raw = ''.join('%s: %s\r\n' % (k, v)
                                       for k, v in response_headers.items())

        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK'
        r = ('%s %s %s\r\n' % (response_proto, response_status,
                               response_status_text) + response_headers_raw + '\r\n' + res)
    else:
        r = res
    c.send(r.encode("utf-8"))
    c.close()

    if (log_):
        print_log(str(addr) + " | " + item_received +
                  " | " + r + "\n----------\n", log_file_)

    return


def start_server(HOST_, PORT_, RECV_BYTES_, response_function_, http_response_, log_, log_file_, counter):
    global counter_count
    s = socket.socket()
    s.bind((HOST_, PORT_))
    s.listen(5)
    
    if (counter == 0):
        while True:
            c, addr = s.accept()
            start_new_thread(respond, (c, addr, RECV_BYTES_,
                                    response_function_, http_response_, log_, log_file_))
    else:
        for _ in range(counter):
            c, addr = s.accept()
            start_new_thread(respond, (c, addr, RECV_BYTES_,response_function_, http_response_, log_, log_file_))   

def __init__(HOST_, PORT_, RECV_BYTES_, response_function_, http_response_=False, log_=False, log_file_="./qs_log.log", counter=0):
    global HOST, PORT, response_function, log
    HOST = HOST_
    PORT = PORT_
    response_function = response_function_
    http_response_ = http_response_
    log = log_
    start_server(HOST_, PORT_, RECV_BYTES_, response_function,
                 http_response_, log_, log_file_, counter)

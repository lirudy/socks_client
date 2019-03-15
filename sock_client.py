import os
import sys
import logging
import socks
import socket
import fcntl
import thread


SOCKS5_PROXY_HOST = sys.argv[1]
SOCKS_PROXY_PORT = sys.argv[2]

def send_log(content):
    logging.error(content)

socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS_PROXY_PORT)
remote_conn = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
remote_ip = sys.argv[3]
remote_port = sys.argv[4]

PY3K = sys.version_info >= (3, 0)
if PY3K:
    console_source = sys.stdin.buffer

try:
    remote_conn.connect((remote_ip, int(remote_port)))
except Exception as e:
    send_log("Error: Unable to connect remote server." + str(e))
    sys.exit()

def read_in(conn):
    while True:
        fd = sys.stdin.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        try:
            text = sys.stdin.read()
            sent = conn.send(text)
        except Exception as e:
            pass

def read_socket(conn):
    while True:
        try:
            in_data = conn.recv(1024)
            if in_data and len(in_data) > 0:
                sys.stdout.write(in_data)
                sys.stdout.flush()
        except Exception as e:
            pass

try:
    thread.start_new_thread( read_socket, (remote_conn, ) )
    thread.start_new_thread( read_in, (remote_conn, ) )
except:
    pass

while 1:
    pass


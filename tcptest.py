#
# _*_ coding:UTF-8 _*_

import socket
import time
import threading
import pickle
import sys

import hashlib
terminating = False
isserver = False
sended = False
def heartbeat(s, des):
    while not terminating:
        time.sleep(1)
        s.sendto("call me at port 7890", des)

def tcplink(sock, addr):
    global sended
    print("connected")
    # sock.send("Welcome!".encode())
    try:
        while not terminating:
            if isserver and not sended:
                sock.send("hello".encode())
                sended = True
            data = sock.recv(1024)
            if not data:
                continue
            print(data.decode())
            if data.decode() == "hello":
                sock.send("get!".encode())
            time.sleep(1)

    except Exception as e:
        print(e)
        # time.sleep(1)
        # sock.send("time: %f" % time.time())
    sock.close()
    print("Connection from %s:%s closed." % addr)
    sended = False


def client():
    global terminating
    tcpclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # addr = ("192.168.1.11", 29989)
    addr = ('localhost', 29989)
    tcpclient.settimeout(3000)
    tcpclient.connect(addr)
    tcpclient.setblocking(10)
    terminating=False
    t_sock = threading.Thread(target=tcplink, args=(tcpclient, addr))
    t_sock.setDaemon(True)
    t_sock.start()
    while True:
        time.sleep(1)

def server():
    global isserver
    isserver = True
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcpserver.bind(('0.0.0.0', 29989))  # 监听端口
    tcpserver.listen(5)
    tcpserver.settimeout(5)
    print("starting listen at ")
    print(socket.gethostbyname(socket.gethostname()))
    global terminating
    try:
        while not terminating:
            try:
                sock, addr = tcpserver.accept()
                sock.setblocking(1)
                t_sock = threading.Thread(target=tcplink, args=(sock, addr))
                t_sock.setDaemon(True)
                t_sock.start()
            except socket.timeout:
                pass
            except all:
                terminating = True
                print("unknown network error")
                return

    except KeyboardInterrupt:
        print("Ctrl+C")
        terminating = True
        return


if __name__ == "__main__":
    # cryptotest()
    # server()
    client()
    print("end snakeserver")




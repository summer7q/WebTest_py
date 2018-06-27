from flask import request
import socket
import threading
import time
import json
import pymongo

from app import app

terminating = False
sended = False


def async(f):
   def wrapper(*arg, **kwargs):
      th = threading.Thread(target=f, args=arg, kwargs=kwargs)
      th.setDaemon(True)
      th.start()
   return wrapper

@app.route("/data", methods=["POST", "GET"])
def data():
    if request.method == "POST":
        print(request.json)
        return "get new post"
    else:
        return "hello world"


@async
def testStart(sock, addr, data):
    """

    :param socket.socket sock:
    :param str addr:
    :return:
    """


def testEnd(sock, addr, data):
    """

    :param socket.socket sock:

    :param str addr:
    :return:
    """

def authCheck(sock, data):
    """
    
    :param socket.socket sock: 
    :param str data: 
    :return: 
    """
    print('Enter authCheck!')
    sock.send(b'JoinSuccess')





@async
def tcplink(sock, addr):
    """

    :param socket.socket sock:

    :param str addr:
    :return:
    """
    print('Accept new connection from %s:%s' % addr)
    sock.send('Connected!'.encode())
    while True:
        data = sock.recv(1024)
        if data:
            print(data)
            jsonData = json.loads(data.decode())
            if jsonData['type'] == 'exit':
                break
            elif jsonData['type'] == 'JN':
                authCheck(sock, jsonData)
            elif jsonData['type'] == 'TS':
                testStart(sock, addr, jsonData)
            elif jsonData['type'] == 'TE':
                testEnd(sock, addr, jsonData)
            print('get command type of %s ' % jsonData['type'])
        else:
            continue
    sock.close()
    print('unconnected with %s:%s ' % addr)




def server(n):
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpserver.bind(('0.0.0.0', 29989))  # 监听端口
    tcpserver.listen(n)
    tcpserver.settimeout(5)
    print("starting listen at ")
    print(socket.gethostbyname(socket.gethostname()))
    global terminating
    try:
        while not terminating:
            try:
                sock, addr = tcpserver.accept()
                sock.setblocking(1)
                tcplink(sock, addr)
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

def servertest(clientsnum):
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpserver.bind(('0.0.0.0', 8000))
    tcpserver.listen(5)
    print('Waiting for connections...')
    while not terminating:
        # accept a socket
        sock, addr = tcpserver.accept()
        # new threading to process TCP socket
        tcplink(sock, addr)


def main():
    from Interfaces.blueprints import blueprint_register
    serverListen = threading.Thread(target=servertest, args=(20,))
    serverListen.start()
    blueprint_register()
    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()


import requests
import time
import socket
import threading
terminating = False
isserver = False
sended = False


def postData():
    requests.post("http://localhost:5000/data", json={"data1": 123, "data2": [3, 4, 5, 6, 3]})


def sensorPost():
    global terminating
    terminating = False
    try:
        while not terminating:
            try:
                postData()
                time.sleep(0.1)
            except all:
                terminating = True
                print("unknown network error")
    except KeyboardInterrupt:
        print("Ctrl+C")
        terminating = True


def tcplink(sock, addr):
    global sended
    print("connected")
    global isserver
    # sock.send("Welcome!".encode())
    try:
        while not terminating:
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


def sensorTCP():
    global terminating
    tcpclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('localhost', 29989)
    tcpclient.settimeout(3000)
    tcpclient.connect(addr)
    tcpclient.setblocking(10)
    terminating = False
    t_sock = threading.Thread(target=tcplink, args=(tcpclient, addr))
    t_sock.setDaemon(True)
    t_sock.start()
    while True:
        time.sleep(1)


# 模拟传感器数据上传 通过POST
if __name__ == '__main__':
    # sensorPost()
    # sensorTCP()
    print('run')
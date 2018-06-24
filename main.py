from flask import Flask, request
import socket
import threading
import time
terminating = False
sended = False


app = Flask("test")

@app.route("/data", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        print(request.json)
        return "get new post"
    else:
        return "hello world"

def tcplink(sock, addr):
    print("connected")
    global sended
    # sock.send("Welcome!".encode())
    try:
        while not terminating:
            if not sended:
                sock.send("hello".encode())
                sended = True
            data = sock.recv(1024)
            if not data:
                continue
            print(data.decode())
            time.sleep(1)

    except Exception as e:
        print(e)
        # time.sleep(1)
        # sock.send("time: %f" % time.time())
    sock.close()
    print("Connection from %s:%s closed." % addr)
    sended = False

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

def severtest(clientsnum):
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpserver.bind("0,0,0,0", 8000)



if __name__ == '__main__':
    serverListen = threading.Thread(target=server, args=(20,))
    serverListen.start()
    app.run(host="0.0.0.0", port=5000)



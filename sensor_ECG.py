import time
import socket
import threading
import struct
import json

joinlist = (b'JN', 201801, b'E001', b'V002')
join_j = {'type': 'JN', 'username': 'admin', 'password': 'admin', 'clientID': 201810, 'ECGSensorID': 'E001',
          'VideoSensorID': 'V001'}

def sensorECG():
    tcpsensor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsensor.settimeout(2999)
    tcpsensor.connect(('localhost', 8000))
    # print(tcpsensor.recv(1024))
    datarecv = tcpsensor.recv(1024)
    print(datarecv)

    if datarecv == b'Connected struct!':
        joinbytes = struct.pack('>2sI4s4s', *joinlist)
        tcpsensor.send(joinbytes)
    elif datarecv == b'Connected!':
        joinjson = json.dumps(join_j)
        tcpsensor.send(joinjson.encode())
    data = tcpsensor.recv(1024)
    print(data)




if __name__ == '__main__':
    sensorECG()

import socket
import sys

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

svr_address = ('localhost', 10000)
sck.connect(svr_address)

try:
    message = input()
    sck.sendall(message)

    received = 0
    expect = len(message)

    while received < expect:
        data = sck.recv(16)
        received += len(data)
        print('received', data)

finally:
    sck.close()
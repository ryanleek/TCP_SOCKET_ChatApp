import socket

HEADERSIZE = 10
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

svr_address = ('localhost', 10000)
sck.connect(svr_address)

try:
    msg = input()
    #add messge length as size 10 header to msg
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    #send as bytes
    sck.send(bytes(msg,"utf-8"))

finally:
    sck.close()
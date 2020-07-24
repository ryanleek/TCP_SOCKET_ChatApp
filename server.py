import socket

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#setting address & port no.
svr_address = ('localhost', 10000)
sck.bind(svr_address)

sck.listen(1)

while True:
    #waiting for connection
    connection, clt_address = sck.accept()

    try:
        print('connection from', clt_address)

        while True:
            data = connection.recv(16)
            print('received', data)
            if data:
                connection.sendall(data)
            else:
                print('no more data')
                break
    
    finally:
        connection.close()



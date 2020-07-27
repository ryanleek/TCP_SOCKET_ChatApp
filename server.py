import socket

HEADERSIZE = 10
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#setting address & port no.
svr_address = ('localhost', 10000)
sck.bind(svr_address)

#socket goes to server mode
sck.listen(1)

while True:
    #waiting for connection
    connection, clt_address = sck.accept()

    try:
        print('connection from', clt_address)

        full_data = ''
        new_data = True

        while True:
            data = connection.recv(16)

            if new_data:
                data_len = int(data[:HEADERSIZE])
                new_data = False
            
            full_data += data.decode("utf-8")

            if len(full_data)-HEADERSIZE == data_len:
                print("full message:", full_data[HEADERSIZE:])
                new_data = True
    
    finally:
        #clean up connection
        connection.close()
import socket
import select

HEADERSIZE = 10
svr_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#setting address & port no.
svr_address = ('localhost', 10000)
svr_sck.bind(svr_address)

#socket goes to server mode
svr_sck.listen(1)

sockets = [svr_sck]
clients = {}

#get message from client and seperate header
def recieve_msg(clt_sck):
    try:
        header = clt_sck.recv(HEADERSIZE)

        if not len(header): #header length == 0
            return False

        msg_len = int(header.decode('utf-8').strip())

        return header, clt_sck.recv(msg_len)

    except:
        return False

while True:
    #blocking call, code execution stops and waits here
    read_sockets, _, exception_sockets = select.select(sockets, [], sockets)

    for sck in read_sockets:

        if sck == svr_address:  #new connection happened
            #accpet new connection
            clt_sck, clt_address = svr_sck.accept()

            sockets.append(clt_sck)

    try:
        print('connection from', clt_address)

        full_data = ''
        new_data = True

        while True:
            data = clt_sck.recv(16)

            if new_data:
                data_len = int(data[:HEADERSIZE])
                new_data = False
            
            full_data += data.decode("utf-8")

            if len(full_data)-HEADERSIZE == data_len:
                print("full message:", full_data[HEADERSIZE:])
                new_data = True
    
    finally:
        #clean up connection
        clt_sck.close()
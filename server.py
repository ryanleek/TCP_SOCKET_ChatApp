import socket
import select

HEADERSIZE = 10
IP = 'localhost'
PORT = 10000
#create server socket
svr_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
svr_sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#setting address & port no.
svr_sck.bind((IP, PORT))

#socket goes to server mode
svr_sck.listen()

sockets = [svr_sck]
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

#get message from client and seperate header
def recieve_msg(clt_sck):

    try:
        header = clt_sck.recv(HEADERSIZE)

        if not len(header): #header length == 0
            return False

        msg_len = int(header.decode('utf-8').strip())

        #return data and data size
        return {'header': header, 'data': clt_sck.recv(msg_len)}

    except:
        return False

while True:
    #blocking call, code execution stops and waits here
    read_sockets, _, exception_sockets = select.select(sockets, [], sockets)

    for sck in read_sockets:

        if sck == svr_sck:  #new connection happened
            #accpet new connection
            clt_sck, clt_address = svr_sck.accept()
            
            #recieve username
            user = recieve_msg(clt_sck)
            
            if not user:    #user quits before sending id
                continue
            
            #add socket and save client
            sockets.append(clt_sck)
            clients[clt_sck] = user

            print("new connection from {}:{}, username: {}".format(*clt_address, user['data'].decode('utf-8')))

        else:   #message from existing connection
            #recieve message
            msg = recieve_msg(sck)

            if not msg: #delete disconnected client
                print('connection with {} closed'.format(clients[sck]['data'].decode('utf-8')))
                
                #delete client's data and socket
                sockets.remove(sck)
                del clients[sck]

                continue
            
            #get user from client list
            user = clients[sck]

            print(f'received message from {user["data"].decode("utf-8")}: {msg["data"].decode("utf-8")}')

            #send message to other clients
            for clt_sck in clients:
                if clt_sck != sck:
                    clt_sck.send(user['header']+user['data']+msg['header']+msg['data'])
        
    # *It's not really necessary to have this, but will handle some socket exceptions just in case
    for sck in exception_sockets:

        # *Remove from list for socket.socket()
        sockets.remove(sck)

        # *Remove from our list of users
        del clients[sck]
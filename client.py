import socket
import sys

HEADERSIZE = 10
IP = 'localhost'
PORT = 10000
username = input("UserName: ")

#create client socket
clt_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to server
clt_sck.connect((IP, PORT))

#non-blocking connection 
clt_sck.setblocking(False)

#send user name to server
clt_id = username.encode('utf-8')
id_header = f"{len(clt_id):<{HEADERSIZE}}".encode('utf-8')
clt_sck.send(id_header + clt_id)

while True:

    #user input a message
    msg = input(f'{username} > ')

    #send message to server
    if msg: #if message is not empty
        msg = msg.encode('utf-8')
        msg_header = f"{len(msg):<{HEADERSIZE}}".encode('utf-8')
        clt_sck.send(msg_header + msg)

    try:
        #recieve message from server(refreshes everytime user sends a message)
        while True:
            #recieve sender's name header
            name_header = clt_sck.recv(HEADERSIZE)

            if not len(name_header):    #if no data is recieved(connection closed)
                print('connectionended by server')
                sys.exit()

            #recieve sender's name
            name_len = int(name_header.decode('utf-8').strip())
            sender = clt_sck.recv(name_len).decode('utf-8')

            #recieve message
            rmsg_header = clt_sck.recv(HEADERSIZE)
            rmsg_len = int(msg_header.decode('utf-8').strip())
            rmsg = clt_sck.recv(rmsg_len).decode('utf-8')

            #print message
            print(f'{sender} > {rmsg}')

    except IOError as e:
        continue
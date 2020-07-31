import socket
import sys
import time
from multiprocessing import Process
import threading

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

#message sending func. for th1
def send_msg(username, headersize, client_socket):
    while True:
        #user input a message
        msg = input(f'{username} > ')

        #send message to server
        if msg: #if message is not empty
            msg = msg.encode('utf-8')
            msg_header = f"{len(msg):<{headersize}}".encode('utf-8')
            client_socket.send(msg_header + msg)

#message recieving func. for th2
def recv_msg(headersize, client_socket):
    while True:
        try:
            #recieve message from server(refreshes everytime user sends a message)
            while True:
                #recieve sender's name header
                name_header = client_socket.recv(headersize)

                if not len(name_header):    #if no data is recieved(connection closed)
                    print('connectionended by server')
                    sys.exit()

                #recieve sender's name
                name_len = int(name_header.decode('utf-8').strip())
                sender = client_socket.recv(name_len).decode('utf-8')

                #recieve message
                rmsg_header = client_socket.recv(HEADERSIZE)
                rmsg_len = int(rmsg_header.decode('utf-8').strip())
                rmsg = client_socket.recv(rmsg_len).decode('utf-8')

                #print message
                print(f'{sender} > {rmsg}')

        except IOError as e:
            continue


th1 = threading.Thread(target=send_msg, args=(username, HEADERSIZE, clt_sck))

th2 = threading.Thread(target=recv_msg, args=(HEADERSIZE, clt_sck))

th1.start()
th2.start()

while True:
    time.sleep(1)
    pass



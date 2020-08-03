import socket
import sys
import time
import threading
from tkinter import*

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
def send_msg():
    #user's message
    msg = input_field.get()

    #send message to server
    if msg: #if message is not empty
        msg = msg.encode('utf-8')
        msg_header = f"{len(msg):<{HEADERSIZE}}".encode('utf-8')
        clt_sck.send(msg_header + msg)

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
                msg = f'{sender} > {rmsg}'
                msg_list.insert(END, msg)

        except IOError as e:
            continue

root = Tk()
root.title("Chatroom")

msg_frame = Frame(root)

scrollbar = Scrollbar(msg_frame)
msg_list = Listbox(msg_frame, height=15, width=50, yscrollcommand=scrollbar.set)

scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_frame.pack()

input_frame = Frame(root)

input_field = Entry(input_frame, width=47)
send_btn = Button(input_frame, text="send", command=send_msg)

send_btn.pack(side=RIGHT, fill=Y)
input_field.pack(side=LEFT, fill=BOTH)
input_frame.pack()

recv_thread = threading.Thread(target=recv_msg, args=(HEADERSIZE, clt_sck))
recv_thread.start()

root.mainloop()
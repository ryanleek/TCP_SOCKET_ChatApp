import socket
import sys
import time
import threading
from tkinter import*

HEADERSIZE = 10
IP = 'localhost'
PORT = 10000
username = input("UserName: ")

def enter_chat():
    IP = ip_input.get()
    PORT = port_input.get()
    username = name_input.get()

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

#message sending function activated by send button
def send_msg():
    #user's message
    msg = input_field.get()

    #send message to server
    if msg: #if message is not empty
        msg = msg.encode('utf-8')
        msg_header = f"{len(msg):<{HEADERSIZE}}".encode('utf-8')
        clt_sck.send(msg_header + msg)

#message recieving function for recieving thread
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

#Tkinter root
root = Tk()
#title of chat window
root.title("Chatroom")

start_frame = Frame(root)

ip_label = Label(start_frame, text='IP:')
ip_input = Entry(start_frame)
ip_label.pack(side=LEFT)
ip_input.pack(side=RIGHT)

port_label = Label(start_frame, text='PORT:')
port_input = Entry(start_frame)
port_label.pack(side=LEFT)
port_input.pack(side=RIGHT)

name_label = Label(start_frame, text='NAME:')
name_input = Entry(start_frame)
name_label.pack(side=LEFT)
name_input.pack(side=RIGHT)

enter_btn = Button(start_frame, text='Enter', command=enter_chat)
enter_btn.pack()

#msg_frame has scrollbar and msg_list in it
msg_frame = Frame(root)
#set scrollbar and msg_list in msg_frame
scrollbar = Scrollbar(msg_frame)
msg_list = Listbox(msg_frame, height=15, width=50, yscrollcommand=scrollbar.set)

#pack(show) msg_frame and it's components
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_frame.pack()

#input_frame has input_field and send_btn in it
input_frame = Frame(root)
#set input_field and send_btn in input_frame
input_field = Entry(input_frame, width=47)
send_btn = Button(input_frame, text='Send', command=send_msg)

#pack(show) input_frame and it's components
send_btn.pack(side=RIGHT, fill=Y)
input_field.pack(side=LEFT, fill=BOTH)
input_frame.pack()

#set and start thread for recieving messages
recv_thread = threading.Thread(target=recv_msg, args=(HEADERSIZE, clt_sck))
recv_thread.start()

#mainloop for Tkinter
root.mainloop()
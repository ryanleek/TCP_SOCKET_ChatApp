from tkinter import*

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
send_btn = Button(input_frame, text="send")

send_btn.pack(side=RIGHT, fill=Y)
input_field.pack(side=LEFT, fill=BOTH)
input_frame.pack()

root.mainloop()
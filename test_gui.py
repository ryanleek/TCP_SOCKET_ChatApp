from tkinter import*

root = Tk()

e = Entry(root, width=50)
e.pack()

def send():
    btn1 = Label(root, text=e.get())
    btn1.pack()

btn2 = Button(root, text="send", command=send)
btn2.pack()

root.mainloop()
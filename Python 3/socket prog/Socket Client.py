import socket
from tkinter import *
from tkinter import ttk
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
CONNECTED = False

def recievethread():
    #infinite loop so that function do not terminate and thread do not end.
    while CONNECTED:
        try:
            text = str(s.recv(4096), 'UTF-8')
            listbox.insert(END, text)
        except ConnectionResetError:
            s.close()
            break

def button_send(txt_box):
    text = txt_box.get()
    print(text)
    txt_box.delete(0, END)
    s.send(bytes(text, 'UTF-8'))

def button_connect(textbox_host, textbox_port):
    host = textbox_host.get()
    port = int(textbox_port.get())
    print(host, port)
    s.connect((host, port))
    CONNECTED = True
    start_new_thread(recievethread ,())

def button_disconnect(textbox_host, textbox_port):
    CONNECTED = False
    s.close()

root = Tk()
root.title("Python manyia")

frame_label_address = Frame(root)
frame_label_address.pack(side=TOP)

label = Label(frame_label_address, text='Host')
label.pack(side=LEFT, anchor=W)
label = Label(frame_label_address, text='Port')
label.pack(side=RIGHT, anchor=E)

frame_textbox_address = Frame(root)
frame_textbox_address.pack(side=TOP)

textbox_host = Entry(frame_textbox_address)
textbox_host.pack(side=LEFT)
textbox_port = Entry(frame_textbox_address)
textbox_port.pack(side=RIGHT)


frame_button_connect = Frame(root)
frame_button_connect.pack(side=TOP)

button = Button(frame_button_connect, text='Connect', command=lambda:button_connect(textbox_host, textbox_port))
button.pack(side=LEFT)
button = Button(frame_button_connect, text='Disconnect', command=lambda:button_disconnect(textbox_host, textbox_port))
button.pack(side=RIGHT)


label_1 = Label(root, text='Messages')
label_1.pack()

listbox = Listbox(root,selectmode=BROWSE)
listbox.pack(fill=X, padx=2)
txt_box_1 = Entry(root)
txt_box_1.pack(fill=X, padx=2, pady=(0, 2))
txt_box_1.bind("<Return>", lambda x:button_send(txt_box_1))

root.mainloop()  

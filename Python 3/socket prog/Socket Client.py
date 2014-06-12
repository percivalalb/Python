import socket
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
CONNECTED = False

def recievethread():
    #infinite loop so that function do not terminate and thread do not end.
    while CONNECTED:
        try:
            text = str(s.recv(1024), 'UTF-8')
            listbox.insert(END, text)
        except ConnectionResetError:
            s.close()
            break

def button_send(txt_box):
    text = txt_box.get()
    print(text)
    listbox.insert(END, text)
    listbox.itemconfig(END, {'bg':'lightgrey'}) 
    txt_box.delete(0, END)
    s.send(bytes(text, 'UTF-8'))

def button_connect_click(textbox_host, textbox_port, button_connect, button_disconnect):
    host = textbox_host.get()
    port = int(textbox_port.get())
    print(host, port)
    s.connect((host, port))
    global CONNECTED
    CONNECTED = True
    button_connect['state'] = 'disabled'
    button_disconnect['state'] = 'active'
    start_new_thread(recievethread ,())

def button_disconnect_click(textbox_host, textbox_port, button_connect, button_disconnect):
    CONNECTED = False
    button_connect['state'] = 'active'
    button_disconnect['state'] = 'disabled'
    global s
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = Tk()
root.title("Python manyia")

frame_label_address = Frame(root)
frame_label_address.pack(side=TOP)

label = Label(frame_label_address, text='Host')
label.pack(side=LEFT, fill=X)
label = Label(frame_label_address, text='Port')
label.pack(side=RIGHT, fill=X)

frame_textbox_address = Frame(root)
frame_textbox_address.pack(side=TOP)

textbox_host = Entry(frame_textbox_address)
textbox_host.pack(side=LEFT)
textbox_port = Entry(frame_textbox_address)
textbox_port.pack(side=RIGHT)


frame_button_connect = Frame(root)
frame_button_connect.pack(side=TOP)

button_connect = Button(frame_button_connect, text='Connect')
button_connect.pack(side=LEFT)
button_disconnect = Button(frame_button_connect, text='Disconnect', state='disabled')
button_disconnect.pack(side=RIGHT)

button_connect.config(command=lambda:button_connect_click(textbox_host, textbox_port, button_connect, button_disconnect))
button_disconnect.config(command=lambda:button_disconnect_click(textbox_host, textbox_port, button_connect, button_disconnect))


label_1 = Label(root, text='Messages')
label_1.pack()

listbox = Listbox(root,selectmode=BROWSE)
listbox.pack(fill=X, padx=2)
txt_box_1 = Entry(root)
txt_box_1.pack(fill=X, padx=2, pady=(0, 2))
txt_box_1.bind("<Return>", lambda x:button_send(txt_box_1))

def ok(top, e):
    print("value is", e.get())
    top.destroy()

top = Toplevel()

Label(top, text="Value").pack()

e = Entry(top)
e.pack(padx=5)

b = Button(top, text="OK", command=lambda:ok(top, e))
b.pack(pady=5)
#root.wait_window(top)
#result = messagebox.askquestion('foo', 'bar!')

root.mainloop()

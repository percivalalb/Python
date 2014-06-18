import socket
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from _thread import *
import atexit
import os
import savehandler
from savehandler import tagbase, tagint, tagstring, tagfloat, tagcompound, taglist

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
CONNECTED = False
FILE = os.getcwd() + '\\save.pfs'

def recievethread():
    #infinite loop so that function do not terminate and thread do not end.
    while CONNECTED:
        try:
            text = str(s.recv(1024), 'UTF-8')
            listbox.insert(END, text)
            listbox.yview(END)
        except ConnectionResetError:
            s.close()
            break
        except ConnectionAbortedError:
            s.close()
            break

def button_send(txt_box):
    text = txt_box.get()
    if text == '':
        return
    print(text)
    listbox.insert(END, text)
    listbox.itemconfig(END, {'bg':'lightgrey'})
    listbox.yview(END)
    txt_box.delete(0, END)
    s.send(bytes(text, 'UTF-8'))
def ok(top, button_name, button_colour):
    print("value is", button_name.get(), button_colour.get())
    top.destroy()

def button_connect_click(textbox_host, textbox_port, button_connect, button_disconnect, txt_box_1):
    host = textbox_host.get()
    port = int(textbox_port.get())


    top = Toplevel()
    top.transient(root)
    top.group(root)
    Label(top, text="Name").pack()

    e = Entry(top)
    e.pack(padx=5)
    Label(top, text="Colour").pack()
    button = Entry(top)
    button.pack(padx=5)
    
    b = Button(top, text="OK", command=lambda:ok(top, e, button))
    b.pack(pady=5)
    root.wait_window(top)
    
    print(host, port)
    tag_compound = tagcompound('test')
    tag_compound.setString('host', host)
    tag_compound.setInteger('port', port)
    savehandler.writeToFile(FILE, tag_compound)
    
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except ConnectionRefusedError:
        messagebox.showerror(title='Connection Error', message='Connection can\'t be made')
        return
    except socket.gaierror:
        messagebox.showerror(title='Connection Error', message='Connection is not real')
        return
    global CONNECTED
    CONNECTED = True
    button_connect['state'] = 'disabled'
    button_disconnect['state'] = 'active'
    txt_box_1['state'] = 'normal'
    start_new_thread(recievethread ,())

def button_disconnect_click(textbox_host, textbox_port, button_connect, button_disconnect, txt_box_1):
    CONNECTED = False
    button_connect['state'] = 'active'
    button_disconnect['state'] = 'disabled'
    txt_box_1['state'] = 'disabled'
    global s
    s.close()

tag_compound = savehandler.readFromFile(FILE)

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



label_1 = Label(root, text='Messages')
label_1.pack()

listbox = Listbox(root,selectmode=BROWSE)
listbox.pack(fill=X, padx=2)
txt_box_1 = Entry(root, state='disabled')
txt_box_1.pack(fill=X, padx=2, pady=(0, 2))
txt_box_1.bind("<Return>", lambda x:button_send(txt_box_1))
button_connect.config(command=lambda:button_connect_click(textbox_host, textbox_port, button_connect, button_disconnect, txt_box_1))
button_disconnect.config(command=lambda:button_disconnect_click(textbox_host, textbox_port, button_connect, button_disconnect, txt_box_1))

if tag_compound.hasTag('host'):
    textbox_host.insert(0, tag_compound.getTag('host').value)
if tag_compound.hasTag('port'):
    textbox_port.insert(0, tag_compound.getTag('port').value)

def prog_exit():
    print('exits')

atexit.register(prog_exit)

root.mainloop()

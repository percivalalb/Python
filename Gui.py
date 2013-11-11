from Tkinter import *
from ttk import Progressbar
import tkMessageBox
from threading import Thread
import Queue
import time
import os

class ThreadedClient:
    def __init__(self, master):
        self.master = master
        self.queue = Queue.Queue()
        self.running = True
        Thread(target = self.workerThread).start()
        self.periodicCall()
        
    def periodicCall(self):
        if self.running:
            self.master.after(100, self.periodicCall)
            
    def workerThread(self):
        while True:
            time.sleep(2)
        self.running = False

def hello():
   tkMessageBox.showinfo("Say Hello", "Hello World")


top = Tk()
top.title("Converter")
L1 = Label(top, text = "Hexadecimal", width=20)
L1.grid(row=0, column=0)
L2 = Label(top, text = "Binary", width=20)
L2.grid(row=0, column=1)
L3 = Label(top, text = "Decimal", width=20)
L3.grid(row=0, column=2)
progressBar = Progressbar(top, orient='horizontal', mode='determinate', length=240)
progressBar.grid(row=3, column = 1, columnspan = 2)

B1 = Button(top, text = "Say Hello", command = hello)
B1.grid(row=31, column=3)


E1 = Entry(top, bd = 3)

E1.grid(row=1, column=0)
E2 = Entry(top, bd = 3)
E2.grid(row=1, column=1)

E3 = Entry(top, bd = 3)
E3.grid(row=1, column=2)

top.mainloop()

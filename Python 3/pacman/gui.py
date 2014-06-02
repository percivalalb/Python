from tkinter import *
from tkinter import ttk
import socket
import os
import random
import atexit
import _thread as thread

from packet import packet, register_channel, write_packet, recive_packet
from datacomplier import dataoutput, datainput
from pfshandler import pfsbase, pfstagint, pfstagstring, pfstagfloat, pfstagcompound, pfstaglist

from constants import TICK_TIME, PACMAN_MOVE, PACMAN_SIZE
from packets import packetpacmanmove, packetpacmanset

COLOURS = ('#e49b0f', '#86db30', '#de3163', 'purple', 'blue')
CONTROLS = (('Left', 'Right', 'Up', 'Down'), ('a', 'd', 'w', 's'), ('4', '6', '8', '5'), ('f', 'h', 't', 'g'), ('j', 'l', 'i', 'k'), ('', '', '', ''))
SOCKET_CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a socket object
SOCKET_SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENTS = []
PACKETS = []
host = '192.168.0.25' #socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
print(host)
IS_CLIENT = True
IS_SERVER = False
TEXT_COUNTER = {}
MOUTH_COUNTER = {}
FULL_SCREEN = False
LAST_DIMENSIONS = 0
ITEM = 'wall'
GRID = []
FILE = os.getcwd() + '\\pacman.pfs'

class Pacman():

    def __init__(self, screen, colour, controls):
        self.reset_all()
        self.colour = colour
        self.screen = screen
        self.controls = controls
        self.speed_boost = 1.0
        self.key_down = [False, False, False, False]

    def reset_all(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def isOnlyKeyDown(self, index):
        i = 0
        for key in self.key_down:
            if i != index:
                if key:
                    return False
            i += 1
        return self.key_down[index]

    def keyPressed(self, event):
        key = event.keysym
        pacmen = self.screen.game.find_withtag("pacman:%s" % self.colour)
        walls = self.screen.game.find_withtag("wall")

        #if key in self.controls:
            #self.key_down[self.controls.index(key)] = True
        
        
        for pacman in pacmen:
            x1, y1, x2, y2 = self.screen.game.bbox(pacman)

            checkX1, checkY1, checkX2, checkY2 = x1, y2, x1, y2
            valid = 'none'

            if key == self.controls[0] and not self.left:
                valid = 'left'
                checkY1 -= PACMAN_MOVE - 1
                checkY2 -= PACMAN_SIZE + 1
            elif key == self.controls[1] and not self.right:
                valid = 'right'
                checkX1 += PACMAN_SIZE - 1
                checkX2 += PACMAN_MOVE + 1
            elif key == self.controls[2] and not self.up:
                valid =  'up'
                checkY1 -= PACMAN_MOVE - 1
                checkY2 -= PACMAN_SIZE + 1
                checkX1 -= PACMAN_MOVE - 1
                checkX2 -= PACMAN_SIZE + 1
            elif key == self.controls[3] and not self.down:
                checkX1 += PACMAN_SIZE - 1
                checkX2 += PACMAN_MOVE + 1
                valid = 'down'

            if valid != 'none':
                overlap = self.screen.game.find_overlapping(checkX1, checkY1, checkX2, checkY2)
                self.screen.game.create_rectangle((checkX1, checkY1, checkX2, checkY2), fill='white', outline = 'white')
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    setattr(self, valid, True)

    def keyReleased(self, event):
        key = event.keysym
        if key in self.controls:
            self.key_down[self.controls.index(key)] = False
    
    def movePacman(self, game):
        pacmen = game.find_withtag("pacman:%s" % self.colour)
        walls = game.find_withtag("wall")
        points = game.find_withtag("point")
        
        for pacman in pacmen:
            pac_coords = game.coords(pacman)
            if len(pac_coords) < 4:
                continue
                 
            if pac_coords[0] <= 0 - PACMAN_SIZE:
                game.move(pacman, game.winfo_width() + PACMAN_SIZE, 0)
                PACKETS.append(packetpacmanmove().set_pacman(self.colour).set_x_change(game.winfo_width() + PACMAN_SIZE).set_y_change(0).set_mouth_timer(-1))
            if pac_coords[1] <= 0 - PACMAN_SIZE:
                game.move(pacman, 0, game.winfo_height() + PACMAN_SIZE)
                PACKETS.append(packetpacmanmove().set_pacman(self.colour).set_x_change(0).set_y_change(game.winfo_height() + PACMAN_SIZE).set_mouth_timer(-1))
            if pac_coords[2] >= game.winfo_width() + PACMAN_SIZE:
                game.move(pacman, -game.winfo_width() - PACMAN_SIZE, 0)
                PACKETS.append(packetpacmanmove().set_pacman(self.colour).set_x_change(-game.winfo_width() - PACMAN_SIZE).set_y_change(0).set_mouth_timer(-1))
            if pac_coords[3] >= game.winfo_height() + PACMAN_SIZE:
                game.move(pacman, 0, -game.winfo_height() - PACMAN_SIZE)
                PACKETS.append(packetpacmanmove().set_pacman(self.colour).set_x_change(0).set_y_change(-game.winfo_height() - PACMAN_SIZE).set_mouth_timer(-1))

            x1, y1, x2, y2 = game.bbox(pacman)
            point = game.find_overlapping(x1, y1, x2, y2)
            for thing in point:
                if thing in points:
                    game.delete(thing)
                    game.create_text(pac_coords[0] + 20, pac_coords[1] - 20, fill=self.colour, font="Candara 15", text='+1 Point', tag='point_text')
                    self.speed_boost += 0.1

            moved = False
            
            if (self.left and not (self.key_down[2] and self.key_down[3])) or self.isOnlyKeyDown(0):
                x1, y1, x2, y2 = game.bbox(pacman)
                overlap = game.find_overlapping(x1 - PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.left = True
                    game.move(pacman, -PACMAN_MOVE * self.speed_boost, 0)
                    last = 0
                    if pacman in MOUTH_COUNTER.keys():
                        last = MOUTH_COUNTER[pacman]
             
                    if last % 30 < 30 / 2:
                        game.itemconfigure(pacman, start=200, extent=320)
                    else:
                        game.itemconfigure(pacman, start=220, extent=280)
                    MOUTH_COUNTER[pacman] = last + 1
                    PACKETS.append(packetpacmanmove().set_pacman(self.colour).set_x_change(-PACMAN_MOVE).set_y_change(0).set_mouth_timer(last))
            
            if (self.right and not (self.key_down[2] and self.key_down[3])) or self.isOnlyKeyDown(1):
                x1, y1, x2, y2 = game.bbox(pacman)
                overlap = game.find_overlapping(x1 + PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 + PACMAN_MOVE, y2 - PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.right = True
                    game.move(pacman, PACMAN_MOVE * self.speed_boost, 0)
                    last = 0
                    if pacman in MOUTH_COUNTER.keys():
                        last = MOUTH_COUNTER[pacman]
             
                    if last % 30 < 30 / 2:
                        game.itemconfigure(pacman, start=20, extent=320)
                    else:
                        game.itemconfigure(pacman, start=40, extent=280)
                    MOUTH_COUNTER[pacman] = last + 1
                    PACKETS.append(packetpacmanmove().set_pacman(self.colour).set_x_change(PACMAN_MOVE).set_y_change(0).set_mouth_timer(last))
            
            if (self.up and not (self.key_down[0] and self.key_down[1])) or self.isOnlyKeyDown(2):
                x1, y1, x2, y2 = game.bbox(pacman)
                overlap = game.find_overlapping(x1 + PACMAN_MOVE / 2, y1 - PACMAN_MOVE, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.up = True
                    game.move(pacman, 0, -PACMAN_MOVE * self.speed_boost)
                    last = 0
                    if pacman in MOUTH_COUNTER.keys():
                        last = MOUTH_COUNTER[pacman]
             
                    if last % 30 < 30 / 2:
                        game.itemconfigure(pacman, start=110, extent=320)
                    else:
                        game.itemconfigure(pacman, start=130, extent=280)
                    MOUTH_COUNTER[pacman] = last + 1
                    PACKETS.append(packetpacmanmove().set_pacman(self.colour).set_x_change(0).set_y_change(-PACMAN_MOVE).set_mouth_timer(last))

            if (self.down and not (self.key_down[0] and self.key_down[1])) or self.isOnlyKeyDown(3):
                x1, y1, x2, y2 = game.bbox(pacman)
                overlap = game.find_overlapping(x1 + PACMAN_MOVE / 2, y1 + PACMAN_MOVE, x2 - PACMAN_MOVE, y2 + PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.down = True
                    game.move(pacman, 0, PACMAN_MOVE * self.speed_boost)
                    last = 0
                    if pacman in MOUTH_COUNTER.keys():
                        last = MOUTH_COUNTER[pacman]
             
                    if last % 30 < 30 / 2:
                        game.itemconfigure(pacman, start=290, extent=320)
                    else:
                        game.itemconfigure(pacman, start=310, extent=280)
                    MOUTH_COUNTER[pacman] = last + 1
                    PACKETS.append(packetpacmanmove().set_pacman(self.colour).set_x_change(0).set_y_change(PACMAN_MOVE).set_mouth_timer(last))

class Controls():

    def __init__(self, screen):
        self.screen = screen
        self.pacmen = {}
        for colour in COLOURS:
            self.pacmen[colour] = Pacman(screen, colour, CONTROLS[COLOURS.index(colour)])

    def onLeftClick(self, event):
        x, y = self.screen.game.canvasx(event.x), self.screen.game.canvasy(event.y)
        point = self.screen.game.find_overlapping(x, y, x, y)
        for item in point:
            tags = self.screen.game.gettags(item)
            if 'deletable' in tags:
                self.screen.game.delete(item)

    def onRightClick(self, event):
        x, y = self.screen.game.canvasx(event.x), self.screen.game.canvasy(event.y)
        x1 = x % PACMAN_SIZE
        y2 = y % PACMAN_SIZE
        x -= x1
        y -= y2
        if ITEM.startswith('pacman:'):
            for colour in COLOURS:
                if ITEM == 'pacman:%s' % colour:
                    self.screen.game.createPacmanItem(x, y, colour, True)
        elif ITEM == 'wall':
            hi = self.screen.game.create_rectangle(x, y, x + PACMAN_SIZE, y + PACMAN_SIZE, fill='blue', tag=('wall', 'deletable'))
        elif ITEM == 'point':
            hi = self.screen.game.screen.game.create_oval(x + PACMAN_SIZE / 3, y + PACMAN_SIZE / 3, x - PACMAN_SIZE / 3 + PACMAN_SIZE, y - PACMAN_SIZE / 3 + PACMAN_SIZE, fill='white', tag=('point', 'deletable'))
            
    def onKeyPressed(self, event):
        for colour in self.pacmen.keys():
            self.pacmen[colour].keyPressed(event)
        
        if event.keysym == 'F11':
            global FULL_SCREEN
            global LAST_DIMENSIONS

            self.screen.parent.overrideredirect(not FULL_SCREEN)

            if FULL_SCREEN:
                self.screen.parent.geometry(LAST_DIMENSIONS)
            else:
                self.screen.parent.geometry("{0}x{1}+0+0".format(self.screen.parent.winfo_screenwidth(), self.screen.parent.winfo_screenheight()))

            FULL_SCREEN = not FULL_SCREEN
            LAST_DIMENSIONS = self.screen.parent.geometry()         
        elif event.keysym == 'Return':
            SOCKET_CLIENT.connect((host, port))
            thread.start_new_thread(self.clientLisinter, ())
        elif event.keysym == 'BackSpace':
            global IS_SERVER
            SOCKET_SERVER.bind((host, port))
            IS_SERVER = True
            thread.start_new_thread(self.waitForOtherClients, ())
        else:
            pass
           # for client in CLIENTS:
                #client.send(bytes('Thank you for connecting', 'UTF-8'))
    
    def waitForOtherClients(self):
        while len(CLIENTS) < 5:
            SOCKET_SERVER.listen(10)              # Now wait for client connection.
            c, addr = SOCKET_SERVER.accept()     # Establish connection with client.
            CLIENTS.append(c)
            set_packets = []
            for colour in COLOURS:
                pacmen = self.screen.game.find_withtag("pacman:%s" % colour)
                coords = self.screen.game.coords(pacmen)
                set_packets.append(packetpacmanset().set_pacman(colour).set_coords(coords))
            c.send(write_packet(set_packets))
            print(addr)

    def clientLisinter(self):
        #infinite loop so that function do not terminate and thread do not end.
        while True:
            try:
                recive_packet(SOCKET_CLIENT.recv(1024), self.screen)
            
            except ConnectionResetError:
                break
            
            
    def onKeyReleased(self, event):
        for colour in self.pacmen.keys():
            self.pacmen[colour].keyReleased(event)

    def movePacman(self, game):
        for colour in self.pacmen.keys():
            self.pacmen[colour].movePacman(game)

class Game(Canvas):

    def __init__(self, screen):
        Canvas.__init__(self, background='black', highlightthickness=0, cursor='dotbox')
        self.screen = screen

        self.points = 0
        self.gameover = False
        self.gamepaused = False
        self.createObjects()

    def createObjects(self):
        for colour in COLOURS:
            self.createPacmanItem(PACMAN_SIZE, PACMAN_SIZE, colour)

        count = 0
        for colour in COLOURS:
            key = 'pacman:%s' % colour
            id = self.create_rectangle((10, 10 + 25 * count, 30, 30 + 25 * count), fill=colour, tags=('palette', 'palette:%s' % key))
            self.tag_bind(id, "<Button-3>", lambda x: self.setItem(key))
            count += 1

        id = self.create_rectangle((10, 10 + 25 * count, 30, 30 + 25 * count), fill="blue", tags=('palette', 'palette:wall', 'palette:selected'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("wall"))
        count += 1
        id = self.create_rectangle((10, 10 + 25 * count, 30, 30 + 25 * count), fill="white", tags=('palette', 'palette:point'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("point"))
        self.itemconfigure('palette', width=5)
        self.itemconfigure('palette', outline='white')

    def createPacmanItem(self, x, y, colour, deletable = False):
        tags = []
        tags.append('pacman:%s' % colour)
        if deletable:
            tags.append('deletable')
            
        self.create_arc(x + 2, y + 2, x+PACMAN_SIZE - 2, y+PACMAN_SIZE - 2, start=30, extent=300, fill=colour, tag=tags)

    def setItem(self, item):
        global ITEM
        self.dtag('all', 'palette:selected')
        self.itemconfigure('palette', outline='white')
        self.addtag('palette:selected', 'withtag', 'palette:%s' % item)
        self.itemconfigure('palette:selected', outline='#999999')
        ITEM = item
      
    def movePacman(self):
        self.screen.controls.movePacman(self)

    def tickPointText(self):
        point_tags = self.find_withtag('point_text')
        for tag in point_tags:
            last = 0
            if tag in TEXT_COUNTER.keys():
                last = TEXT_COUNTER[tag]
             
            if last > 40:
                self.delete(tag)
            else:
                TEXT_COUNTER[tag] = last + 1

    def onTick(self):
        if self.gamepaused:
            return
         
        if not self.gameover:
            self.tickPointText()
            if IS_SERVER:
                self.movePacman()

            if len(PACKETS) > 0:
                data = write_packet(PACKETS)
                PACKETS.clear()
                if IS_SERVER:
                    for i in CLIENTS:
                        if i is not SOCKET_SERVER and i is not SOCKET_CLIENT: #i is not this server socket and i is not the socket the message was recived from
                            #print('packet size %d' % len(data))
                            i.send(data)
            
            self.screen.after(TICK_TIME, self.onTick)
        else:
            self.gameOver()  

    def gameOver(self):
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2,  text="Game Over", fill="white") 

    def gameExit(self):
        pass

class Screen(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent

        self.game = Game(self)
        self.controls = Controls(self)

        win = PanedWindow(parent, orient=VERTICAL)
        top = Label(win, text="top pane")
        win.add(top)
        #win.grid(row=0,column=0)
        win.pack(side="right", fill="both", expand = 0)
        self.game.config(width = 800, height = 650)
        
        self.game.pack(side="left", fill="both", expand = 0)
        #self.game.grid(column=0, row=1)
        
        self.parent.title("Pacman")
        #self.centerWindow(300, 200)

        register_channel('pacmanmove', packetpacmanmove)
        register_channel('pacmanset', packetpacmanset)
    
        self.after(TICK_TIME, self.game.onTick)
        self.bind_all("<KeyPress>", self.controls.onKeyPressed)
        self.bind_all("<KeyRelease>", self.controls.onKeyReleased)
        self.bind_all("<Button-1>", self.controls.onRightClick)
        self.bind_all("<B1-Motion>", self.controls.onRightClick)
        self.bind_all("<Button-3>", self.controls.onLeftClick)
        self.bind_all("<B3-Motion>", self.controls.onLeftClick)

    def centerWindow(self, frame_width, frame_height):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x = (screen_width - frame_width) / 2
        y = (screen_height - frame_height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (frame_width, frame_height, x, y))

    def screenExit(self):
        self.game.gameExit()
        print("ddawe")
        SOCKET.close()

root = Tk()
ex = Screen(root)
atexit.register(ex.screenExit)
root.mainloop() 

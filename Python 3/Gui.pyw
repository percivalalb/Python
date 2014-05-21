from tkinter import *
from tkinter import ttk
import os
import random
import atexit

from PFSHandler import PFSBase
from PFSHandler import PFSTagInt
from PFSHandler import PFSTagString
from PFSHandler import PFSTagFloat
from PFSHandler import PFSTagCompound
from PFSHandler import PFSTagList

TICK_TIME = 10
PACMAN_MOVE = 2
PACMAN_SIZE = 32
COLOURS = ('yellow', 'red', 'green')


TEXT_COUNTER = {}
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
        self.last_direction = 'none'

    def currentDirection(self):
        if self.left:
            return 'left'
        elif self.right:
            return 'right'
        elif self.up:
            return 'up'
        elif self.down:
            return 'down'
        else:
            return 'none'

    def setDirection(self, direction):
        self.reset_all()
        if direction == 'left':
            self.left = True
        elif direction == 'right':
            self.right = True
        elif direction == 'up':
            self.up = True
        elif direction == 'down':
            self.down = True

    def isOnlyKeyDown(self, index):
        i = 0
        for key in self.key_down:
            if i != index:
                if key:
                    return False
            i += 1
        if self.key_down[index]:
            print("dawe")
        return self.key_down[index]

    def keyPressed(self, event):
        key = event.keysym
        pacmen = self.screen.game.find_withtag("pacman:%s" % self.colour)
        walls = self.screen.game.find_withtag("wall")

        if key in self.controls:
            self.key_down[self.controls.index(key)] = True
        
        
        for pacman in pacmen:
            x1, y1, x2, y2 = self.screen.game.bbox(pacman)
            
            if key == self.controls[0] and not self.left:
                overlap = self.screen.game.find_overlapping(x1 - PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.left = True
            
            if key == self.controls[1] and not self.right:
                overlap = self.screen.game.find_overlapping(x1 + PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 + PACMAN_MOVE, y2 - PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.right = True
                
            if key == self.controls[2] and not self.up:
                overlap = self.screen.game.find_overlapping(x1 + PACMAN_MOVE / 2, y1 - PACMAN_MOVE, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.up = True
                
            if key == self.controls[3] and not self.down:
                overlap = self.screen.game.find_overlapping(x1 + PACMAN_MOVE / 2, y1 + PACMAN_MOVE, x2 - PACMAN_MOVE, y2 + PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.down = True

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
            if pac_coords[1] <= 0 - PACMAN_SIZE:
                game.move(pacman, 0, game.winfo_height() + PACMAN_SIZE)
            if pac_coords[2] >= game.winfo_width() + PACMAN_SIZE:
                game.move(pacman, -game.winfo_width() - PACMAN_SIZE, 0)
            if pac_coords[3] >= game.winfo_height() + PACMAN_SIZE:
                game.move(pacman, 0, -game.winfo_height() - PACMAN_SIZE)


            x1, y1, x2, y2 = game.bbox(pacman)
            point = game.find_overlapping(x1, y1, x2, y2)
            for thing in point:
                if thing in points:
                    game.delete(thing)
                    game.create_text(pac_coords[0] + 20, pac_coords[1] - 20, fill=self.colour, font="Candara 15", text='+1 Point', tag='point_text')
                    self.speed_boost += 0.1

            moved = False
            
            if (self.left or self.isOnlyKeyDown(0)):
                overlap = game.find_overlapping(x1 - PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.left = True
                    game.move(pacman, -PACMAN_MOVE * self.speed_boost, 0)
                    game.itemconfigure(pacman, start=210, extent=300)
            
            if (self.right or self.isOnlyKeyDown(1)):
                overlap = game.find_overlapping(x1 + PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 + PACMAN_MOVE, y2 - PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.right = True
                    game.move(pacman, PACMAN_MOVE * self.speed_boost, 0)
                    game.itemconfigure(pacman, start=30, extent=300)
            
            if (self.up or self.isOnlyKeyDown(2)):
                overlap = game.find_overlapping(x1 + PACMAN_MOVE / 2, y1 - PACMAN_MOVE, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.up = True
                    game.move(pacman, 0, -PACMAN_MOVE * self.speed_boost)
                    game.itemconfigure(pacman, start=120, extent=300)

            if (self.down or self.isOnlyKeyDown(3)):
                overlap = game.find_overlapping(x1 + PACMAN_MOVE / 2, y1 + PACMAN_MOVE, x2 - PACMAN_MOVE, y2 + PACMAN_MOVE)
                hasWall = False
                for thing in overlap:
                    if thing in walls:
                        hasWall = True
                if not hasWall:
                    self.reset_all()
                    self.down = True
                    game.move(pacman, 0, PACMAN_MOVE * self.speed_boost)
                    game.itemconfigure(pacman, start=300, extent=300)

class Controls():

    def __init__(self, screen):
        self.screen = screen
        self.pacman_yellow = Pacman(screen, 'yellow', ('Left', 'Right', 'Up', 'Down'))
        self.pacman_red = Pacman(screen, 'red', ('a', 'd', 'w', 's'))
        self.pacman_green = Pacman(screen, 'green', ('4', '6', '8', '5'))

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
        self.pacman_yellow.keyPressed(event)
        self.pacman_red.keyPressed(event)
        self.pacman_green.keyPressed(event)

    def onKeyReleased(self, event):
        self.pacman_yellow.keyReleased(event)
        self.pacman_red.keyReleased(event)
        self.pacman_green.keyReleased(event)

    def movePacman(self, game):
        self.pacman_yellow.movePacman(game)
        self.pacman_red.movePacman(game)
        self.pacman_green.movePacman(game)

class Game(Canvas):

    def __init__(self, screen):
        Canvas.__init__(self, background='black', highlightthickness=0)
        self.screen = screen
        
        self.points = 0
        self.gameover = False
        self.gamepaused = False
        self.createObjects()

    def createObjects(self):
        for colour in COLOURS:
            self.createPacmanItem(PACMAN_SIZE, PACMAN_SIZE, colour)


        id = self.create_rectangle((10, 10, 30, 30), fill="yellow", tags=('palette', 'palette:pacman:yellow'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("pacman:yellow"))
        id = self.create_rectangle((10, 35, 30, 55), fill="red", tags=('palette', 'palette:pacman:red'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("pacman:red"))
        id = self.create_rectangle((10, 60, 30, 80), fill="green", tags=('palette', 'palette:pacman:green'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("pacman:green"))
        id = self.create_rectangle((10, 85, 30, 105), fill="blue", tags=('palette', 'palette:wall', 'palette:selected'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("wall"))
        id = self.create_rectangle((10, 110, 30, 130), fill="white", tags=('palette', 'palette:point'))
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
            self.movePacman()
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

        self.game.grid(column=0, row=0, sticky=(N,W,E,S))
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        self.parent.title("Pacman")
        self.centerWindow(300, 200)

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

root = Tk()
ex = Screen(root)
atexit.register(ex.screenExit)
root.mainloop() 

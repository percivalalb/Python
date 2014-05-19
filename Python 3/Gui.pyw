from tkinter import *
from tkinter import ttk
import random

TICK_TIME = 10
PACMAN_MOVE = 2
PACMAN_SIZE = 32
TEXT_COUNTER = {}
ITEM = 'wall'

class Pacman():

    def __init__(self, screen):
        self.reset_all()

    def reset_all(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False

class Controls():

    def __init__(self, screen):
        self.screen = screen
        self.yellow_pacman = Pacman(screen)
        self.red_pacman = Pacman(screen)

    def onRightClick(self, event):
        x, y = self.screen.game.canvasx(event.x), self.screen.game.canvasy(event.y)
        x1 = x % PACMAN_SIZE
        y2 = y % PACMAN_SIZE
        x -= x1
        y -= y2
        if ITEM == "yellow_pacman":
            self.screen.game.create_arc(x, y, x + PACMAN_SIZE, y + PACMAN_SIZE, start=30, extent=300, fill='yellow', tag="pacman_yellow")
        elif ITEM == "red_pacman":
            self.screen.game.create_arc(x, y, x + PACMAN_SIZE, y + PACMAN_SIZE, start=30, extent=300, fill='yellow', tag="pacman_red")
        elif ITEM == "wall":
            hi = self.screen.game.create_rectangle(x, y, x + PACMAN_SIZE, y + PACMAN_SIZE, fill='blue', tag="wall")
        elif ITEM == "point":
            hi = self.screen.game.screen.game.create_oval(x + PACMAN_SIZE / 2, y + PACMAN_SIZE / 2, x + PACMAN_SIZE / 3 + PACMAN_SIZE / 2, y + PACMAN_SIZE / 3 + PACMAN_SIZE / 2, fill='white', tag="point")
            
    def onKeyPressed(self, event):
        key = event.keysym
        pac_yellow = self.screen.game.find_withtag("pacman_yellow")
        pac_red = self.screen.game.find_withtag("pacman_red")
        
        if key == "Left" and not self.yellow_pacman.left:
            self.yellow_pacman.reset_all()
            self.yellow_pacman.left = True
            self.screen.game.itemconfigure(pac_yellow, start=210, extent=300)
        
        if key == "Right" and not self.yellow_pacman.right:
            self.yellow_pacman.reset_all()
            self.yellow_pacman.right = True
            self.screen.game.itemconfigure(pac_yellow, start=30, extent=300)
            
        if key == "Up" and not self.yellow_pacman.up:
            self.yellow_pacman.reset_all()
            self.yellow_pacman.up = True
            self.screen.game.itemconfigure(pac_yellow, start=120, extent=300)
            
        if key == "Down" and not self.yellow_pacman.down:
            self.yellow_pacman.reset_all()
            self.yellow_pacman.down = True
            self.screen.game.itemconfigure(pac_yellow, start=300, extent=300)
            
        if key == "a" and not self.red_pacman.left:
            self.red_pacman.reset_all()
            self.red_pacman.left = True
            self.screen.game.itemconfigure(pac_red, start=210, extent=300)
        
        if key == "d" and not self.red_pacman.right:
            self.red_pacman.reset_all()
            self.red_pacman.right = True
            self.screen.game.itemconfigure(pac_red, start=30, extent=300)
        
        if key == "w" and not self.red_pacman.up:
            self.red_pacman.reset_all()
            self.red_pacman.up = True
            self.screen.game.itemconfigure(pac_red, start=120, extent=300)
            
        if key == "s" and not self.red_pacman.down:
            self.red_pacman.reset_all()
            self.red_pacman.down = True
            self.screen.game.itemconfigure(pac_red, start=300, extent=300)

class Game(Canvas):

     def __init__(self, screen):
        Canvas.__init__(self, background='black', highlightthickness=0)
        self.screen = screen

        self.points = 0
        self.gameover = False
        self.gamepaused = False
        self.createObjects()

     def createObjects(self):
        createPacmanItem(20)
        self.create_arc(20, 20, 20 + PACMAN_SIZE, 20 + PACMAN_SIZE, start=30, extent=300, fill='yellow', tag="pacman_yellow")

        self.create_arc(20, 20, 20 + PACMAN_SIZE, 20 + PACMAN_SIZE, start=30, extent=300, fill='red', tag="pacman_red")

        id = self.create_rectangle((10, 10, 30, 30), fill="yellow", tags=('palette', 'palette:yellow_pacman'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("yellow_pacman"))
        id = self.create_rectangle((10, 35, 30, 55), fill="red", tags=('palette', 'palette:red_pacman'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("red_pacman"))
        id = self.create_rectangle((10, 60, 30, 80), fill="blue", tags=('palette', 'palette:wall', 'palette:selected'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("wall"))
        id = self.create_rectangle((10, 85, 30, 105), fill="white", tags=('palette', 'palette:point'))
        self.tag_bind(id, "<Button-3>", lambda x: self.setItem("point"))
        self.itemconfigure('palette', width=5)
        self.itemconfigure('palette', outline='white')

     def createPacmanItem(self, x, y, color):
        self.create_arc(x, y, x+PACMAN_SIZE, y+PACMAN_SIZE, start=30, extent=300, fill='color', tag="pacman:" % color)

     def setItem(self, item):
        global ITEM
        self.dtag('all', 'palette:selected')
        self.itemconfigure('palette', outline='white')
        self.addtag('palette:selected', 'withtag', 'palette:%s' % item)
        self.itemconfigure('palette:selected', outline='#999999')
        ITEM = item
      
     def movePacman(self):
         pac_yellow = self.find_withtag("pacman_yellow")
         pac_coords = self.coords(pac_yellow)
         walls = self.find_withtag("wall")
         points = self.find_withtag("point")
         
         if pac_coords[0] <= 0 - PACMAN_SIZE:
            self.screen.parent.update()
            self.move(pac_yellow, self.screen.parent.winfo_width() + PACMAN_SIZE, 0)
         if pac_coords[1] <= 0 - PACMAN_SIZE:
            self.screen.parent.update()
            self.move(pac_yellow, 0, self.screen.parent.winfo_height() + PACMAN_SIZE)
         if pac_coords[2] >= self.screen.parent.winfo_width() + PACMAN_SIZE:
            self.screen.parent.update()
            self.move(pac_yellow, -self.screen.parent.winfo_width() - PACMAN_SIZE, 0)
         if pac_coords[3] >= self.screen.parent.winfo_height() + PACMAN_SIZE:
            self.screen.parent.update()
            self.move(pac_yellow, 0, -self.screen.parent.winfo_height() - PACMAN_SIZE)


         x1, y1, x2, y2 = self.bbox(pac_yellow)
         point = self.find_overlapping(x1, y1, x2, y2)
         for thing in point:
            try:
                points.index(thing)
                self.delete(thing)
                self.create_text(pac_coords[0] + 20, pac_coords[1] - 20, fill='yellow', font="Candara 15", text='+1 Point', tag='point_text')
            except ValueError:
                pass
         
         if self.screen.controls.yellow_pacman.left:
            overlap = self.find_overlapping(x1 - PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
            bools = True
            for thing in overlap:
                try:
                    walls.index(thing)
                    bools = False
                except ValueError:
                    pass
            if bools:
                self.move(pac_yellow, -PACMAN_MOVE, 0)    
        
         if self.screen.controls.yellow_pacman.right:
            overlap = self.find_overlapping(x1 + PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 + PACMAN_MOVE, y2 - PACMAN_MOVE)
            bools = True
            for thing in overlap:
                try:
                    walls.index(thing)
                    bools = False
                except ValueError:
                    pass
            if bools:
                self.move(pac_yellow, PACMAN_MOVE, 0)
        
         if self.screen.controls.yellow_pacman.up:
            overlap = self.find_overlapping(x1 + PACMAN_MOVE / 2, y1 - PACMAN_MOVE, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
            bools = True
            for thing in overlap:
                try:
                    walls.index(thing)
                    bools = False
                except ValueError:
                    pass
            if bools:
                self.move(pac_yellow, 0, -PACMAN_MOVE)

         if self.screen.controls.yellow_pacman.down:
            overlap = self.find_overlapping(x1 + PACMAN_MOVE / 2, y1 + PACMAN_MOVE, x2 - PACMAN_MOVE, y2 + PACMAN_MOVE)
            bools = True
            for thing in overlap:
                try:
                    walls.index(thing)
                    bools = False
                except ValueError:
                    pass
            if bools:
                self.move(pac_yellow, 0, PACMAN_MOVE)

         pac_red = self.find_withtag("pacman_red")
         pac_red_coords = self.coords(pac_red)
         x1, y1, x2, y2 = self.bbox(pac_red)
         point = self.find_overlapping(x1, y1, x2, y2)
         for thing in point:
            try:
                points.index(thing)
                self.delete(thing)
                self.create_text(pac_red_coords[0] + 20, pac_red_coords[1] - 20, fill='red', font="Candara 15", text='+1 Point', tag='point_text')
            except ValueError:
                pass
         
         if self.screen.controls.red_pacman.left:
            overlap = self.find_overlapping(x1 - PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
            bools = True
            for thing in overlap:
                try:
                    walls.index(thing)
                    bools = False
                except ValueError:
                    pass
            if bools:
                self.move(pac_red, -PACMAN_MOVE, 0)    
        
         if self.screen.controls.red_pacman.right:
            overlap = self.find_overlapping(x1 + PACMAN_MOVE, y1 + PACMAN_MOVE / 2, x2 + PACMAN_MOVE, y2 - PACMAN_MOVE)
            bools = True
            for thing in overlap:
                try:
                    walls.index(thing)
                    bools = False
                except ValueError:
                    pass
            if bools:
                self.move(pac_red, PACMAN_MOVE, 0)
        
         if self.screen.controls.red_pacman.up:
            overlap = self.find_overlapping(x1 + PACMAN_MOVE / 2, y1 - PACMAN_MOVE, x2 - PACMAN_MOVE, y2 - PACMAN_MOVE)
            bools = True
            for thing in overlap:
                try:
                    walls.index(thing)
                    bools = False
                except ValueError:
                    pass
            if bools:
                self.move(pac_red, 0, -PACMAN_MOVE)

         if self.screen.controls.red_pacman.down:
            overlap = self.find_overlapping(x1 + PACMAN_MOVE / 2, y1 + PACMAN_MOVE, x2 - PACMAN_MOVE, y2 + PACMAN_MOVE)
            bools = True
            for thing in overlap:
                try:
                    walls.index(thing)
                    bools = False
                except ValueError:
                    pass
            if bools:
                self.move(pac_red, 0, PACMAN_MOVE)

         if pac_red_coords[0] <= 0 - PACMAN_SIZE:
            self.screen.parent.update()
            self.move(pac_red, self.screen.parent.winfo_width() + PACMAN_SIZE, 0)
         if pac_red_coords[1] <= 0 - PACMAN_SIZE:
            self.screen.parent.update()
            self.move(pac_red, 0, self.screen.parent.winfo_height() + PACMAN_SIZE)
         if pac_red_coords[2] >= self.screen.parent.winfo_width() + PACMAN_SIZE:
            self.screen.parent.update()
            self.move(pac_red, -self.screen.parent.winfo_width() - PACMAN_SIZE, 0)
         if pac_red_coords[3] >= self.screen.parent.winfo_height() + PACMAN_SIZE:
            self.screen.parent.update()
            self.move(pac_red, 0, -self.screen.parent.winfo_height() - PACMAN_SIZE)
            
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
    
     def isOffScreen(self, coords):
         pass

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
        self.bind_all("<Key>", self.controls.onKeyPressed)
        self.bind_all("<Button-1>", self.controls.onRightClick)
        self.bind_all("<B1-Motion>", self.controls.onRightClick)

    def centerWindow(self, frame_width, frame_height):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x = (screen_width - frame_width) / 2
        y = (screen_height - frame_height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (frame_width, frame_height, x, y))

root = Tk()
ex = Screen(root)
root.mainloop() 

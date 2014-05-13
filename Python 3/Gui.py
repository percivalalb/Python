from tkinter import *
from tkinter import ttk

TICK_TIME = 15
PACMAN_MOVE = 2
PACMAN_SIZE = 32

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

    def onKeyPressed(self, e): 
        key = e.keysym
        print(key)
        pac_yellow = self.screen.game.find_withtag("pacman_yellow")
        pac_yellow_coords = self.screen.game.coords(pac_yellow)
        pac_red = self.screen.game.find_withtag("pacman_red")
        left = self.screen.game.find_overlapping(pac_yellow_coords[0] - PACMAN_SIZE, pac_yellow_coords[1], pac_yellow_coords[2] - PACMAN_SIZE, pac_yellow_coords[3])
        if key == "Left" and not self.yellow_pacman.left and not any(self.screen.game.index("wall") in code for code in left):
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
        Canvas.__init__(self, background="black", highlightthickness=0)
        self.screen = screen

        self.gameover = False
        self.gamepaused = False
        self.createObjects()

     def createObjects(self):
        self.create_arc(20, 20, 20 + PACMAN_SIZE, 20 + PACMAN_SIZE, start=30, extent=300, fill='yellow', tag="pacman_yellow")

        self.create_arc(20, 20, 20 + PACMAN_SIZE, 20 + PACMAN_SIZE, start=30, extent=300, fill='red', tag="pacman_red")

        for i in range(1):
            self.create_rectangle(60, 60, 60 + PACMAN_SIZE, 60 + PACMAN_SIZE, fill='blue', tag="wall")
        
     def movePacman(self):
         pac_yellow = self.find_withtag("pacman_yellow")
         pac_coords = self.coords(pac_yellow)

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

         
         if self.screen.controls.yellow_pacman.left: 
            self.move(pac_yellow, -PACMAN_MOVE, 0)    
        
         if self.screen.controls.yellow_pacman.right:
            self.move(pac_yellow, PACMAN_MOVE, 0)
        
         if self.screen.controls.yellow_pacman.up:
            self.move(pac_yellow, 0, -PACMAN_MOVE)

         if self.screen.controls.yellow_pacman.down:
            self.move(pac_yellow, 0, PACMAN_MOVE)

         pac_red = self.screen.game.find_withtag("pacman_red")
         if self.screen.controls.red_pacman.left: 
            self.move(pac_red, -PACMAN_MOVE, 0)   
        
         if self.screen.controls.red_pacman.right:
            self.move(pac_red, PACMAN_MOVE, 0)
        
         if self.screen.controls.red_pacman.up:
            self.move(pac_red, 0, -PACMAN_MOVE)

         if self.screen.controls.red_pacman.down:
            self.move(pac_red, 0, PACMAN_MOVE)


     def isOffScreen(self, coords):
         pass

     def onTick(self):
        if self.gamepaused:
            return
         
        if not self.gameover:
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

    def centerWindow(self, frame_width, frame_height):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x = (screen_width - frame_width) / 2
        y = (screen_height - frame_height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (frame_width, frame_height, x, y))

root = Tk()
ex = Screen(root)
root.mainloop()  

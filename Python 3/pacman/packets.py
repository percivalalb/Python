from packet import packet

class packetpacmanmove(packet):

    def __init__(self):
        packet.__init__(self, 'pacmanmove')

    def set_pacman(self, pacman):
        self.pacman = pacman
        return self

    def set_x_change(self, x_change):
        self.x_change = x_change
        return self

    def set_y_change(self, y_change):
        self.y_change = y_change
        return self

    def set_mouth_timer(self, mouth_timer):
        self.mouth_timer = mouth_timer
        return self
    
    def write(self, do):
        do.writeString(self.pacman)
        do.writeInteger(self.x_change)
        do.writeInteger(self.y_change)
        do.writeInteger(self.mouth_timer)
    
    def read(self, di):
        self.pacman = di.readString()
        self.x_change = di.readInteger()
        self.y_change = di.readInteger()
        self.mouth_timer = di.readInteger()
        
    def execute(self, screen):
        pacmen = screen.game.find_withtag("pacman:%s" % self.pacman)
        for pacman in pacmen:
            screen.game.move(pacman, self.x_change, self.y_change)
            if self.mouth_timer != -1:
                pass

class packetpacmanset(packet):

    def __init__(self):
        packet.__init__(self, 'pacmanset')

    def set_pacman(self, pacman):
        self.pacman = pacman
        return self

    def set_coords(self, coords):
        self.coords = coords
        return self
        
    def write(self, do):
        do.writeString(self.pacman)
        do.writeIntegerArray(self.coords)
    
    def read(self, di):
        self.pacman = di.readString()
        self.coords = di.readIntegerArray()

    def execute(self, screen):
        pacmen = screen.game.find_withtag("pacman:%s" % self.pacman)
        for pacman in pacmen:
            screen.game.coords(pacman, self.coords[0], self.coords[1], self.coords[2], self.coords[3])

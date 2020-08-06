# cmu_112_graphics is from diderot -> 15112 class!
# https://www.diderot.one/course/34/chapters/2847/
from cmu_112_graphics import *
import random
import time

class SandPile():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for i in range(self.cols)] for j in range(self.rows)]
    def solveSandPile(self):
        result = [[0 for i in range(self.cols)] for j in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] <= 3:
                    result[row][col] = self.grid[row][col]
        for row in range(self.rows):
            for col in range(self.cols):
                value = self.grid[row][col]
                if value >= 4:
                    result[row][col] += value-4
                    if row+1<self.rows:
                        result[row+1][col]+=1
                    if row-1>=0:
                        result[row-1][col]+=1
                    if col+1<self.cols:
                        result[row][col+1]+=1
                    if col-1>=0:
                        result[row][col-1]+=1
        self.grid = result        

class Block():
    #these make up the dragon
    #NORMAL blocks are generated right under head block...
    def __init__(self, app, x, y):
        self.app = app
        self.width = 20
        self.height = 20
        self.x = x
        self.y = y
        self.row = 12
        self.col = 8
        # self.gridX = self.x+self.width/2
        # self.gridY = self.y-self.height/2
        self.gridPosition = ()
        self.hasBeenHit = False
        self.onObstacle = False
    def slide(self):
        #move block
        self.x += 20
        #self.gridX += 20
        self.col+=1
    # def getGridPosition(self):
    #     #
    #     row = int(self.gridY//self.app.cellHeight)%15
    #     col = int(self.gridX//self.app.cellWidth)%15
    #     self.gridPosition = (row, col)
    def draw(self, canvas):
        cx = self.x-self.app.scrollX
        cy = self.y-self.app.scrollY
        canvas.create_rectangle(cx-self.width/2, cy-self.height/2, cx+self.width/2, cy+self.height/2, fill = "red")

class Head(Block):
    #the "dragon" block
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.breathingFire = False
    def breatheFire(self):
        self.breathingFire = True
    def draw(self, canvas):
        super().draw(canvas)
        cx = self.x-self.app.scrollX
        cy = self.y-self.app.scrollY
        canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill = "black")

class Dragon():
    def __init__(self, app):
        self.app = app
        self.lastTime = 0
        self.time = 0       
        self.blocks = [Head(self.app, self.app.width/2, self.app.height-50)]
        #self.gridPositions = []
    def spawnBlock(self):
        #add blocks to the tail
        if len(self.blocks)>=1:
            #coords of last elem
            x = self.blocks[-1].x
            y = self.blocks[-1].y
            #move all current blocks up by one block
            for block in self.blocks:
                block.y -= block.width
                #block.gridY -= block.width
                if block.row>0:
                    block.row-=1
            #add 40 to offset y from ground... 10 for block.width/2 & 30 for ground height -> y + 10 +self.app.ground.height
            self.blocks.append(Block(self.app, x, y))
    def checkGameOver(self):
        #if there are no more blocks (all blocks were hit)
        if len(self.blocks)==0 or not isinstance(self.blocks[0], Head):
            self.app.setActiveMode("gameOver")
    # def updateGridPositions(self):
    #     for block in self.blocks:
    #         if block.col!=self.app.cols-1:
    #             block.col+=1
    #         #block.getGridPosition()
    def slide(self):
        #dragon moving
        self.app.scrollX+=20
        #move all blocks
        for block in self.blocks:
            block.slide()
        #self.updateGridPositions()
        #self.collidesWithObstacle()
    def collidesWithObstacle(self):
        keepers = []
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            #print(block.gridPosition[0], block.gridPosition[1])
            # if self.app.grid[block.gridPosition[0]][block.gridPosition[1]-1] == None:
            #     keepers.append(block)
            if self.app.grid[block.row][block.col]==None:
                keepers.append(block)
            else:
                print("collided")
        self.blocks = keepers
        
    def draw(self, canvas):
        for block in self.blocks:
            block.draw(canvas)

class Obstacle():
    def __init__(self, app, row, col):
        self.app = app
        self.row = row
        self.col = col 


class BlockObstacle(Obstacle):
    def __init__(self, app, row, col, blocksWide=0, blocksHigh=0):
        super().__init__(app, row, col)
        if blocksWide==0 and blocksHigh==0:
            self.blocksWide = random.choice([1, 2, 3, 4])
            self.blocksHigh = random.choice([1, 2, 3])
            #self.fillBlockObstacles()
        else:
            self.blocksHigh = blocksHigh
            self.blocksWide = blocksWide
    def draw(self, canvas):
        x0 = self.col*self.app.cellWidth-self.app.scrollX
        y0 = self.row*self.app.cellHeight-self.app.scrollY
        x1 = x0+self.app.cellWidth
        y1 = y0+self.app.cellHeight
        canvas.create_rectangle(x0, y0, x1, y1, fill = "brown")
        #canvas.create_rectangle(cx-self.width/2, cy-self.height/2, cx+self.width/2, cy+self.height/2, fill = "brown")
    

class PlayMode(Mode):
    def appStarted(self):
        self.rows = 15
        self.cols = 1000
        self.sandPile = SandPile(self.rows, self.cols)
        for i in range(100):
            row = random.randrange(0, self.rows)
            col = random.randrange(0, self.cols)
            self.sandPile.grid[row][col] = random.randrange(100, 500)
        for i in range (0, 500):
            self.sandPile.solveSandPile()
        #print(self.sandPile.grid)
        self.timerCalls = 0
        self.scrollX = 0
        self.scrollY = 0
        self.cellScrolls = 0
        self.cellWidth = self.width/15
        self.cellHeight = self.height/self.rows
        self.grid = [[None for i in range(self.cols)] for j in range(self.rows)]
        #grid appends a block at start block
        #block literally spawns at the coord
        self.blckObst = BlockObstacle(self, 13, 12)
        self.dragon = Dragon(self)
        self.spawnObstacles()
    def spawnObstacles(self):
        #print("spawning....")
        for col in range(10, self.cols):
            row = random.randrange(0, 13)
            if self.sandPile.grid[row][col] == 3:
                #print("obj created!")
                obstacle = BlockObstacle(self, row, col)
                self.grid[row][col] = obstacle
               #   self.fillBlockObstacle(obstacle)
    def fillBlockObstacle(self, obstacle):
        for row in range(obstacle.blocksHigh-1):
            for col in range(obstacle.blocksWide-1):
                if not self.outOfBounds(row-1, col+1):
                    self.grid = BlockObstacle(self.app, row-1, col+1, 1, 1)

    def modeActivated(self):
        """
        populate game...
        """
        self.appStarted()
    def outOfBounds(self, row, col):
        if row > 12 or row < 0 or col > self.cols-1 or col < 0:
            return True
        return False
    def updateGrid(self):
        if self.scrollX//self.cellWidth > self.cellScrolls:
            self.cellScrolls += 1
            #shift obstacle filled blocks one cell left
            for row in range(self.rows-2):
                for col in range(self.cols):
                    if self.grid[row][col] != None:
                        if not self.outOfBounds(row, col-1):
                            self.grid[row][col-1] = self.grid[row][col]
                        self.grid[row][col] = None
    def keyPressed(self, event):
         if event.key == "Space":
            self.dragon.spawnBlock()
    def timerFired(self):
        self.timerCalls+=1
        #if self.timerCalls%5==0:
        self.dragon.collidesWithObstacle()
        self.dragon.slide()
        self.updateGrid()
        #self.spawnObstacles()
        self.dragon.checkGameOver()
    def redrawAll(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                val = self.grid[row][col]
                x0 = col*self.cellWidth
                y0 = row*self.cellHeight
                x1 = x0+self.cellWidth
                y1 = y0+self.cellHeight
                # if self.grid[row][col] == "blckObst":
                #     canvas.create_rectangle(x0, y0, x1, y1, fill = "brown")
                if row == 13:
                    canvas.create_rectangle(x0, y0, x1, y1, fill = "green")
                if row == 14:
                    canvas.create_rectangle(x0, y0, x1, y1, fill = "brown")
                canvas.create_rectangle(x0, y0, x1, y1, outline = "MistyRose2")
                if isinstance(val, BlockObstacle):
                    #print("draw")
                    self.grid[row][col].draw(canvas)
                if self.grid[row][col] != None:
                    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = "OBST")
        #self.blckObst.draw(canvas)
        self.dragon.draw(canvas)

class GameOverMode(Mode):
    def appStarted(self):
        pass
    def keyPressed(self, event):
        if event.key == "r":
            self.setActiveMode("play")
    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/2, text = "GAME OVER", fill = "red")
        canvas.create_text(self.width/2, self.height*3/4, text = "['r' to restart]", fill = "red")

class DragonBlockGame(ModalApp):
    #create modes...
    def appStarted(self):
        #self.addMode(StartMode(name="start"))
        self.addMode(PlayMode(name="play"))
        self.addMode(GameOverMode(name="gameOver"))
        #prolly add some more modes
        #set active mode to start
        self.setActiveMode("play")
        #self.setActiveMode("play")

DragonBlockGame()
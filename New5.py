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
        self.gridX = self.x+self.width/2
        self.gridY = self.y-self.height/2
        self.gridPosition = []
        self.setGridPosition()
        self.getGridPosition()
        # self.timer = 0
        self.fallingTimer = 0
        # self.row = row
        # self.col = col
    def slide(self):
        #move block
        self.x += 20
        self.gridX += 20
    def getGridPosition(self):
        return self.gridPosition
    def setGridPosition(self):     
        row = int(self.gridY//self.app.cellHeight)
        # print("row",row,self.gridY)
        # print("self.app.cellHeight",self.app.cellHeight)
        # print("int(self.gridY//self.app.cellHeight)%15",int(self.gridY//self.app.cellHeight)%15)
        col = int(self.gridX//self.app.cellWidth)
        # print("col",col,self.gridX)
        self.gridPosition = [row, col]
        #print("block.gridPosition ", self.y, self.height, self.gridY, self.gridPosition)
    def draw(self, canvas):
        cx = self.x-self.app.scrollX
        cy = self.y-self.app.scrollY
        canvas.create_rectangle(cx-self.width/2, cy-self.height/2, cx+self.width/2, cy+self.height/2, fill = "red")
        canvas.create_text(cx, cy, text = f"{self.gridPosition[0]}, {self.gridPosition[1]}")

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
        self.runTime = 0    
        self.startTime = 0  
        self.blocks = [Head(self.app, self.app.width/2, self.app.height-50)]
        self.isFalling = False
        self.positionCounter = 0

    def checkGameOver(self):
        #if there are no more blocks (all blocks were hit)
        if len(self.blocks)==0 or not isinstance(self.blocks[0], Head):
            self.app.setActiveMode("gameOver")
    def spawnBlock(self):
        #add blocks to the tail
        if len(self.blocks)>=1:
            #coords of last elem
            x = self.blocks[-1].x
            y = self.blocks[-1].y
            #move all current blocks up by one block
            for block in self.blocks:
                block.y -= block.width
                block.gridY -= block.height
                # if block.row>0:
                #     block.row-=1
            #add 40 to offset y from ground... 10 for block.width/2 & 30 for ground height -> y + 10 +self.app.ground.height
            self.blocks.append(Block(self.app, x, y))
    def updateGridPositions(self):
        for block in self.blocks:
            block.setGridPosition()
    def slide(self):
        self.positionCounter+=1
        #dragon moving
        self.app.scrollX+=20
        #NEW TODO
        self.app.cellScrolls+=1
        #move all blocks
        for block in self.blocks:
            block.slide()
        #if self.app.timerCalls%10==0:
        for knight in self.app.knights:
            #knight.col-=1
            if abs(knight.col-self.blocks[0].gridPosition[1]) <= 20:
                knight.updateMovesToMake()
        self.fall()
        self.updateGridPositions()
        # for ndx, block in enumerate(self.blocks):
        #     # print("self.app.cellHeight", self.app.cellHeight)
        #     print("block.gridPosition ", ndx, block.y, block.gridPosition)
        self.collidesWithObstacle()
    def collidesWithObstacle(self):
        keepers = []
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            #print(block.gridPosition[0], block.gridPosition[1])
            #8 b/c the dragon is always in the center of the screen
            if self.app.grid[block.gridPosition[0]][8] == None:
                keepers.append(block)
            # if self.app.grid[block.row][block.col]==None:
            #     keepers.append(block)
            else:
                print("collided")
                if isinstance(self.app.grid[block.gridPosition[0]][8], Knight):
                    print(self.app.grid[block.gridPosition[0]][8].row, self.app.grid[block.gridPosition[0]][8].col)
 
        self.blocks = keepers

        #self.updateDragon()
    def updateDragon(self):
        print("update called")
        #case where a bottom block is sliced
        if self.blocks[-1].gridPosition[0] != 12:
            for block in self.blocks:
                block.y+=20
                block.gridPosition[0]-=1
            #numBlocksDied = 
            self.isFalling = True
            #self.fall()
        # case where a middle block is sliced 
        for i in range(len(self.blocks)-1):
            print("in for")
            block = self.blocks[i]
            blockRow = block.gridPosition[0]
            #blockCol = block.gridPosition[1]
            if self.app.grid[blockRow+1][8] == None and block != self.blocks[-1]:
                print("got to if")
                goalRow = self.blocks[i+1].gridPosition[0]-1
                goalY = goalRow*self.app.cellHeight-self.app.cellHeight/2
                block.y = goalY
                block.gridPosition[0] = goalRow
                self.isFalling = True

    def fall(self):
        """
        Modified falling physics for better gaming experince
        Each block can only fall to the block below and the bottom
        block can only fall to the ground level.
        """
        if len(self.blocks)>0:
            # print("Total Block", len(self.blocks))
            prevBlock = None
            for ndx, block in enumerate(reversed(self.blocks)):
                # do not fall when obstacle is below
                okToFall = True
                row, col = block.getGridPosition()
                if row>0 and row<12:
                    objectBelow = self.app.grid[row+1][col]
                else:
                    objectBelow = None
                if isinstance(objectBelow, BlockObstacle): #TODO: Check other obstacle types
                    okToFall = False
                if ndx==0: # bottom block
                    level = 260
                    if block.y+block.height/2<level and okToFall:
                        if block.fallingTimer == 0:
                            dt = 0
                            block.fallingTimer = time.monotonic()
                        else:
                            dt = ((time.monotonic()-block.fallingTimer+1)*2)**2
                        if block.y+block.height/2+dt > level: # stop at the ground level
                            dt = level - (block.y+block.height/2)
                            block.y = block.y + dt
                            block.gridY += dt
                        else:
                            block.y = block.y + dt
                            block.gridY += dt
                    else:
                        block.fallingTimer = 0
                else: # all blocks above the bottom block
                    level = prevBlock.y-prevBlock.height/2
                    if prevBlock != None and block.y<prevBlock.y-block.height and okToFall:
                        if block.fallingTimer == 0:
                            dt = 0
                            block.fallingTimer = time.monotonic()
                        else:
                            dt = ((time.monotonic()-block.fallingTimer+1)*2)**2
                        if block.y+block.height/2+dt > level: # stop at the top of the block below
                            dt = level - (block.y+block.height/2)
                            block.y = block.y + dt
                            block.gridY += dt
                        else:
                            block.y = block.y + dt
                            block.gridY += dt
                    else:
                        block.fallingTimer = 0
                prevBlock = block

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

class Knight():
    def __init__(self, app, row, col):
        self.app = app
        self.row = row
        self.col = col
        self.r = 10
        self.movesToMake = []
        self.hasBeenClicked = False
        #self.updateMovesToMake()
    def solveBFS(self, currRow, currCol, goalRow, goalCol, numRows, numCols):
        previous = dict()
        for r in range(numRows):
            for c in range(numCols):
                previous[(r, c)] = None
        visited = []
        visited.append((currRow, currCol))
        queue = []
        queue.append((currRow, currCol))
        while len(queue)>0:
            position = queue.pop(0)
            if position == (goalRow, goalCol):
                path = []
                current = (goalRow, goalCol)
                while current != None:
                    path.append(current)
                    current = previous[current]
                return path
            dirs = [(-1,-1), (-1,0), (-1,1),
                    (0, -1),         (0, 1),
                    (1, -1), (1, 0), (1, 1)]
            for drow, dcol in dirs:
                newRow, newCol = position[0]+drow, position[1]+dcol
                if not(newRow < 0 or newRow > numRows-1 or newCol<0 or newCol>numCols-1) and (newRow, newCol) not in visited:
                    visited.append((newRow, newCol))
                    queue.append((newRow, newCol))
                    previous[(newRow, newCol)] = position
    def checkClicked(self, x, y):
        x0 = self.col*self.app.cellWidth-self.app.scrollX
        y0 = self.row*self.app.cellHeight-self.app.scrollY
        x1 = x0+self.app.cellWidth
        y1 = y0+self.app.cellHeight
        if x0<=x<=x1 and y0<=y<=y1:
            return True
    def updateMovesToMake(self):
        print("calleddd")
        self.movesToMake = self.solveBFS(self.row, self.col, self.app.dragon.blocks[0].gridPosition[0],\
                                                self.app.dragon.blocks[0].gridPosition[1]+3, self.app.rows, self.app.cols)
        if not self.movesToMake==None:
            for move in self.movesToMake:
                move = (move[0], move[1]-self.app.cellScrolls)
            print(self.movesToMake)
            self.movesToMake.pop()
    def move(self):
        #print("moving")
        #print(self.movesToMake)
        if self.movesToMake!= None and len(self.movesToMake)>0:
            move = self.movesToMake.pop()
            self.row = move[0]
            self.col = move[1]
    def draw(self, canvas):
        #print("knight drawn")
        x0 = self.col*self.app.cellWidth-self.app.scrollX
        y0 = self.row*self.app.cellHeight-self.app.scrollY
        x1 = x0+self.app.cellWidth
        y1 = y0+self.app.cellHeight
        canvas.create_oval(x0, y0, x1, y1, fill = "cornflower blue", outline = "")
    

class PlayMode(Mode):
    def appStarted(self):
        self.rows = 15
        self.cols = 500
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
        self.knights = []
        self.blckObst = BlockObstacle(self, 13, 12)
        self.dragon = Dragon(self)
        self.spawnObstacles()
        self.spawnKnight()
        # self.knight1 = Knight(self, 5, 50)
        # self.knight2 = Knight(self, 7, 80)
        # self.knight3 = Knight(self, 3, 200)
        # self.knights.append(self.knight1)
        # self.knights.append(self.knight2)
        # self.knights.append(self.knight3)
        # self.grid[5][15] = self.knight1
        # self.grid[7][80] = self.knight2
        # self.grid[3][200] = self.knight3
    def spawnObstacles(self):
        if True:
            print("spawning....")
            for col in range(10, self.cols):
                row = random.randrange(0, 13)
                if self.sandPile.grid[row][col] == 3: # obstacle
                    #print("obj created!")
                    length = random.randrange(1, 5)
                    height = random.randrange(1, 3)
                    lastRow = None
                    for i in range(0, height):
                        for j in range(0,length):
                            if row+i >= 0 and row+i < 13:
                                if lastRow != None and lastRow != 1:
                                    obstacle = BlockObstacle(self, row+i, col-j)
                                    self.grid[row+i][col-j] = obstacle
                                else:
                                    obstacle = BlockObstacle(self, row+i, col-j)
                                    self.grid[row+i][col-j] = obstacle
                                lastRow = row+i
                if self.sandPile.grid[row][col] == 2: # spikeobstacle
                    pass
                if self.sandPile.grid[row][col] == 1: # knight
                    pass
                if self.sandPile.grid[row][col] == 0: # trap
                    pass
    def spawnKnight(self):
        for col in range(self.dragon.blocks[0].gridPosition[1]+1, self.cols):
            if len(self.knights)<50:
                row = random.choice([3, 6, 9])
                if self.sandPile.grid[row][col] == 1:
                    #print("KNIGHT SPAWNED", row, col)
                    #print("dragon coords", self.dragon.blocks[0].gridPosition[0], self.dragon.blocks[0].gridPosition[1])
                    knight = Knight(self, row, col)
                    self.knights.append(knight)
                    self.grid[row][col] = knight
    def fillBlockObstacle(self, obstacle):
        for row in range(obstacle.blocksHigh-1):
            for col in range(obstacle.blocksWide-1):
                if not self.outOfBounds(row-1, col+1):
                    self.grid = BlockObstacle(self.app, row-1, col+1, 1, 1)
    # def checkKnightsValid(self):
    #     keepers = []
    #     for i in range(len(self.knights)-1):
    #         knight = self.knights[i]
    #         if knight.movesToMake != [] or knight.col >= self.dragon.blocks[0].gridPosition[1]:
    #             keepers.append(knight)
    #     self.knights = keepers

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
        # if self.scrollX//self.cellWidth > self.cellScrolls:
        #     self.cellScrolls += 1
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
        if event.key == 'h':
            self.setActiveMode("help")
    def mousePressed(self, event):
        keepers = []
        for knight in self.knights:
            if not knight.checkClicked(event.x, event.y):
                keepers.append(knight)
            else:
                print("knight has been killed")
        self.knights = keepers
    def timerFired(self):
        self.timerCalls+=1
        #if self.timerCalls%5==0:
        #self.dragon.collidesWithObstacle()
        self.dragon.slide()
        self.updateGrid()
        #self.spawnObstacles()
        # if self.dragon.isFalling:
        #     self.dragon.fall()
        self.dragon.checkGameOver()
        #self.spawnKnight()
        #self.checkKnightsValid()
        for knight in self.knights: 
            #if abs(knight.col-self.dragon.blocks[0].gridPosition[1])<=20:
            knight.move()
        # if self.timerCalls%50==0:
        #     if len(self.knights)>0:
        #         self.knights.pop()
    def redrawAll(self, canvas):
        if len(self.dragon.blocks) > 0:
            dragonRow, dragonCol = self.dragon.blocks[0].getGridPosition()
        print("dragon col", dragonCol)
        for row in range(self.rows):
            #for col in range(max(0,self.dragon.positionCounter-50), self.dragon.positionCounter+50):
            for col in range(self.cols):
                val = self.grid[row][col]
                #print(val)
                x0 = col*self.cellWidth-self.scrollX
                y0 = row*self.cellHeight
                x1 = x0+self.cellWidth
                y1 = y0+self.cellHeight
                # if self.grid[row][col] == "blckObst":
                #     canvas.create_rectangle(x0, y0, x1, y1, fill = "brown")
                if row == 13:
                    canvas.create_rectangle(x0, y0, x1, y1, fill = "green", outline = "")
                if row == 14:
                    canvas.create_rectangle(x0, y0, x1, y1, fill = "brown", outline = "")
                canvas.create_rectangle(x0, y0, x1, y1, outline = "MistyRose2")
                if val!=None:
                    #print("draw")
                    val.draw(canvas)
                # if self.grid[row][col] != None:
                #     canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f"{row}, {col}")
        #self.blckObst.draw(canvas)
        self.dragon.draw(canvas)

class GameOverMode(Mode):
    def appStarted(self):
        pass
    def keyPressed(self, event):
        if event.key == "r":
            self.setActiveMode("play")
    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = "red")
        canvas.create_text(self.width/2, self.height/2, text = "YOU DIED", font = f"Arial 25 bold")
        canvas.create_text(self.width/2, self.height*3/4, text = "['r' to restart]", font = f"Times 15")

class LoadingMode(Mode):
    def appStarted(self):
        self.dotList = [[190, "azure"], [210, "orange"], [230, "orange"]]
        self.timerCalls = 0
    def changeColors(self):
        if self.dotList[0][1] == "azure":
            self.dotList[0][1] = "orange"
            self.dotList[1][1] = "azure"
        elif self.dotList[1][1] == "azure":
            self.dotList[1][1] = "orange"
            self.dotList[2][1] = "azure"
        elif self.dotList[2][1] == "azure":
            self.dotList[2][1] = "orange"
            self.dotList[0][1] = "azure"

    def timerFired(self):
        self.timerCalls +=1
        if self.timerCalls%5==0:
            self.changeColors()

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = "azure")
        canvas.create_text(self.width/2.3, self.height/2, text = "Loading", font = f"Helvetica{17}bold", fill = "orange")
        for dot in self.dotList:
            #print(dot)
            canvas.create_oval(dot[0]-3, self.height/1.92-3, dot[0]+3, self.height/1.92+3, fill = dot[1], outline = "")

class StartMode(Mode):
    def appStarted(self):
        pass
    def keyPressed(self, event):
        if event.key=="Space":
            self.setActiveMode("play")
        if event.key=="h":
            self.setActiveMode("help")
    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = "azure")
        canvas.create_text(self.width/2, self.height/2.7, text = "Welcome to Dragonblock!",font = f"Helvetica{17}bold", fill = "orange")
        canvas.create_text(self.width/2, self.height/1.7, text = ">> 'h' for help \n(press anytime while playing)!\n>> 'Space' to start game!",font = f"Helvetica{11}bold")
        canvas.create_text(self.width/2, self.height/1.2, text = "**Please note that the game \nwill take a while to start\n after pressing space**",font = f"Helvetica{15}", fill = "red")
        
class HelpMode(Mode):
    def appStarted(self) -> None:
        """
        Set up help book
        """
        self.cover = Cover(self, "Instructions", "Hello! I hope you are having fun!\n> Press 'n' for more information\n> Press 'Space' to return to game")
        self.pg1 = Page(self, "Avoid hitting blocks!\nAlso avoid the blue knights which find you!\nPress 'Space' to generate blocks under you\n>> Press 'Space' to go back and start game!")
        #self.pg2 = Page(self, "Hint! Click anywhere on the screen to generate small food.\nClick on any food to increase it's point value!\n> Press 'b' for previous page\n> Press 'space bar' to return to game!")
        self.pgList = [self.cover, self.pg1]
        #initialize book
        self.book = Book(self, "Help Manual", self.pgList)


    def keyPressed(self, event) -> None:
        """
        keys to get back to game, and go through help book
        """
        if event.key == "Space":
            self.app.setActiveMode("play")

        # next page
        if event.key == "n":
            self.book.flipForward()


    def redrawAll(self, canvas) -> None:
        """
        draw help book
        """
        self.book.renderBook(canvas)

class DragonBlockGame(ModalApp):
    #create modes...
    def appStarted(self):
        #self.addMode(StartMode(name="start"))
        self.addMode(PlayMode(name="play"))
        self.addMode(GameOverMode(name="gameOver"))
        self.addMode(StartMode(name="start"))
        self.addMode(HelpMode(name="help"))
        #self.addMode(LoadingMode(name="loading"))
        #prolly add some more modes
        #set active mode to start
        self.setActiveMode("start")
        #self.setActiveMode("play")


###################################################################################
#Books -> hw 9
###################################################################################

class Page():
    def __init__(self, app, words):
        """
        initialize string of words in page
        """
        self.words = words
        self.app = app
    def getWordCount(self):
        """
        get # words on page
        """
        # list of separate words + get the lenght of this list
        return len(self.words.split(" "))
    def getCharCount(self):
        """
        get # characters (including whitespace) on page
        """
        countChar = 0
        for word in self.words:
            for char in word:
                #increment countChar everytime there is a character in a word in words
                countChar += 1
        return countChar
    def __repr__(self):
        """
        string of words on page
        """
        return self.words
    def __eq__(self, other):
        """
        tests equality of Page to other Page or str
        (compares the words on page)
        """
        #case where other is a Page
        if isinstance(other, Page):
            return self.words == other.words
        #case where other is a string
        if isinstance(other, str):
            return self.words == other
    def __add__(self, other):
        """
        adds a Page to another Page or a string to a Page
        concatenates the words to more words
        """
        # case where other is a Page
        if isinstance(other, Page):
            return Page(self.words + other.words)
        # case where other is a string
        if isinstance(other, str):
            return Page(self.words + other)
    def __contains__(self, other):
        """
        sees if a string is in the words on page
        """
        return other in self.words 
    def lines(self, pageWidth):
        """
        splits words on page over a certain length without splitting words
        """
        #to be returned
        wordList = []
        count = 0
        #the phrases whithin the list
        partialPhrase = ""
        for word in self.words.split(" "):
            # count adds on the length of word
            count += len(word)
            if(count <= pageWidth):
                # add space if count still within bounds given
                partialPhrase += word + " "
                count += 1
            else:
                # if count is already out of bounds, delete the extra whitespace
                if(partialPhrase[len(partialPhrase)-1] == " "):
                    partialPhrase = partialPhrase[:-1]
                # add partial phrase to wordList
                wordList.append(partialPhrase)
                #set partialPhrase to the word
                partialPhrase = word + " "
                count = len(partialPhrase)
        #get rid of whitespace at the end
        if(partialPhrase[len(partialPhrase)-1] == " "):
            partialPhrase = partialPhrase[:-1]
        wordList.append(partialPhrase)
        return wordList
    def render(self, canvas) -> None:
        """
        Draws word content
        """
        canvas.create_text(self.app.width/2 ,self.app.height/2, text = self.words, font = f"Times 13")
        
class Cover(Page):
    def __init__(self, app, title, words):
        """
        initializes words on page (same as in parent class)
        Also has a title
        """
        super().__init__(app, words)
        self.title = title
    def __repr__(self):
        """
        Overrides parent method
        string of ttile instead of words on pg
        """
        return self.title
    def render(self, canvas) -> None:
        """
        Draws title and page content
        """
        canvas.create_text(self.app.width/2, self.app.height/3, text = self.title, font = "Times 20 italic", fill = "SteelBlue1")            
        super().render(canvas)

class Book():
    def __init__(self, app, title, pages):
        """
        sets title, pages, and current page
        """
        self.title = title
        self.pages = pages
        self.currPg = 0
        self.app = app
    def __len__(self):
        """
        returns num pages
        """
        return len(self.pages)
    def getWordCount(self):
        """
        counts total words in all pages in book
        """
        wordCount = 0
        for pg in self.pages:
            # get wordCount for each page & add to total
            wordCount += pg.getWordCount()
        return wordCount
    def getCharCount(self):
        """
        Count the characters in all words in all pages of book
        """
        charCount = 0
        for pg in self.pages:
            # get charCound for each page and add to total
            charCount += pg.getCharCount()
        return charCount
    def getCurrentPage(self):
        """
        gets the page of the book that obj is on
        """
        #return page at current page
        return self.pages[self.currPg]
    def __repr__(self):
        """
        returns string with title and num pages
        """
        return self.title + " [" + str(len(self.pages)) + " pgs]"
    def __eq__(self, other):
        """
        checks for equality between book and list
        compares the pages
        """
        #case where other is Book
        if isinstance(other, Book):
            return self.pages == other.pages
        # case where other is list
        if isinstance(other, list):
            return self.pages == other
    def __add__(self, other):
        """
        Adds book to book, book to page, book to str
        Returns new book with combined pages
        """
        #case where other is BOok
        if isinstance(other, Book):
            return Book(self.title, self.pages + other.pages)
        #case where other is Page
        if isinstance(other, Page):
            return Book(self.title, self.pages + [other])
        # cacse where other is string
        if isinstance(other, str):
            return Book(self.title, self.pages + [Page(other)])
    def flipBackward(self):
        """
        goes back a page
        """
        #don't do if no more pgs to flip back on
        if self.currPg == 0:
            return False
        self.currPg -=1
        return True
    def flipForward(self):
        """
        goes to next page
        """
        self.currPg += 1
        #don't do if at end of book
        if(self.currPg == len(self.pages)):
            self.currPg -=1
            return False
        return True
    def __contains__(self, other):
        """
        checks if a certain string is anywhere in the book's pages
        """
        for page in self.pages:
            # checks if other is in each page
            if other in page.words:
                return True
        return False
    def renderBook(self, canvas) -> None:
        """
        Draws title and pages
        """
        canvas.create_text(self.app.width/3, self.app.width/5, text = self.title, font = f"Arial 25 bold", underline = True, fill = "pale violet red")
        self.pages[self.currPg].render(canvas)

DragonBlockGame()
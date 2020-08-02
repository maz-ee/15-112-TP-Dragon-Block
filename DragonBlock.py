#############################################
# DRAGON BLOCK GAME!
# TP 15-112
# Morgan Zhang
# morganz
#############################################

from cmu_112_graphics import *
import random

#############################################
# Dragon & it's tail
#############################################
class Dragon():
    def __init__(self, app):
        #dragon has width of 20
        self.height = 20
        self.width = 20
        self.app = app
        self.x = self.app.width/2
        self.y = self.app.height-30
        self.breathingFire = False
        self.timerCalls = 0
        self.fireTime = 0
        self.fire = Fire(self.app, self.x, self.y)
        self.Tail = Tail(self.app, self.x, self.y)
    def moveHead(self, factor):
        self.y+= self.height*factor
        self.fire.updateFirePosition(self.x, self.y)
    def slide(self):
        """
        automatically slide horizontally...
        """
        self.x += 5
        self.app.scrollX += 5
        self.Tail.slideTail()
        self.fire.updateFirePosition(self.x, self.y)

    def fly(self, dx, dy):
        """
        for when its flying time
        """
        self.x += dx
        self.y += dy
        self.app.scrollX += dx
        self.app.scrollY += dy
    def breatheFire(self):
        self.breathingFire = True
    def drawDragon(self, canvas):
        if self.breathingFire:
            self.fire.drawFire(canvas)
        self.Tail.drawTail(canvas)
        cx = self.x-self.app.scrollX
        cy = self.y-self.app.scrollY
        canvas.create_rectangle(cx-self.width/2, cy-self.height/2, cx+self.width/2, cy+self.height/2, fill = "red")
        #eye to indicate that this is the dragon block
        canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill = "black")

class TailBlock():
    def __init__(self, app, x, y):
        """
        tail block spawns right under dragon head -> same y
        """
        self.app = app
        self.x = x
        self.y = y
        self.hasBeenHit = False
    def slideBLock(self):
        if not self.hasBeenHit:
            self.x+=5
    def drawBlock(self, canvas):
        cx = self.x-self.app.scrollX
        cy = self.y-self.app.scrollY
        canvas.create_rectangle(cx-10, cy-10, cx+10, cy+10, fill = "red")

class Tail():
    def __init__(self, app, x, y):
        self.app = app
        self.blocks = []
        self.x = x
        self.y = y
    def spawnBlock(self):
        self.blocks.append(TailBlock(self.app, self.app.dragon.x, self.app.dragon.y))
        self.app.dragon.moveHead(-1)
        print(len(self.blocks))
    def shorten(self):
        blocksHitCount = 0
        remainingBlocks = []
        for block in self.blocks:
            if block.hasBeenHit:
                blocksHitCount += 1
            else:
                remainingBlocks.append(block)
        for i in range(len(remainingBlocks)-1):
            if remainingBlocks[i+1].y-remaningBlocks[i].y > 20:
                for j in range(i+1, len(remainingBlocks)):
                    remainingBlocks[j].y-=20*blocksHitCount
        self.blocks = remainingBlocks
        self.app.dragon.moveHead(blocksHitCount)
    def slideTail(self):
        for block in self.blocks:
            block.slideBlock()
    def drawTail(self, canvas):
        for block in self.blocks:
            block.drawBlock(canvas)

class Fire():
    def __init__(self, app, x, y):
        self.app = app
        self.power = 10
        self.size = 25
        self.range = 50
        #x, y represent the corner coming from the bird
        self.x = x+10
        self.y = y+10
        self.lowerLeftX = 0
        self.lowerLeftY = 0
        self.upperRightX = 0
        self.upperRightY = 0
        self.isSelected = False
        self.resetCoords()
    def resetCoords(self):
        self.lowerLeftX = self.x+self.range
        self.lowerLeftY = self.y-self.size/2
        self.upperRightX = self.x+self.range
        self.upperRightY = self.y+self.size/2
    def updateFirePosition(self, x, y):
        self.x = x+10
        self.y = y+10
    def levelUp(self):
        self.power += 10
        self.size += 10
        self.range += 20
    def selectFire(self):
        self.isSelected = True
    def angle(self, x, y):
        # n1 = math.sqrt(origX**2+origY**2)
        # n2 = math.sqrt(c**2+y**2)
        # angle = math.arccos((orgX*x+origY*y)/(n1*n2))
        #newY = sin
        #newX = cos
        self.lowerLeftX = x-self.range
        self.lowerLeftY = y-self.size/2
        self.upperRightX = x+self.range
        self.upperRightY = y+self.size/2
    def drawFire(self, canvas):
        cx = self.x-self.app.scrollX
        cy = self.y-self.app.scrollY
        canvas.create_polygon(cx, cy, self.lowerLeftX-self.app.scrollX, self.lowerLeftY-self.app.scrollY, self.upperRightX-self.app.scrollX, self.upperRightY-self.app.scrollY, fill = "orange", onClick = self.selectFire)

#############################################
# Obstacles
#############################################
class Obstacle():
    def __init__(self, app, x, y):
        pass

#############################################
# Knights
#############################################

#############################################
# Course
#############################################

#############################################
# Everyting? -> idek
#############################################
class PlayMode(Mode):
    def appStarted(self):
        """
        will have
            - a dragon
            - obstacles
            - knights
            - coords
            - coins
            - score
            - highscore
        """
        self.scrollX = 0
        self.scrollY = 0
        self.dragon = Dragon(self)
        self.timerCalls = 0
    def modeActivated(self):
        """
        populate game...
        """
        pass
    def modeDeactivated(self):
        """
        when dragon dies?
        """
        pass
    def keyPressed(self, event):
        """
        will have
            - build blocks with "Space"
            - breathe fire with "f"
            - navigate flying with arrow keys
            - p to pause, help screen pops up?
            - r to resume...?
        """
        if event.key == "Space":
            self.dragon.Tail.spawnBlock()
        if event.key == "f":
            self.dragon.breatheFire()
    def mousePressed(self, event):
        """
        click anywhere on screen to generate blocks
        maybe click and drag to angle fire at knights?
        """
        if not self.dragon.fire.isSelected:
            self.dragon.Tail.spawnBlock()
            
    def mouseDragged(self, event):
        if self.dragon.fire.isSelected:
            self.dragon.fire.angle(event.x, event.y)
    def mouseReleased(self, event):
        self.dragon.fire.isSelected = False
    def timerFired(self):
        self.timerCalls += 1
        #fire only lasts for 2.5 seconds
        if self.dragon.breathingFire:
            self.dragon.fireTime += 1
            if self.dragon.fireTime%70 == 0:
                self.dragon.breathingFire = False
                self.dragon.fire.resetCoords()
    def redrawAll(self, canvas):
        self.dragon.drawDragon(canvas)

    


class DragonBlockGame(ModalApp):
    #create modes...
    def appStarted(self):
        #self.addMode(StartMode(name="start"))
        self.addMode(PlayMode(name="play"))
        #prolly add some more modes
        #set active mode to start
        #self.setActiveMode("start")
        self.setActiveMode("play")

DragonBlockGame()

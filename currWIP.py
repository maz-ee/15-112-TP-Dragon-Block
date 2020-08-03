from cmu_112_graphics import *
import random

###################################################
#Dragon
###################################################
class Block():
    #NORMAL blocks are generated right under head block...
    def __init__(self, app, x, y):
        self.app = app
        self.width = 20
        self.height = 20
        self.x = x
        #30 is ground height
        self.y = y-self.width/2-self.app.ground.height
        self.hasBeenHit = False
        self.onObstacle = False
    def slide(self):
        self.x += 3
    def isOnObstacle(self, obstacle):
        if self.x+self.width/2>=obstacle.x-obstacle.width/2 and self.x-self.width/2<=obstacle.x+obstacle.width/2 and (self.y+self.height/2)-(obstacle.y-obstacle.height/2)<=2:
            self.onObstacle = True
        else:
            self.onObstacle = False
    def draw(self, canvas):
        cx = self.x-self.app.scrollX
        cy = self.y-self.app.scrollY
        canvas.create_rectangle(cx-self.width/2, cy-self.height/2, cx+self.width/2, cy+self.width/2, fill = "red")
class Head(Block):
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
        # self.x = x
        # self.y = y
        self.blocks = [Head(self.app, self.app.width/2, self.app.height)]
        #print(self.blocks[0].x, self.blocks[0].y)
    def spawnBlock(self):
        if len(self.blocks)>=1:
            x = self.blocks[-1].x
            y = self.blocks[-1].y
            for block in self.blocks:
                block.y -= 20
            #add 40 to offset from ground...
            self.blocks.append(Block(self.app, x, y+10+self.app.ground.height))
            #print(self.blocks[1].x, self.blocks[1].y)
    def slide(self):
        self.app.scrollX+=3
        for block in self.blocks:
            block.slide()
        #print("is moving!")
    def checkGameOver(self):
        if len(self.blocks)==0:
            self.app.setActiveMode("gameOver")
    def checkCollisions(self):
        currObstacle = None
        somethingWasHit = False
        for obstacle in self.app.ground.obstacles:
            if isinstance(obstacle, BlockObstacle):
                for block in self.blocks:
                    if block.x+block.width/2>obstacle.x-obstacle.width/2 and block.y+block.height/2>obstacle.y-obstacle.height/2:
                        print("HIT")
                        somethingWasHit = True
                        block.hasBeenHit = True
                    block.isOnObstacle(obstacle)
                    if block.onObstacle:
                        currObstacle = obstacle
            if isinstance(obstacle, SpikeObstacle):
                for spike in obstacle.spikes:
                    for block in self.blocks:
                        if block.x+block.width/2>=spike.x and block.y+block.height/2==spike.x:
                            print("The first case")
                            somethingWasHit = True
                            block.hasBeenHit = True 
                        elif block.x+block.width/2>=spike.center and block.y-block.height/2>=spike.y-spike.height-5:
                            print("impaled")
                            somethingWasHit = True
                            block.hasBeenHit = True 
        self.checkGameOver()
        if somethingWasHit:
            self.shrink()
    def shrink(self):
        keeperBlocks = []
        numBlocksHit = 0
        for block in self.blocks:
            if not block.hasBeenHit:
                keeperBlocks.append(block)
            else:
                numBlocksHit += 1
        print(numBlocksHit)
        print(keeperBlocks)
        for i in range(len(keeperBlocks)-1, -1, -1):
            block = keeperBlocks[i]
            if len(keeperBlocks)==1:
                if block.y!=self.app.height-self.app.ground.height-10:
                    #for block obstacle
                    if block.onObstacle == False:
                        block.y+= block.height*numBlocksHit
                    #break
            elif i > 0:
                nxtBlock = keeperBlocks[i-1]
                if abs(block.y-nxtBlock.y)>20 or (i==len(keeperBlocks)-1 and block.y!=self.app.height-self.app.ground.height-10):
                    if block.onObstacle == False:
                        for j in range(i, 0, -1):
                            keeperBlocks[j].y += keeperBlocks[j].height*numBlocksHit
        self.blocks = keeperBlocks
    def draw(self, canvas):
        for block in self.blocks:
            block.draw(canvas)


#############################################
#Obstacles
#############################################

class Obstacle():
    def __init__(self, app, x, y):
        self.app = app
        self.x = x
        self.y = y-self.app.ground.height
        
class BlockObstacle(Obstacle):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.width = random.choice([40, 60, 80, 100])
        self.height = random.choice([20, 40, 60, 80, 100])
        self.y -= self.height/2
    def draw(self, canvas):
        cx = self.x-self.app.scrollX
        cy = self.y-self.app.scrollY
        canvas.create_rectangle(cx-self.width/2, cy-self.height/2, cx+self.width/2, cy+self.height/2, fill = "brown")
class Spike(Obstacle):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.width = 20
        self.height = 20
        self.center = self.x+self.width/2
        print(self.center)
    def draw(self, canvas):
        #print("draw spike")
        x = self.x-self.app.scrollX
        y = self.y-self.app.scrollY
        c = self.center-self.app.scrollX
        canvas.create_polygon(x, y, c, y-self.height, x+self.width, y, fill = "AntiqueWhite3")

class SpikeObstacle(Obstacle):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.numSpikes = random.choice([2, 4, 6])
        self.spikes = []
        self.spikeWidth = 20
        self.createSpikes()
    def createSpikes(self):
        for i in range(self.numSpikes):
            self.spikes.append(Spike(self.app, self.x+self.spikeWidth*i, self.y+30))
    def draw(self, canvas):
        for spike in self.spikes:
            spike.draw(canvas)

#############################################
#Knights/enemy stuff
#############################################

class Weapon():
    def __init__(self, app, x, y):
        self.app = app
        self.x = x
        self.y = y
        self.hasHitDragon = False

class Sword(Weapon):
    def __init__(self, app, x, y, length=0):
        super().__init__(app, x, y)
        self.length = -1
        if length != 0:
            self.length = length
        else:
            self.length = random.choice(10, 20, 30, 40)
        self.width = 6
    def move(self):
        self.x-=8
    def touchedDragon(self):
        print("here")
        for block in self.app.dragon.blocks:
            if self.x<=block.x+block.width/2 and block.y+block.height/2>self.y>block.y-block.height/2:
                #issue, blocks are falling down/updating as they move, so multiple are taken out
                #if one has been hit, set rest to false, or break...?
                print("a block was hit")
                print(self.y)
                print(block.y)
                block.hasBeenHit = True
                
                
                
        self.app.dragon.shrink()
    def draw(self, canvas):
        canvas.create_polygon(self.x, self.y-self.width/2, self.x, self.y+self.width/2, self.x-self.length, self.y, fill = "black")
        
        
          
class Knight():
    def __init__(self, app, x, y, weapon):
        self.app = app
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.dead = False
        self.weapon = None
        self.hasHitDragon = False
        if weapon == "sword":
            self.weapon = Sword(self.app, self.x-self.width/2, self.y, 10)

class FlyingKnight(Knight):
    def __init__(self, app, x, y, weapon="sword"):
        super().__init__(app, x, y, weapon)
        #the y is always the same y as dragon head y
    def move(self):
        self.weapon.move()
        self.x-=8
    def hitDragon(self):
        self.weapon.touchedDragon()
        # if self.weapon.hasHitDragon:
        #     self.hasHitDragon = True
        #     self.app.dragon.shrink()
    def draw(self, canvas):
        self.weapon.draw(canvas)
        canvas.create_rectangle(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2, fill = "purple")



#############################################
#Course
#############################################

class Ground():
    def __init__(self, app):
        self.app = app
        self.height = 30
        self.obstacles = []
    def spawnObstacles(self):
        #self.obstacles.append(BlockObstacle(self.app, 270, self.app.height))
        self.obstacles.append(SpikeObstacle(self.app, 270, self.app.height))

    def draw(self, canvas):
        for obstacle in self.obstacles:
            obstacle.draw(canvas)
        canvas.create_rectangle(0, self.app.height-20, self.app.width, self.app.height, fill = "brown")
        canvas.create_rectangle(0, self.app.height-self.height, self.app.width, self.app.height-20, fill = "green")

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
        self.timerCalls = 0
        self.ground = Ground(self)
        self.dragon = Dragon(self)
        self.knights = []
        self.knights.append(FlyingKnight(self, self.width, self.dragon.blocks[0].y))
    def modeActivated(self):
        """
        populate game...
        """
        self.appStarted()
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
            self.dragon.spawnBlock()
        if event.key == "s":
            self.ground.spawnObstacles()
        # if event.key == "f":
        #     self.dragon.breatheFire()
    def mousePressed(self, event):
        """
        click anywhere on screen to generate blocks
        maybe click and drag to angle fire at knights?
        """
        #if not self.dragon.fire.isSelected:
        self.dragon.spawnBlock()
            
    # def mouseDragged(self, event):
    #     if self.dragon.fire.isSelected:
    #         self.dragon.fire.angle(event.x, event.y)
    # def mouseReleased(self, event):
    #     self.dragon.fire.isSelected = False
    def timerFired(self):
        #self.ground.collidesWith()
        #if not self.dragon.hasBeenHit:
        self.dragon.slide()
        self.dragon.checkCollisions()
        for knight in self.knights:
            knight.move()
        for knight in self.knights:
            if not knight.hasHitDragon:
                knight.hitDragon()
        self.dragon.checkGameOver()
        self.timerCalls += 1
        # #fire only lasts for 2.5 seconds
        # if self.dragon.breathingFire:
        #     self.dragon.fireTime += 1
        #     if self.dragon.fireTime%70 == 0:
        #         self.dragon.breathingFire = False
        #         self.dragon.fire.resetCoords()
    def redrawAll(self, canvas):
        self.ground.draw(canvas)
        self.dragon.draw(canvas)
        for knight in self.knights:
            knight.draw(canvas)

class StartMode(Mode):
    def appStarted(self):
        pass
    def keyPressed(self, event):
        if event.key == "Space":
            self.setActiveMode("play")
    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/2, text = "<< Start >>")
        canvas.create_text(self.width/2, self.height*3/4, text = "['Space' to start]")
    

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
        self.addMode(StartMode(name="start"))
        self.addMode(PlayMode(name="play"))
        self.addMode(GameOverMode(name="gameOver"))
        #prolly add some more modes
        #set active mode to start
        self.setActiveMode("start")
        #self.setActiveMode("play")

DragonBlockGame()
# cmu_112_graphics is from diderot -> 15112 class!
# https://www.diderot.one/course/34/chapters/2847/
from cmu_112_graphics import *
import random
import time
###################################################
#Dragon
###################################################
class Block():
    #these make up the dragon
    #NORMAL blocks are generated right under head block...
    def __init__(self, app, x, y):
        self.app = app
        self.width = 20
        self.height = 20
        self.x = x
        # 30 is ground height
        self.y = y-self.height/2-self.app.ground.height
        self.hasBeenHit = False
        self.onObstacle = False
    def slide(self):
        #move block
        self.x += 3
    def isOnObstacle(self, obstacle):
        #supposed to check if a block is on top of a blockObstacle
        # if self.x+self.width/2>=obstacle.x-obstacle.width/2 and self.x-self.width/2<=obstacle.x+obstacle.width/2 and (self.y+self.height/2)-(obstacle.y-obstacle.height/2)<=2:
        #     self.onObstacle = True
        # else:
        #     self.onObstacle = False
        if self.x+self.width>=obstacle.x and \
                self.x+16<=obstacle.x+obstacle.width and \
                self.y+self.height/2>= \
                (self.app.ground.level-obstacle.height+3):
            self.onObstacle = True
        else:
            self.onObstacle = False
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
        # self.x = x
        # self.y = y
        #all of the blocks make up the dragon. head block is the first element
        self.blocks = [Head(self.app, self.app.width/2, self.app.height)]
        #print(self.blocks[0].x, self.blocks[0].y)
    def spawnBlock(self):
        #add blocks to the tail
        if len(self.blocks)>=1:
            #coords of last elem
            x = self.blocks[-1].x
            y = self.blocks[-1].y
            #move all current blocks up by one block
            for block in self.blocks:
                block.y -= block.width
            #add 40 to offset y from ground... 10 for block.width/2 & 30 for ground height -> y + 10 +self.app.ground.height
            self.blocks.append(Block(self.app, x, y+10+self.app.ground.height))
            #print(self.blocks[1].x, self.blocks[1].y)
    def slide(self):
        #dragon moving
        self.app.scrollX+=3
        #move all blocks
        for block in self.blocks:
            block.slide()
        #print("is moving!")
    def fall(self, obstacle_type, idx, doFall):
        """
        Modified physics free fall for better game experience
        """
        if (len(self.blocks)>0):
            if doFall:
                print("obstacle_type: ", obstacle_type)
                if self.lastTime == 0:
                     self.lastTime = time.monotonic()
                     self.dt = 0
                else:
                    self.dt = time.monotonic() - self.lastTime
                if obstacle_type == 1: # Start Fall faster for box obstacle
                    if (self.dt < .5):
                        self.dt = .5
                dt = int(self.dt**2)
                if obstacle_type == 0: # Limit spike obstacle fall speed
                    if dt > .5:
                        dt = .5
                if obstacle_type == 2: # Limit Horizontal Knight fall speed
                    if dt > 2:
                        dt = 2
                # limt fall to stop at ground level
                if self.blocks[-1].y+self.blocks[-1].height/2+dt > self.app.ground.level:
                    dt = self.app.ground.level - (self.blocks[-1].y+self.blocks[-1].height/2)
                for block in reversed(self.blocks[:idx]):
                    block.y += dt
            else:
                self.lastTime = 0
        else:
            self.lastTime = 0

    def checkGameOver(self):
        #if there are no more blocks (all blocks were hit)
        if len(self.blocks)==0:
            self.app.setActiveMode("gameOver")
    def checkCollisions(self):
        currObstacle = None
        somethingWasHit = False
        for obstacle in self.app.ground.obstacles:
            #go through ALL obstacles
            if isinstance(obstacle, BlockObstacle):
                # self.count = self.count + 1
                # print(self.count)                
                pop_idx = None
                for idx, block in enumerate(self.blocks):
                    if block.x+block.width+10>=obstacle.x and \
                                block.x+0<=obstacle.x+obstacle.width and \
                                block.y+block.height/2>= \
                                    (self.app.ground.level-obstacle.height+3):
                        pop_idx = idx
                        break
                if pop_idx is not None:
                    self.blocks = self.blocks[:pop_idx]
                if len(self.blocks)>0:
                    if not (self.blocks[-1].x+self.blocks[-1].width+10>=obstacle.x and \
                                self.blocks[-1].x+0<=obstacle.x+obstacle.width and \
                                self.blocks[-1].y+self.blocks[-1].height/2<= \
                                    (self.app.ground.level-obstacle.height)):
                        self.fall(1, len(self.blocks), True)
            if isinstance(obstacle, SpikeObstacle):
                #case where the obstacle is a SpikeObstacle
                for spike in obstacle.spikes:
                    #self.checkGameOver()
                    # if len(self.blocks)>1:
                    if len(self.blocks)>0:
                        block = self.blocks[-1]
                        if block.x+block.width>=spike.x and \
                                    block.x<=spike.x+spike.width and \
                                    block.y+block.height/2>= \
                                        (self.app.ground.level-self.app.ground.height+12):
                            self.blocks.pop()
                            break
                self.fall(0, len(self.blocks), True)
            #TODO: isinstance(obstacle, TrapObstacle)
            if isinstance(obstacle, TrapObstacle):
                #check bounds
                #self.checkGameOver()
                if len(self.blocks)>0:
                    block = self.blocks[-1]
                    if block.x+block.width/2 >= obstacle.x-obstacle.width/2:
                        #print("hey there")
                        # if obstacle.firstTouch:
                        #     print("hey there")
                        obstacle.slideOver()
                        #obstacle.knight.weapon.touchedDragon() 
                        self.fall(3, len(self.app.dragon.blocks), True)       
        self.checkGameOver()
        if somethingWasHit:
            self.shrink()
    def shrink(self):
        #updates the blocks if blocks have been hit
        keeperBlocks = []
        numBlocksHit = 0
        #tracks the number of blocks hit
        #appends blocks that have not been hit to new lsit
        for block in self.blocks:
            if not block.hasBeenHit:
                keeperBlocks.append(block)
            else:
                numBlocksHit += 1
        print(numBlocksHit)
        print(keeperBlocks)
        #supposed to update position of blocks (everything is supposed to be on the ground, not in the air)
        for i in range(len(keeperBlocks)-1, -1, -1):
            block = keeperBlocks[i]
            #was supposed to take the case where all bottom blocks are hit, and only floating blocks in the air remain
            #but got idx errors on the elif
            #so for some reason, i put this if statement here...
            if len(keeperBlocks)==1:
                if block.y!=self.app.height-self.app.ground.height-10:
                    #for block obstacle
                    if block.onObstacle == False:
                        block.y+= block.height*numBlocksHit
                    #break
            #supposed to take the case where a block surrounded by blocks on the top and bottom is hit, and then the gap between top and bottom has to be closed
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
        #can have these widths/heights
        #increment by 20 since the blocks have width of 20
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
        #x & y are the lower left corner
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
        #contains a list of spike objects
        self.spikes = []
        self.spikeWidth = 20
        self.createSpikes()
    def createSpikes(self):
        for i in range(self.numSpikes):
            self.spikes.append(Spike(self.app, self.x+self.spikeWidth*i, self.y+30))
    def draw(self, canvas):
        for spike in self.spikes:
            spike.draw(canvas)

class TrapObstacle(Obstacle):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.knight = None
        self.touched = False
        self.width = 40
        self.height = 6
        self.firstTouch = True
        print("trapX: ", self.x)
    def slideOver(self):
        if self.firstTouch:
            self.firstTouch = False
            self.knight = TrapKnight(self.app, self.x, self.y)
            self.x += self.width
            self.touched = True
            self.knight.weapon.touchedDragon()
            #self.knight.move()
    def draw(self, canvas):
        x = self.x-self.app.scrollX
        y = self.y-self.app.scrollY
        if self.touched and self.knight != None:
            self.knight.draw(canvas)
        canvas.create_rectangle(x-self.width/2, y-self.height/2, x+self.width/2, y+self.height/2, fill = "burlywood1")

#############################################
#Knights/enemy stuff
#############################################

class Weapon():
    def __init__(self, app, x, y):
        self.app = app
        self.x = x
        self.y = y
        self.hasHitDragon = False

class HorizontalSword(Weapon):
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
        for idx, block in enumerate(reversed(self.app.dragon.blocks)):   
            if block.x+block.width-50>=self.x and \
                        block.x-50<=self.x+self.length and \
                        block.y+block.height/2>= \
                        (self.app.ground.level-self.app.ground.height+20):
                self.app.dragon.blocks.pop()
                break
        #block = self.app.dragon.blocks[-1]
        if len(self.app.dragon.blocks)>0:
            block = self.app.dragon.blocks[-1]
            if not (block.x+block.width-50>=self.x and \
                    block.x-50<=self.x+self.length and \
                    block.y+block.height/2>= \
                    (self.app.ground.level-self.app.ground.height+20)):
                self.app.dragon.fall(2, len(self.app.dragon.blocks), True)

    def draw(self, canvas):
        canvas.create_polygon(self.x, self.y-self.width/2, self.x, self.y+self.width/2, self.x-self.length, self.y, fill = "black")
        
class VerticalSword(Weapon):
    def __init__(self, app, x, y, length=0):
        super().__init__(app, x, y)
        self.length = -1
        if length != 0:
            self.length = length
        else:
            self.length = random.choice([20, 40])
        self.width = 6
    def move(self):
        #self.y -=self.length
        pass
    def touchedDragon(self):
        if self.length == 40:
            for i in range(2):
                if len(self.app.dragon.blocks) > 0:
                    self.app.dragon.blocks.pop()
        if self.length == 20:
            for i in range(1):
                if len(self.app.dragon.blocks) > 0:
                    self.app.dragon.blocks.pop()
        print("Before fall")
        #self.app.dragon.fall(3, len(self.app.dragon.blocks), True)
        
    def draw(self, canvas):
        x = self.x-self.app.scrollX
        y = self.y#-self.app.scrollY
        #y = 275
        # print("swordy: ", y)
        # print("swordx: ", x)
        #canvas.create_polygon(x-self.width/2, y, x+self.width/2, y, x, y-self.length)
        canvas.create_polygon(x-self.width/2, y, x+self.width/2, y, x, y-self.length)
         
class Knight():
    def __init__(self, app, x, y, weapon):
        self.app = app
        self.x = x
        print("KnightX: ", self.x)
        self.y = y
        self.width = 15
        self.height = 15
        self.dead = False
        self.weapon = None
        self.hasHitDragon = False
        if weapon == "horizontal sword":
            self.weapon = HorizontalSword(self.app, self.x-self.width/2, self.y, 10)
        if weapon == "vertical sword":
            self.weapon = VerticalSword(self.app, self.x, self.y)
            print("init y: ", y)

class FlyingKnight(Knight):
    def __init__(self, app, x, y, weapon="horizontal sword"):
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
        # print("yyyyy: ", self.y)
        #canvas.create_rectangle(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2, fill = "purple")
        canvas.create_rectangle(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2, fill = "purple")

class TrapKnight(Knight):
    def __init__(self, app, x, y, weapon="vertical sword"):
        super().__init__(app, x, y, weapon)
        # print("created")
        # print("TrapKnightX: ", self.x)
        #y passed in is canvas height - groundhieght - half of trap height
        #knight width is 10
        #sword "base" has to be lined up with ground after moving up
        #self.y = self.app.height-self.weapon.length#-self.height/2
        #print("self.app.height = ", self.app.height)
        #print(self.y)
        self.weapon.y = self.y
        #^^leaves 
    def move(self):
        self.weapon.move()
        self.y -= self.weapon.length
    def draw(self, canvas):
        self.weapon.draw(canvas)
        # print("knight is drawn plzzzz")
        # print("wdt: ", self.width)
        # print("ht: ", self.height)
        # print("yyyyy: ", self.y)
        # print("self.y-self.height/2: ", self.y-self.height/2)
        x = self.x-self.app.scrollX
        y = self.y-self.app.scrollY
        # canvas.create_rectangle(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2, fill = "purple")
        canvas.create_rectangle(x-self.width/2, y-self.height/2, x+self.width/2, y+self.height/2, fill = "purple")
        #canvas.create_rectangle(x-self.width/2, 275, x+self.width/2, 290, fill = "purple")
        

#############################################
#Course
#############################################

class Ground():
    def __init__(self, app):
        self.app = app
        self.height = 30
        self.level = 300 - self.height # 270
        #obstacles are populated on the ground
        self.obstacles = []
    def spawnObstacles(self):
        newObstacle = random.choice([BlockObstacle(self.app, self.app.dragon.blocks[0].x+70, self.app.height),
                                SpikeObstacle(self.app, self.app.dragon.blocks[0].x+50, self.app.height),
                                TrapObstacle(self.app, self.app.dragon.blocks[0].x+40, self.app.height)])
        self.obstacles.append(newObstacle)
        # self.obstacles.append(BlockObstacle(self.app, 270, self.app.height))
        # self.obstacles.append(SpikeObstacle(self.app, self.level-self.app.scrollX, self.app.height))
        # self.obstacles.append(TrapObstacle(self.app, 270, self.app.height))

    def draw(self, canvas):
        # for obstacle in self.obstacles:
        #     obstacle.draw(canvas)
        canvas.create_rectangle(0, self.app.height-20, self.app.width, self.app.height, fill = "brown")
        canvas.create_rectangle(0, self.app.height-self.height, self.app.width, self.app.height-20, fill = "green")
        for obstacle in self.obstacles:
            obstacle.draw(canvas)

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
        #self.knights.append(FlyingKnight(self, self.width, self.dragon.blocks[0].y))
        self.knights.append(FlyingKnight(self, self.width, 180))
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
        # self.dragon.fall()
        for knight in self.knights:
            knight.move()
        # for knight in self.knights:
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
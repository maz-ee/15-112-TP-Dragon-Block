from cmu_112_graphics import *
import random

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
    def checkCollisions(self):
        currObstacle = None
        somethingWasHit = False
        for obstacle in self.app.ground.obstacles:
            for block in self.blocks:
                if block.x+block.width/2>obstacle.x-obstacle.width/2 and block.y+block.height/2>obstacle.y-obstacle.height/2:
                    print("HIT")
                    somethingWasHit = True
                    block.hasBeenHit = True
                # if block.x-block.width/2>=obstacle.x-obstacle.width/2 and block.x+block.width/2<=obstacle.x+obstacle.width/2 and block.y+block.height/2==obstacle.y-obstacle.height/2:
                #     block.onObstacle = True
                # if block.onObstacle and block.x-block.width/2>obstacle.x+obstacle.width/2:
                #     block.onObstacle = False
                block.isOnObstacle(obstacle)
                if block.onObstacle:
                    currObstacle = obstacle


        if somethingWasHit:
            self.shrink(currObstacle)
    def shrink(self, obstacle):
        keeperBlocks = []
        numBlocksHit = 0
        for block in self.blocks:
            print("first loop")
            if not block.hasBeenHit:
                keeperBlocks.append(block)
            else:
                numBlocksHit += 1
        print(numBlocksHit)
        print(keeperBlocks)
        # for i in range(len(keeperBlocks)-1):
        #     block = keeperBlocks[i]
        #     nxtBlock = keeperBlocks[i+1]
        #     if block.y-nxtBlock.y > 20:
        #         for j in range(i+1):
        #             keeperBlocks[j].y += keeperBlocks[j].height*numBlocksHit
        for i in range(len(keeperBlocks)-1, -1, -1):
            print("hereeeee")
            block = keeperBlocks[i]
            if len(keeperBlocks)==1:
                print("only head")
                if block.y!=self.app.height-self.app.ground.height-10:
                    print("special case")
                    if block.onObstacle == False:
                        print("bad bad bad")
                        block.y+= block.height*numBlocksHit
                    #break
            elif i > 0:
                nxtBlock = keeperBlocks[i-1]
                if abs(block.y-nxtBlock.y)>20 or (i==len(keeperBlocks)-1 and block.y!=self.app.height-self.app.ground.height-10):
                    print("passed conditionsl")
                    if block.onObstacle == False:
                        for j in range(i, 0, -1):
                            keeperBlocks[j].y += keeperBlocks[j].height*numBlocksHit
        print("dissapear")
        self.blocks = keeperBlocks
    def draw(self, canvas):
        for block in self.blocks:
            block.draw(canvas)


#############################################
#Obstacles
#############################################

class Obstacle():
    def __init__(self, app, x, y):
        print("called")
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



#############################################
#Course
#############################################

class Ground():
    def __init__(self, app):
        self.app = app
        self.height = 30
        self.obstacles = []
        #self.obstacles.append(BlockObstacle(self.app, 270, self.app.height))
    def spawnObstacles(self):
        self.obstacles.append(BlockObstacle(self.app, 270, self.app.height))
    # def collidesWith(self):
    #     for obstacle in self.obstacles:
    #         if obstacle.x-obstacle.width/2 < self.app.dragon.x+self.app.dragon.width/2 and obstacle.y-obstacle.height/2 < self.app.dragon.y+self.app.dragon.height/2:
    #             self.app.dragon.hasBeenHit = True
    #         for block in self.app.dragon.Tail.blocks:
    #             if obstacle.x-obstacle.width/2 < block.x+block.width/2 and obstacle.y-obstacle.height/2 < block.y+block.width/2:
    #                 block.hasBeenHit = True
    #         self.app.dragon.Tail.shorten()

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
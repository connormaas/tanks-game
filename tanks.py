##############################################################
#############               TANKS!               #############
##############################################################
# Name: Connor Maas
##############################################################

import math, random
import pyautogui
from graphics import *

##############################################################
# 1.) APP STARTED + APP STARTED HELPERS
##############################################################

# Stores all starting values, calls starting function
def appStarted(app, highScore=None):
  # GENERAL
  app.tankWidth = 80
  app.tankHeight = 50
  app.margin = 10
  app.topMargin = 50
  app.randInt= 0
  app.moveDelay = 0
  app.timerDelay =  2
  app.flickerHelper = 0 
  app.barrierBounce = 10
  app.tankScale = 1/3.2

  # TANK INFO
  cx = app.margin + app.tankWidth
  cy = app.topMargin + app.tankHeight
  cxN = app.width - app.margin - app.tankWidth
  cyN = app.height - app.margin - app.tankHeight
  cxA = -100
  cyA = -100
  app.gunLength = app.width/50
  app.spriteCounter = [0,0,0]
  app.nextMoveStatus = [None, False, False]
  app.ogPoints = [None,[0,0],[0,0]]
  app.centerHelpers = [None,[False, False],[False, False]]
  app.findingPath = [None, False, False]
  app.noTurn = [False, False, False]
  app.intersectionNow = [False, False, False]
  app.move= [False, False, False]
  # 0-N, 1-E, 2-S, 3-W, 4-NE, 5-SE, 6-SW, 7-NW
  app.tankDirections = [[False]*8,[False]*8, [False]*8]
  app.tankCenters = ([[app.width/2-200,app.height/2],
                      [app.width/2+200,app.height/2],
                      [app.width/2+200,app.height/1.5]])
  userTankEdges = ([app.tankCenters[0][0], 
                      app.tankCenters[0][1]-app.tankHeight/2, 
                      app.tankCenters[0][0]+app.tankWidth/2, 
                      app.tankCenters[0][1]-app.tankHeight/2,
                      app.tankCenters[0][0]+app.tankWidth/2, 
                      app.tankCenters[0][1]+app.tankHeight/2,
                      app.tankCenters[0][0]-app.tankWidth/2, 
                      app.tankCenters[0][1]+app.tankHeight/2])
  
  normalTankEdges = ([app.tankCenters[1][0], app.tankCenters[1][1], 
                    app.tankCenters[1][0], app.tankCenters[1][1],
                    app.tankCenters[1][0], app.tankCenters[1][1],
                    app.tankCenters[1][0], app.tankCenters[1][1]])

  attackTankEdges = ([-100,-100,-100,-100,-100,-100,-100,-100])
  app.tankEdges = [userTankEdges,normalTankEdges,attackTankEdges]
  app.armDirection = 0
  app.directionDegree = [0,0,0]

  # LEVEL INFO
  app.tanksRemaining = 3
  app.neededTanksKilled = 3
  app.bulletSpeed = 7
  app.level = 1
  app.enemyTankSpeed = 2.5
  app.highScore = highScore
  app.score = 0
  
  # EXPLOSION INFO
  app.correctorNumber = 0
  app.explosionSpriteCounter = 0
  app.explosionInfo = [[False, -100,-100],[False, -100,-100],[False, -100,-100]]
  app.explosionDelay = 0

  # BULLET INFO
  app.bulletSlopes = [0, 0, 0]
  app.bulletBounces = [0, 0, 0]
  app.shoot = [False,False,False]
  rB = 4
  cxB, cyB = -5, -5
  cxB1, cyB1 = 0,0
  rBN = 4
  cxBN, cyBN = -5, -5
  cxB1N, cyB1N = 0,0
  rBA = 4
  cxBA, cyBA = cxA, cyA
  cxB1A, cyB1A = 0,0
  app.bulletInfo = ([[cxB,cyB,rB,cxB1,cyB1],[cxBN,cyBN,rBN,cxB1N,cyB1N], 
  [cxBA,cyBA,rBA,cxB1A,cyB1A]])
  app.shootNow = [False, False, False]
  app.originalBulletPoints = [[cx,cy],[cxN, cyN],[cxA, cyA]]

  # BARRIER INFO
  app.maxBarrierSize = app.width//9
  app.barrierCords = ([[app.margin, app.topMargin+app.height//8],
                      [app.width-app.margin-(app.width//9), 
                      app.height-app.margin-app.height//4]])
  app.barrierSizes = ([[app.width//9,app.width//20], 
                        [app.width//9,app.width//20]])

  # BOOLS
  app.instructionScreen = False
  app.attackTankTime = False
  app.nextLevelScreen = False
  app.titleScreen = True
  app.paused = True
  app.showHighScore = False
  app.flicker = False
  app.gameOver = True

  # IMAGES
  # from https://craftpix.net/product/2d-top-down-tank-game-assets/
  app.storeUserTankIm = ([["images/track_1_a.png","images/track_1_b.png"],["images/hull_02.png"],
                        ["images/gun_01.png"]])
  app.userTankIm = ([["images/track_1_a.png","images/track_1_b.png"],["images/hull_02.png"],
                        ["images/gun_01.png"]])
  

  app.storeNormalTankIm = ([["images/track_1_a.png","images/track_1_b.png"],["images/hull_06.png"],
                          ["images/gun_03.png"]])
  app.normalTankIm = ([["images/track_1_a.png","images/track_1_b.png"],["images/hull_06.png"],
                        ["images/gun_03.png"]])

  app.storeAttackTankIm = ([["images/track_3_A.png","images/track_3_B.png"],["images/hull_03.png"],
                          ["images/gun_05_b.png"]])
  app.attackTankIm = ([["images/track_1_a.png","images/track_1_b.png"],["images/hull_03.png"],
                        ["images/gun_05_b.png"]])
  app.explosionIm = ["images/explosion_c.png","images/explosion_d.png","images/explosion_e.png"]

  # from https://stock.adobe.com/search?k=wood+plank+background+cartoon
  app.barrierIm = ["images/barrier.png"]*6

  # SETUP 
  getBarrierData(app)
  tankOrientation(app, app.directionDegree[0], app.userTankIm, "user")
  armOrientation(app, app.armDirection, 0, app.userTankIm, "user")
  trackOrientation(app, app.directionDegree[0], app.userTankIm, "user")
 
  tankOrientation(app, app.directionDegree[1], app.normalTankIm, "normal")
  armOrientation(app, app.armDirection, 0, app.normalTankIm, "normal")
  trackOrientation(app, app.directionDegree[1], app.normalTankIm, "normal")

  tankOrientation(app, app.directionDegree[2], app.attackTankIm, "attack")
  armOrientation(app, app.armDirection, 0, app.attackTankIm, "attack")
  trackOrientation(app, app.directionDegree[2], app.attackTankIm, "attack")

  loadEffect(app, app.explosionIm)
  loadEffect(app, app.barrierIm)
  scaleCropBarrier(app)

# Gets the data for the barriers
def getBarrierData(app):
  app.barrierCords = ([[app.margin, app.topMargin+app.height//8],
                      [app.width-app.margin-(app.width//9), 
                      app.height-app.margin-app.height//4]])
  app.barrierSizes = ([[app.width//9,app.width//20], [app.width//9,
                      app.width//20]])
  for i in range(4):
    legalBarrierDistance = app.width - ((app.width//9+app.margin)*2)
    distribX1 = (app.width//9+app.margin) + i*((legalBarrierDistance//4))
    distribX2 = (((app.width//9+app.margin) + i*((legalBarrierDistance//4)))+
                  (legalBarrierDistance//4))
    
    randomCordinateX = (random.randint(distribX1, distribX1+app.tankWidth//2))   
    randomCordinateY= (random.randint(app.topMargin+app.barrierCords[0][1], 
              app.height-app.margin-app.maxBarrierSize-app.barrierCords[0][1]))
    randomSizeX = random.randint(app.maxBarrierSize//2, app.maxBarrierSize)
    randomSizeY = random.randint(app.maxBarrierSize//2, app.maxBarrierSize)

    app.barrierCords += [[randomCordinateX, randomCordinateY]]
    app.barrierSizes += [[randomSizeX, randomSizeY]]

##############################################################
# 2.) IMAGES AND GRAPHICS
##############################################################
# scales the image to a certain size
def scaleImage(app, image, scale, antialias=False):
  # antialiasing is higher-quality but slower
  resample = Image.ANTIALIAS if antialias else Image.NEAREST
  return image.resize((round(image.width*scale), round(image.height*scale)), 
                      resample=resample)

# Scale and crop the barrier image to match barrier size and location
def scaleCropBarrier(app):
  for i in range(len(app.barrierIm)):  
    x, y = (0, 0)
    x1, y1 = app.barrierSizes[i][0],app.barrierSizes[i][1]
    app.barrierIm[i] = app.barrierIm[i].crop((x, y, x1, y1))

# load an effect 
def loadEffect(app, images):  
  for i in range(len(images)):
    if not str(images[i]).startswith("<"):
      url = app.loadImage(images[i])
    else:
      url = images[i]
    images[i] = url

# changes the direction of the arm
def armOrientation(app, degree, oldDegree, images, tank):
  url = processImData(app, images, 2, 0, tank)
  url = url.rotate(degree)
  updateOrientation(app, url, 2, 0, tank)

# changes the direction of the tracks of the tank
def trackOrientation(app, degree, images, tank):
  for i in range(len(images[0])):
    url = processImData(app, images, 0, i, tank)
    url = url.rotate(degree, expand=True)
    updateOrientation(app, url, 0, i, tank)
  app.spriteCounter[0] = 0

# changes the direction of the base of the tank
def tankOrientation(app, degree, images, tank):
  if not str(images[1][0]).startswith("<"):
    url = app.loadImage(images[1][0])
    url = scaleImage(app, url, app.tankScale)
  else:
    url = (images[1][0])
  url = url.rotate(degree)
  updateOrientation(app, url, 1, 0, tank)

# reloads image because images are destroyed if rotated too often
def processImData(app, images, i, x, tank):
  if tank == "user":
    images[i][x] = app.storeUserTankIm[i][x]
  elif tank == "normal":
    images[i][x] = app.storeNormalTankIm[i][x]
  elif tank == "attack":
    images[i][x] = app.storeAttackTankIm[i][x]
  url = app.loadImage(images[i][x])
  url = scaleImage(app, url, app.tankScale)
  return url

# updates the orientation of every tank
def updateOrientation(app, url, i, x, tank):  
  if tank == "user":
    app.userTankIm[i][x] = url
  elif tank == "normal":
    app.normalTankIm[i][x] = url
  elif tank == "attack":
    app.attackTankIm[i][x] = url

##############################################################
# 3.) BUILT IN + HELPERS
##############################################################
# when mouse is pressed
def mousePressed(app, event):
  if app.shootNow[0] == False: 
    # facilitate enemy tank dodge
    app.randInt = random.randint(1,2)

    # for bullet
    app.shootNow[0] = True
    app.shoot[0] = True
    app.originalBulletPoints[0][0] = app.tankCenters[0][0]
    app.originalBulletPoints[0][1] = app.tankCenters[0][1]
    app.bulletInfo[0][0], app.bulletInfo[0][1] = (app.tankCenters[0][0],
                                                  app.tankCenters[0][1])
    x, y = findDistantPoint(app, app.tankCenters[0][0], app.tankCenters[0][1], 
                              event.x, event.y, "user")
    app.bulletInfo[0][3], app.bulletInfo[0][4] = x, y

# when a key is pressed
def keyPressed(app, event):
  if (event.key == "p"):
    # advance to next level
    if app.nextLevelScreen:
      cx = app.margin + app.tankWidth
      cy = app.height/2
      cxN, cyN = app.width - app.margin -app.tankWidth, app.height/2
      app.titleScreen = False
      app.paused = False
      app.move[1] = True
      # put attack tank into play
      if app.attackTankTime:
        cxA = app.width-app.margin-app.tankWidth
        cyA = app.height /4
        app.tankCenters = [[cx,cy],[cxN,cyN],[cxA,cyA]]
        app.move[2] = True
      else:
        app.tankCenters = [[cx,cy],[cxN,cyN],[-100,-100]]
      app.nextLevelScreen = False
    # pauses game
    elif not app.titleScreen and not app.nextLevelScreen:
      app.paused = not app.paused 
  # high scores
  elif (event.key == "h") and app.titleScreen or app.showHighScore:
    app.showHighScore = not app.showHighScore
  # instructions
  elif (event.key == "i") and app.titleScreen or app.instructionScreen:
    app.instructionScreen = not app.instructionScreen
  # begins game from title screen
  elif (event.key == "1"):
    if (not app.showHighScore and app.gameOver and app.titleScreen and not 
      app.instructionScreen):
      app.nextLevelScreen = True
      cx, cy = app.margin + app.tankWidth, app.height/2
      cxN, cyN = app.width - app.margin -app.tankWidth, app.height/2
      app.tankCenters = [[cx,cy],[cxN,cyN],[-100,-100]]
      app.titleScreen = False
      app.gameOver = False
      app.flicker = False
      app.move[1] = True
      app.move[2] = False
  # exits game
  if (event.key == "l"):
    if app.highScore == None:
      app.highScore= app.score
    else:
      if app.score > app.highScore:
        appStarted(app, app.score)
      else:
        appStarted(app, app.highScore)
 
  # moves tank
  if event.key in "wdxaeczq" and not app.paused and not app.titleScreen:
    app.move[0]= True
    if app.noTurn[0]:
      if (event.key == "w") and (app.directionDegree[0] == 0 or 
        app.directionDegree[0] == 180):
        app.tankDirections[0][0]= True
        app.tankDirections[0][1] = False
        app.tankDirections[0][2] = False
        app.tankDirections[0][3] = False
        app.tankDirections[0][4] = False
        app.tankDirections[0][5] = False
        app.tankDirections[0][6] = False
        app.tankDirections[0][7] = False
        selection = 0
      elif ((event.key == 'x') and (app.directionDegree[0] == 0 
        or app.directionDegree[0] == 180)):
        app.tankDirections[0][2] = True
        app.tankDirections[0][0] = False
        app.tankDirections[0][1] = False
        app.tankDirections[0][3] = False
        app.tankDirections[0][4] = False
        app.tankDirections[0][5] = False
        app.tankDirections[0][6] = False
        app.tankDirections[0][7] = False
        selection = 180
      elif ((event.key == 'd') and (app.directionDegree[0] == 90 or 
        app.directionDegree[0] == 270)):
        app.tankDirections[0][1] = True
        app.tankDirections[0][0] = False
        app.tankDirections[0][2] = False
        app.tankDirections[0][3] = False
        app.tankDirections[0][4] = False
        app.tankDirections[0][5] = False
        app.tankDirections[0][6] = False
        app.tankDirections[0][7] = False
        selection = 270
      elif ((event.key == 'a') and (app.directionDegree[0] == 90 or 
        app.directionDegree[0] == 270)):
        app.tankDirections[0][3] = True
        app.tankDirections[0][0] = False
        app.tankDirections[0][1] = False
        app.tankDirections[0][2] = False
        app.tankDirections[0][4] = False
        app.tankDirections[0][5] = False
        app.tankDirections[0][6] = False
        app.tankDirections[0][7] = False
        selection = 90
      else:
        selection = app.directionDegree[0]
    else:
      if (event.key == "w"):
          app.tankDirections[0][0] = True
          app.tankDirections[0][1] = False
          app.tankDirections[0][2] = False
          app.tankDirections[0][3] = False
          app.tankDirections[0][4] = False
          app.tankDirections[0][5] = False
          app.tankDirections[0][6] = False
          app.tankDirections[0][7] = False
          selection = 0
      elif (event.key == 'x'):
          app.tankDirections[0][2] = True
          app.tankDirections[0][0] = False
          app.tankDirections[0][1] = False
          app.tankDirections[0][3] = False
          app.tankDirections[0][4] = False
          app.tankDirections[0][5] = False
          app.tankDirections[0][6] = False
          app.tankDirections[0][7] = False
          selection = 180
      elif (event.key == 'd'):
          app.tankDirections[0][1] = True
          app.tankDirections[0][0] = False
          app.tankDirections[0][2] = False
          app.tankDirections[0][3] = False
          app.tankDirections[0][4] = False
          app.tankDirections[0][5] = False
          app.tankDirections[0][6] = False
          app.tankDirections[0][7] = False
          selection = 270
      elif (event.key == 'a'):
          app.tankDirections[0][3] = True
          app.tankDirections[0][0] = False
          app.tankDirections[0][1] = False
          app.tankDirections[0][2] = False
          app.tankDirections[0][4] = False
          app.tankDirections[0][5] = False
          app.tankDirections[0][6] = False
          app.tankDirections[0][7] = False
          selection = 90
      elif (event.key == 'e'):
        app.tankDirections[0][4] = True
        app.tankDirections[0][0] = False
        app.tankDirections[0][1] = False
        app.tankDirections[0][2] = False
        app.tankDirections[0][3] = False
        app.tankDirections[0][5] = False
        app.tankDirections[0][6] = False
        app.tankDirections[0][7] = False
        selection = 315
      elif (event.key == 'z'):
        app.tankDirections[0][6] = True
        app.tankDirections[0][0] = False
        app.tankDirections[0][1] = False
        app.tankDirections[0][2] = False
        app.tankDirections[0][3] = False
        app.tankDirections[0][4] = False
        app.tankDirections[0][5] = False
        app.tankDirections[0][7] = False
        selection = 135
      elif (event.key == 'c'):
        app.tankDirections[0][5] = True
        app.tankDirections[0][0] = False
        app.tankDirections[0][1] = False
        app.tankDirections[0][2] = False
        app.tankDirections[0][3] = False
        app.tankDirections[0][4] = False
        app.tankDirections[0][6] = False
        app.tankDirections[0][7] = False
        selection = 225
      elif (event.key == 'q'):
        app.tankDirections[0][7] = True
        app.tankDirections[0][0] = False
        app.tankDirections[0][1] = False
        app.tankDirections[0][2] = False
        app.tankDirections[0][3] = False
        app.tankDirections[0][4] = False
        app.tankDirections[0][5] = False
        app.tankDirections[0][6] = False
        selection = 45
    trackOrientation(app, selection, app.userTankIm, "user")
    rotation = selection - app.directionDegree[0]
    if 270 > abs(rotation) > 90:
      rotation = rotation-180
    app.directionDegree[0] = selection
    tankOrientation(app, rotation, app.userTankIm, "user")
  # stops tank
  elif (event.key == 's'):
    app.move[0] = False
    app.tankDirections[0][0] = False
    app.tankDirections[0][1] = False
    app.tankDirections[0][2] = False
    app.tankDirections[0][3] = False
    app.tankDirections[0][4] = False
    app.tankDirections[0][5] = False
    app.tankDirections[0][6] = app.tankDirections[0][7] = False

# simulates "key pressed" for the AI tank
def rotateNonUserTankHelper(app, tank):
    if tank == "normal":
      index = 1
      images = app.normalTankIm
    elif tank == "attack":
      index = 2
      images = app.attackTankIm
    if app.tankDirections[index][0]:
      selection = 0
    elif app.tankDirections[index][1]:
      selection = 270
    elif app.tankDirections[index][2]:
      selection = 180
    elif app.tankDirections[index][3]:
      selection = 90
    elif app.tankDirections[index][4]:
      selection = 315
    elif app.tankDirections[index][5]:
      selection = 225
    elif app.tankDirections[index][6]:
      selection = 135
    elif app.tankDirections[index][7]:
      selection = 45
    else: 
      selection = app.directionDegree[index]
    trackOrientation(app, selection, images, tank)
    # allows tank to go backwards
    rotation = selection - app.directionDegree[index]
    if 270 > abs(rotation) > 90:
      rotation = rotation-180
    app.directionDegree[index] = selection
    tankOrientation(app, rotation, images, tank)

# timer fired
def timerFired(app): 
  if not app.gameOver and not app.paused:
    app.moveDelay += 1
    app.explosionDelay += 1
    # throttle movement so the animation stays smooth
    if app.moveDelay % 5 == 0: 
      if app.move[0] == True:
          app.spriteCounter[0] = ((1 + app.spriteCounter[0]) 
                                  % len(app.userTankIm[0]))
      if app.move[1] == True:
          app.spriteCounter[1] = ((1 + app.spriteCounter[1]) 
                                  % len(app.normalTankIm[0]))
      if app.move[2] == True:
          app.spriteCounter[2] = ((1 + app.spriteCounter[2]) 
                                  % len(app.attackTankIm[0]))

    # throttle rotation, which is expensive (the delay isn't noticeable)
    if app.moveDelay % 10 == 0:
      rotateNonUserTankHelper(app, "normal")
      rotateNonUserTankHelper(app, "attack")

    # explosion
    if app.explosionDelay % 5 == 0:
      if (app.explosionInfo[0][0] or app.explosionInfo[1][0] or 
        app.explosionInfo[2][0]):
        if app.explosionInfo[0][0]:
          app.explosionInfo[0][0] = False
        if app.explosionInfo[1][0]:
          app.explosionInfo[1][0] = False
        if app.explosionInfo[2][0]:
          app.explosionInfo[2][0] = False
        app.explosionDelay = 0  
        app.explosionSpriteCounter = ((1 + app.explosionSpriteCounter) 
                                      % len(app.explosionIm))

    # levelCheck
    levelCheck(app)

    # motion of enemy tank
    if app.move[1]:
      if app.findingPath[1]:
        rerouteA(app, "normal")
      else:
        seek(app, "normal")     
    if app.move[2]:
      if app.findingPath[2]:
        rerouteA(app, "attack")
      else:
        seek(app, "attack") 

    # moves tank in specific direction
    doStep(app, "user", 3)
    doStep(app, "normal", 5*app.enemyTankSpeed/8)
    doStep(app, "attack", app.enemyTankSpeed)

    # movement for tank gun
    armMotion(app)
    enemyTankMotion(app, "normal")
    enemyTankMotion(app, "attack")

    # intersections
    checkIntersects(app, app.tankEdges[0], "user")
    checkIntersects(app, app.tankEdges[1], "normal")
    checkIntersects(app, app.tankEdges[2], "attack")
    checkBulletIntersects(app, "user")
    checkBulletIntersects(app, "normal")
    checkBulletIntersects(app, "attack")
    checkAttackTankHitsUser(app)

    # catches edge cases the intersection checks miss
    correctorFunction(app, "user")
    correctorFunction(app, "normal")
    correctorFunction(app, "attack")

    # updates
    tankEdges(app, "user")
    tankEdges(app, "normal")
    tankEdges(app, "attack")
    updateShootingStatus(app, "user")
    updateShootingStatus(app, "normal")
    updateShootingStatus(app, "attack")
  
  else:
    if app.gameOver:
      app.flickerHelper += 1
      if (app.flickerHelper % 55 == 0 or app.flickerHelper % 57 == 0 or 
        app.flickerHelper % 59 == 0):
        app.flicker = False
      else:
        app.flicker = True

##############################################################
# 4.) ACTIONS
##############################################################
# Updates the position of the bullet (called when app.shoot[i] is true)
def bulletMotion(app, bulletType):
  if bulletType == "user":
    index = 0
    newDistance = 10
  else:
    index = 1
    newDistance = app.bulletSpeed
  distance = math.sqrt(((app.bulletInfo[index][3]-app.bulletInfo[index][0])**2)
                    +((app.bulletInfo[index][4]-app.bulletInfo[index][1])**2))
  if distance == 0:
    distance = 0.00001
  x = (app.bulletInfo[index][0] + (newDistance*(app.bulletInfo[index][3]
      -app.bulletInfo[index][0]))/distance)
  y = (app.bulletInfo[index][1] + (newDistance*(app.bulletInfo[index][4]
      -app.bulletInfo[index][1]))/distance)
  app.bulletInfo[index][0], app.bulletInfo[index][1] = (x, y)

# moves a tank by updating its center position
def doStep(app, tank, speed):
  if tank == "user":
    index = 0
  elif tank == "normal": 
    index = 1
  elif tank == "attack":
    index = 2
  if app.tankDirections[index][0]== True:
    app.tankCenters[index][1] -= speed
  elif app.tankDirections[index][1]== True:
    app.tankCenters[index][0] += speed
  elif app.tankDirections[index][2]== True:
    app.tankCenters[index][1] += speed
  elif app.tankDirections[index][3]== True: 
    app.tankCenters[index][0] -= speed
  elif app.tankDirections[index][4]== True: 
    app.tankCenters[index][0] += math.sqrt(2) * speed / 2
    app.tankCenters[index][1] -= math.sqrt(2) * speed / 2
  elif app.tankDirections[index][5]== True: 
    app.tankCenters[index][0] += math.sqrt(2) * speed / 2
    app.tankCenters[index][1] += math.sqrt(2) * speed / 2
  elif app.tankDirections[index][6]== True: 
    app.tankCenters[index][0] -= math.sqrt(2) * speed / 2
    app.tankCenters[index][1] += math.sqrt(2) * speed / 2
  elif app.tankDirections[index][7]== True:
    app.tankCenters[index][0] -= math.sqrt(2) * speed / 2
    app.tankCenters[index][1] -= math.sqrt(2) * speed / 2

# enemy tanks move into position to shoot the player
def seek(app, tank):
  if tank == "normal":
    index = 1
    verticalDecisionDis = 150
  elif tank == "attack":
    index = 2
    verticalDecisionDis = app.tankHeight
  distance = math.sqrt(((app.tankCenters[0][0]-app.tankCenters[index][0])**2+
                      (app.tankCenters[0][1]-app.tankCenters[index][1])**2))
  # dodge the player's missile
  if app.shoot[0] and app.bulletBounces[0] < 1:
    if (app.tankCenters[index][0] + verticalDecisionDis > app.bulletInfo[0][0] 
      and app.tankCenters[index][1] + verticalDecisionDis > app.bulletInfo[0][1]):
      if app.randInt == 1:
        app.tankDirections[index][2] = True
      else:
        app.tankDirections[index][1] = True
    elif (app.tankCenters[index][0] < 
      app.bulletInfo[0][0] - verticalDecisionDis and app.tankCenters[index][1] 
      + verticalDecisionDis > app.bulletInfo[0][1]): 
      if app.randInt == 1:
        app.tankDirections[index][1] = True
      else:
        app.tankDirections[index][3] = True
    elif (app.tankCenters[index][0] + verticalDecisionDis > 
          app.bulletInfo[0][0] and app.tankCenters[index][1] < 
          app.bulletInfo[0][1] - verticalDecisionDis): 
      if app.randInt == 1:
        app.tankDirections[index][1] = True
      else:
        app.tankDirections[index][3] = True
    elif (app.tankCenters[index][0] < app.bulletInfo[0][0] - 
          verticalDecisionDis and app.tankCenters[index][1] 
          < app.bulletInfo[0][1] - verticalDecisionDis): 
      if app.randInt == 1:
        app.tankDirections[index][3] = True
      else:
        app.tankDirections[index][1] = True
    elif (app.tankCenters[index][0] > app.bulletInfo[0][0] and 
        app.bulletInfo[0][1] - verticalDecisionDis <= app.tankCenters[index][1]
         <= app.bulletInfo[0][1] + verticalDecisionDis): 
      if app.randInt == 1:
        app.seW = True
      else:
        app.tankDirections[index][4] = True
    elif  (app.tankCenters[index][1] > app.bulletInfo[0][1] and 
      app.bulletInfo[0][0] - verticalDecisionDis <= app.tankCenters[index][0] 
      <= app.bulletInfo[0][0] + verticalDecisionDis): 
      if app.randInt == 1:
        app.nwW = True
      else:
        app.tankDirections[index][6] = True
    elif (app.tankCenters[index][0] < app.bulletInfo[0][0] and 
        app.bulletInfo[0][1] - verticalDecisionDis <= app.tankCenters[index][1]
        <= app.bulletInfo[0][1] + verticalDecisionDis): 
      if app.randInt == 1:
        app.seW = True
      else:
        app.tankDirections[index][4] = True
    elif (app.tankCenters[index][1] < app.bulletInfo[0][1] and 
          app.bulletInfo[0][0] - verticalDecisionDis <= 
          app.tankCenters[index][0] <= app.bulletInfo[0][0] + 
          verticalDecisionDis): 
      if app.randInt == 1:
        app.swW = True
      else:
        app.tankDirections[index][4] = True
  else:
    if tank == "normal":
      x = 550
      x1 = 300
    elif tank == "attack":
      x = 1
      x1 = 0.01
    app.tankDirections[index][7] = False
    app.tankDirections[index][6] = False
    app.tankDirections[index][4] = False
    app.tankDirections[index][5] = False
    app.tankDirections[index][2] = False
    app.tankDirections[index][0] = False
    app.tankDirections[index][1] = False
    app.tankDirections[index][3] = False
    if distance > x:  
      if (app.tankCenters[index][0] + verticalDecisionDis > 
        app.tankCenters[0][0] and app.tankCenters[index][1] + 
        verticalDecisionDis > app.tankCenters[0][1]):
        app.tankDirections[index][7] = True
      elif (app.tankCenters[index][0] < app.tankCenters[0][0] - 
        verticalDecisionDis and app.tankCenters[index][1] + verticalDecisionDis 
        > app.tankCenters[0][1]): 
        app.tankDirections[index][4] = True
      elif (app.tankCenters[index][0] + verticalDecisionDis > 
        app.tankCenters[0][0] and app.tankCenters[index][1] < 
        app.tankCenters[0][1] - verticalDecisionDis): 
        app.tankDirections[index][6] = True
      elif (app.tankCenters[index][0] < app.tankCenters[0][0] - 
        verticalDecisionDis and app.tankCenters[index][1] < 
          app.tankCenters[0][1] - verticalDecisionDis): 
        app.tankDirections[index][5] = True   
      if (app.tankCenters[index][0] > app.tankCenters[0][0] and 
        app.tankCenters[0][1] - verticalDecisionDis <= app.tankCenters[index][1] 
        <= app.tankCenters[0][1] + verticalDecisionDis): 
        app.tankDirections[index][3] = True
      elif (app.tankCenters[index][1] > app.tankCenters[0][1] and 
        app.tankCenters[0][0] - verticalDecisionDis <= app.tankCenters[index][0] 
        <= app.tankCenters[0][0] + verticalDecisionDis): 
        app.tankDirections[index][0] = True
      elif (app.tankCenters[index][0] < app.tankCenters[0][0] and 
        app.tankCenters[0][1] - verticalDecisionDis <= app.tankCenters[index][1] 
        <= app.tankCenters[0][1] + verticalDecisionDis):  
        app.tankDirections[index][1] = True
      elif (app.tankCenters[index][1] < app.tankCenters[0][1] and 
        app.tankCenters[0][0] - verticalDecisionDis <= app.tankCenters[index][0] 
        <= app.tankCenters[0][0] + verticalDecisionDis): 
        app.tankDirections[index][2] = True
    elif distance < x1:
      if (app.tankCenters[index][0] + verticalDecisionDis > 
        app.tankCenters[0][0] and app.tankCenters[index][1] + 
        verticalDecisionDis > app.tankCenters[0][1]):
        app.tankDirections[index][5] = True
      elif (app.tankCenters[index][0] < app.tankCenters[0][0] - 
        verticalDecisionDis and app.tankCenters[index][1] + 
        verticalDecisionDis > app.tankCenters[0][1]): 
        app.tankDirections[index][6] = True
      elif (app.tankCenters[index][0] + verticalDecisionDis > 
        app.tankCenters[0][0] and app.tankCenters[index][1] < 
        app.tankCenters[0][1] - verticalDecisionDis): 
        app.tankDirections[index][4] = True
      elif (app.tankCenters[index][0] < app.tankCenters[0][0] - 
        verticalDecisionDis and app.tankCenters[index][1] < 
        app.tankCenters[0][1] - verticalDecisionDis): 
        app.tankDirections[index][7] = True   
      if (app.tankCenters[index][0] > app.tankCenters[0][0] and 
        app.tankCenters[0][1] - verticalDecisionDis <= app.tankCenters[index][1] 
        <= app.tankCenters[0][1] + verticalDecisionDis): 
        app.tankDirections[index][1] = True
      elif  (app.tankCenters[index][1] > app.tankCenters[0][1] and 
        app.tankCenters[0][0] - verticalDecisionDis <=
        app.tankCenters[index][0] <= app.tankCenters[0][0] + 
        verticalDecisionDis): 
        app.tankDirections[index][2] = True
      elif (app.tankCenters[index][0] < app.tankCenters[0][0] and 
      app.tankCenters[0][1] - verticalDecisionDis <= app.tankCenters[index][1] 
      <= app.tankCenters[0][1] + verticalDecisionDis):  
        app.tankDirections[index][3] = True
      elif (app.tankCenters[index][1] < app.tankCenters[0][1] and 
      app.tankCenters[0][0] - verticalDecisionDis <= app.tankCenters[index][0] 
      <= app.tankCenters[0][0] + verticalDecisionDis): 
        app.tankDirections[index][0] = True 
    else:
      if app.shootNow[index] == False:
        app.originalBulletPoints[index][0] = app.tankCenters[index][0]
        app.originalBulletPoints[index][1] = app.tankCenters[index][1]
        app.bulletInfo[index][0] = app.tankCenters[index][0]
        app.bulletInfo[index][1] = app.tankCenters[index][1]
        x, y = findDistantPoint(app, app.tankCenters[index][0], 
                app.tankCenters[index][1], app.tankCenters[0][0], 
                app.tankCenters[0][1], tank)
        app.bulletInfo[index][3], app.bulletInfo[index][4] = x, y
        app.shootNow[index] = True
        app.shoot[index] = True

# reroutes the tank if it hits a barrier
def rerouteA(app, tank):
  if tank == "normal":
    index = 1
  elif tank == "attack":
    index = 2
  if not app.nextMoveStatus[index]:  
    if app.centerHelpers[index][0]:
      app.centerHelpers[index][0] = False
      app.ogPoints[index][0] = app.tankCenters[index][0]
      app.ogPoints[index][1] = app.tankCenters[index][1]
      if app.tankDirections[index][0]:
        app.tankDirections[index][2] = True
        app.tankDirections[index][0] = False
      elif app.tankDirections[index][1]:
        app.tankDirections[index][3] = True
        app.tankDirections[index][1] = False
      elif app.tankDirections[index][3]:
        app.tankDirections[index][1] = True
        app.tankDirections[index][3] = False
      elif app.tankDirections[index][2]:
        app.tankDirections[index][0] = True
        app.tankDirections[index][2] = False
      elif app.tankDirections[index][4]:
        app.tankDirections[index][6] = True
        app.tankDirections[index][4] = False
      elif app.tankDirections[index][7]:
        app.tankDirections[index][5] = True
        app.tankDirections[index][7] = False  
      elif app.tankDirections[index][6]:
        app.tankDirections[index][4] = True
        app.tankDirections[index][6] = False
      elif app.tankDirections[index][5]:
        app.tankDirections[index][7] = True
        app.tankDirections[index][5] = False
    distance = math.sqrt(((app.tankCenters[index][0]-app.ogPoints[index][0])**2
                        +(app.tankCenters[index][1]-app.ogPoints[index][1])**2))
    if distance > app.tankWidth/2:
      app.nextMoveStatus[index] = True
      if app.tankDirections[index][1] or app.tankDirections[index][3]:
        if app.tankCenters[index][1]>app.tankCenters[0][1]:
          app.tankDirections[index][0] = True
        else:
          app.tankDirections[index][2] = True
      else: 
        if app.tankCenters[index][0]>app.tankCenters[0][0]:
          app.tankDirections[index][3] = True
        else:
          app.tankDirections[index][1] = True
  else:
    if app.centerHelpers[index][1]:
      app.centerHelpers[index][1] = False
      app.ogPoints[index][0] = app.tankCenters[index][0]
      app.ogPoints[index][1] = app.tankCenters[index][1]

    distance = math.sqrt(((app.tankCenters[index][0]-app.ogPoints[index][0])**2
                      +(app.tankCenters[index][1]-app.ogPoints[index][1])**2))
    if distance > app.tankWidth/2: 
      app.findingPath[index] = app.nextMoveStatus[index] = False

# reroutes the tank if it hits a wall   
def rerouteB(app, tank):
  if tank == "normal":
    index = 1
  elif tank == "attack":
    index = 2
  if app.centerHelpers[index][0]:  
    app.centerHelpers[index][0] = False
    app.ogPoints[index][0] = app.tankCenters[index][0]
    app.ogPoints[index][1] =  app.tankCenters[index][1]
    if app.tankDirections[index][0] or app.tankDirections[index][2]:
      if app.tankDirections[index][0]:
        app.tankCenters[index][1] += app.barrierBounce
      else:
        app.tankCenters[index][1] -= app.barrierBounce
      if app.tankCenters[index][0] > app.width/2:
        app.tankDirections[index][3] = True
      else:
        app.tankDirections[index][1] = True
      app.tankDirections[index][0] = app.tankDirections[index][2] = False
    elif app.tankDirections[index][1] or app.tankDirections[index][3]:
      if app.tankDirections[index][1]:
        app.tankCenters[index][0] -= app.barrierBounce
      else:
        app.tankCenters[index][0] += app.barrierBounce
      if app.tankCenters[index][1] > app.height/2:
        app.tankDirections[index][0] = True
      else:
        app.tankDirections[index][2] = True
      app.tankDirections[index][1] = app.tankDirections[index][3] = False
    else:
      if app.tankDirections[index][7]:
        app.tankCenters[index][0] += app.barrierBounce
        app.tankCenters[index][1] += app.barrierBounce
        if (app.tankCenters[index][0] - app.margin > app.tankCenters[index][1] 
          - app.topMargin):
          app.tankDirections[index][1] = True
        else:
          app.tankDirections[index][2] = True
      elif app.tankDirections[index][4]:
        app.tankCenters[index][0] -= app.barrierBounce
        app.tankCenters[index][1] += app.barrierBounce
        if (app.width - app.tankCenters[index][0] - app.margin > 
          app.tankCenters[index][1] - app.topMargin):
          app.tankDirections[index][3] = True
        else:
          app.tankDirections[index][2] = True
      elif app.tankDirections[index][6]:
        app.tankCenters[index][0] += app.barrierBounce
        app.tankCenters[index][1] -= app.barrierBounce
        if (app.tankCenters[index][0] - app.margin > app.height 
          - app.tankCenters[index][1] - app.topMargin):
          app.tankDirections[index][3] = True
        else:
          app.tankDirections[index][0] = True
      else:
        app.tankCenters[index][0] -= app.barrierBounce
        app.tankCenters[index][1] -= app.barrierBounce
        if (app.width - app.tankCenters[index][0] - 
          app.margin > app.height - app.tankCenters[index][1] - app.topMargin):
          app.tankDirections[index][3] = True
        else:
          app.tankDirections[index][0] = True
      app.tankDirections[index][4] = False
      app.tankDirections[index][7] = False
      app.tankDirections[index][5] = False
      app.tankDirections[index][6] = False
  else:
    distance = math.sqrt(((app.tankCenters[index][0]-app.ogPoints[index][0])**2
                      +(app.tankCenters[index][1]-app.ogPoints[index][1])**2))
    if distance > 150: 
      app.findingPath[index] = False

# has gun follow the user tank
def enemyTankMotion(app, tank):
  if tank == "normal":
    index = 1
    images = app.normalTankIm
  elif tank == "attack":
    index = 2
    images = app.attackTankIm
  lookX, lookY = app.tankCenters[0][0], app.tankCenters[0][1]
  lookY = lookY - 45
  sideX, sideY = lookX-app.tankCenters[index][0], lookY-app.tankCenters[index][1]
  degree = int((180 / math.pi) * math.atan2(sideX, sideY))
  armOrientation(app, degree-180, app.armDirection, images, tank)

# has gun follow the mouse position
def armMotion(app):
  lookX, lookY = pyautogui.position()
  lookY = lookY - 45
  sideX, sideY = lookX-app.tankCenters[0][0], lookY-app.tankCenters[0][1]
  degree = int((180 / math.pi) * math.atan2(sideX, sideY))
  armOrientation(app, degree-180, app.armDirection, app.userTankIm, "user")

# bounces a tank off a barrier depending on its direction
def barrierBounce(app, tank):
  if tank == "user":
    index = 0
  elif tank == "normal":
    index = 1
  if app.tankDirections[index][0]:
    app.tankCenters[index][1] += app.barrierBounce
  elif app.tankDirections[index][1]:
    app.tankCenters[index][0] -= app.barrierBounce
  elif app.tankDirections[index][2]:
    app.tankCenters[index][1] -= app.barrierBounce
  elif app.tankDirections[index][3]:
    app.tankCenters[index][0] += app.barrierBounce
  elif app.tankDirections[index][4]: 
    app.tankCenters[index][0] -= app.barrierBounce
    app.tankCenters[index][1] += app.barrierBounce
  elif app.tankDirections[index][7]:
    app.tankCenters[index][0] += app.barrierBounce
    app.tankCenters[index][1] += app.barrierBounce
  elif app.tankDirections[index][6]:
    app.tankCenters[index][0] += app.barrierBounce
    app.tankCenters[index][1] -= app.barrierBounce  
  elif app.tankDirections[index][5]:
    app.tankCenters[index][0] -= app.barrierBounce
    app.tankCenters[index][1] -= app.barrierBounce

  app.tankDirections[index][0]= app.tankDirections[index][1]= app.tankDirections[index][2]= app.tankDirections[index][3]= app.tankDirections[index][4]= app.tankDirections[index][5]= app.tankDirections[index][6]= app.tankDirections[index][7]= False
  app.tankEdges[index] = ([app.margin+1,app.topMargin+1,app.margin+1,
                      app.topMargin+1,app.margin+1,app.topMargin+1,
                      app.margin+1,app.topMargin+1])

##############################################################
# 5.) STORING OR UPDATING VALUES 
##############################################################

# updates the coordinates of a tank's edges for its current direction
def tankEdges(app, tank):
  if tank == "user":
    index = 0
  elif tank == "normal":
    index = 1
  elif tank == "attack":
    index = 2
  hW = app.tankHeight/2
  hH = app.tankHeight/2

  if app.tankDirections[index][1]or app.tankDirections[index][3]:
    app.tankEdges[index] = ([app.tankCenters[index][0]-app.tankWidth/2, 
                      app.tankCenters[index][1]-app.tankHeight/2, 
                      app.tankCenters[index][0]+app.tankWidth/2, 
                      app.tankCenters[index][1]-app.tankHeight/2,
                      app.tankCenters[index][0]+app.tankWidth/2, 
                      app.tankCenters[index][1]+app.tankHeight/2,
                      app.tankCenters[index][0]-app.tankWidth/2, 
                      app.tankCenters[index][1]+app.tankHeight/2])
  elif app.tankDirections[index][0]or app.tankDirections[index][2]:
    app.tankEdges[index] = ([app.tankCenters[index][0]-app.tankHeight/2, 
                            app.tankCenters[index][1]-app.tankWidth/2, 
                            app.tankCenters[index][0]+app.tankHeight/2, 
                            app.tankCenters[index][1]-app.tankWidth/2,
                            app.tankCenters[index][0]+app.tankHeight/2, 
                            app.tankCenters[index][1]+app.tankWidth/2,
                            app.tankCenters[index][0]-app.tankHeight/2, 
                            app.tankCenters[index][1]+app.tankWidth/2])
  elif app.tankDirections[index][4]or app.tankDirections[index][5]or app.tankDirections[index][7]or app.tankDirections[index][6]:
    if app.tankDirections[index][7]or app.tankDirections[index][5]:
      newX = ((app.tankCenters[index][0]+((hW*math.cos(math.pi/4))
              -(hH*math.sin(math.pi/4)))+hW/2))
      newY = ((app.tankCenters[index][1]+((hW*math.sin(math.pi/4))
              +(hH*math.cos(math.pi/4)))+hW/2))
      newX1 = ((app.tankCenters[index][0]+((hW*math.sin(math.pi/4))
              +(hH*math.cos(math.pi/4)))+hW/2))
      newY1 = ((app.tankCenters[index][1]+((hW*math.cos(math.pi/4))
              -(hH*math.sin(math.pi/4)))+hW/2))
      newX2 = ((app.tankCenters[index][0]-((hW*math.cos(math.pi/4))
              -(hH*math.sin(math.pi/4)))-hW//2))
      newY2 = ((app.tankCenters[index][1]-((hW*math.sin(math.pi/4))
              +(hH*math.cos(math.pi/4)))-hW//2))
      newX3 = ((app.tankCenters[index][0]-((hW*math.sin(math.pi/4))
              +(hH*math.cos(math.pi/4)))-hW//2))
      newY3 = ((app.tankCenters[index][1]-((hW*math.cos(math.pi/4))
              -(hH*math.sin(math.pi/4)))-hW//2))
    else:
      newX = ((app.tankCenters[index][0]-((hW*math.cos(math.pi/4))
          -(hH*math.sin(math.pi/4)))-hW/2))
      newY = ((app.tankCenters[index][1]+((hW*math.sin(math.pi/4))
          +(hH*math.cos(math.pi/4)))+hW/2))
      newX1 = ((app.tankCenters[index][0]-((hW*math.sin(math.pi/4))
          +(hH*math.cos(math.pi/4)))-hW/2))
      newY1 = ((app.tankCenters[index][1]+((hW*math.cos(math.pi/4))
          -(hH*math.sin(math.pi/4)))+hW/2))
      newX2 = ((app.tankCenters[index][0]+((hW*math.cos(math.pi/4))
          -(hH*math.sin(math.pi/4)))+hW//2))
      newY2 = ((app.tankCenters[index][1]-((hW*math.sin(math.pi/4))
          +(hH*math.cos(math.pi/4)))-hW//2))
      newX3 = ((app.tankCenters[index][0]+((hW*math.sin(math.pi/4))
          +(hH*math.cos(math.pi/4)))+hW//2))
      newY3 = ((app.tankCenters[index][1]-((hW*math.cos(math.pi/4))
          -(hH*math.sin(math.pi/4)))-hW//2))   
    app.tankEdges[index] = (newX, newY, newX1, newY1, newX2, newY2, newX3, newY3)

# updates the shooting and explosion status of tanks
def updateShootingStatus(app, bulletType):
  if bulletType == "user":
    index = 0
    other = "normal"
    other2 = "attack"
  elif bulletType == "normal":
    index = 1
    other = "user"
  elif bulletType == "attack":
    index = 2
    other = "user"
  if app.shootNow[index] == True:
    if app.shoot[index] == True:
      

      if bulletType == "user":
        checkBulletHitTank(app, bulletType, other2)
      checkBulletHitTank(app, bulletType, other)
      if app.bulletBounces[index] < 2:
        bulletMotion(app, bulletType)
      else:
        app.explosionInfo[index][1] = app.bulletInfo[index][0]
        app.explosionInfo[index][2] = app.bulletInfo[index][1]
        app.bulletInfo[index][0] = app.tankCenters[index][0]
        app.bulletInfo[index][1] = app.tankCenters[index][1]
        app.explosionInfo[index][0] = True
        app.bulletBounces[index] = 0
        app.shoot[index] = False
        app.shootNow[index] = False
    else:
      app.bulletInfo[index][0] = app.tankCenters[index][0]
      app.bulletInfo[index][1] = app.tankCenters[index][1]
  else:
    app.bulletInfo[index][0] = app.tankCenters[index][0]
    app.bulletInfo[index][1] = app.tankCenters[index][1]

# Updates the level status, enemy bullet speed, enemy speed, enemies remaining,
# and enemies needed to be killed before advancing to the next round
def levelCheck(app):
  if app.tanksRemaining == 0:
    app.nextLevelScreen = True
    app.paused = True
    app.neededTanksKilled = 2 + round(app.level * 1.5)
    app.tanksRemaining = app.neededTanksKilled
    getBarrierData(app)
    app.level += 1
    if app.level % 3 == 0:
      app.bulletSpeed += 1
      app.enemyTankSpeed += 1
  if app.level > 3:
    app.attackTankTime = True

##############################################################
# 6.) CALCULATIONS
############################################################## 
# finds a far point along the shot's line, so the missile keeps going past
# the click (or the CPU's target) instead of stopping there
def findDistantPoint(app, x, y, x1, y1, tank):
  if tank == "user":
    index = 0
  elif tank == "normal":
    index = 1
  elif tank == "attack":
    index = 2 
  if (x1-x) == 0:
    val = (x1-x)+0.0001
  else: 
    val = (x1-x)
  app.bulletSlopes[index] = (y1-y)/(x1-x)
  slope = (y1-y)/(x1-x)
  if x1 > x:
    x2, y2 = x1+app.width*2, y1+app.width*2*slope
  else:
    x2, y2 = x1-app.width*2, y1-app.width*2*slope
  return (x2, y2)

##############################################################
# 7.) CHECKING INTERSECTIONS
##############################################################
# catches edge cases the checks below miss
def correctorFunction(app, tank):
  if tank == "user":
    index = 0
  elif tank == "normal":
    index = 1
  elif tank == "attack":
    index = 2
  
  # frees a tank stuck in a barrier
  for i in range(len(app.barrierCords)):
    if ((app.barrierCords[i][0]<app.tankCenters[index][0]<
      app.barrierCords[i][0]+app.barrierSizes[i][0]) and 
      (app.barrierCords[i][1]<app.tankCenters[index][1]<
      app.barrierCords[i][1]+app.barrierSizes[i][1])):
      if ((app.barrierCords[i][0]<app.tankCenters[index][0]<
      app.barrierCords[i][0]+app.barrierSizes[i][0]/2) and 
      (app.barrierCords[i][1]<app.tankCenters[index][1]<
      app.barrierCords[i][1]+app.barrierSizes[i][1])/2):
      # top left
        app.tankCenters[index][0] -= app.tankWidth/2
        app.tankCenters[index][1] -= app.tankWidth/3
      elif ((app.barrierSizes[i][0]/2+app.barrierCords[i][0]<
      app.tankCenters[index][0]<app.barrierCords[i][0]+app.barrierSizes[i][0]) 
      and (app.barrierCords[i][1]<app.tankCenters[index][1]<
      app.barrierCords[i][1]+app.barrierSizes[i][1])/2):
      # top right
        app.tankCenters[index][0] += app.tankWidth/2
        app.tankCenters[index][1] -= app.tankWidth/3
      elif ((app.barrierCords[i][0]<app.tankCenters[index][0]<
      app.barrierCords[i][0]+app.barrierSizes[i][0]/2) and 
      (app.barrierCords[i][1]+app.barrierSizes[i][1]/2)<
      app.tankCenters[index][1]<app.barrierCords[i][1]+app.barrierSizes[i][1]):
      # bottom left
        app.tankCenters[index][0] -= app.tankWidth/2
        app.tankCenters[index][1] += app.tankWidth/3
      elif ((app.barrierSizes[i][0]/2+app.barrierCords[i][0]<
      app.tankCenters[index][0]<app.barrierCords[i][0]+app.barrierSizes[i][0]) 
      and (app.barrierCords[i][1]+app.barrierSizes[i][1])/2<
      app.tankCenters[index][1]<app.barrierCords[i][1]+app.barrierSizes[i][1]):
      # bottom right 
        app.tankCenters[index][0] += app.tankWidth/2
        app.tankCenters[index][1] += app.tankWidth/3

  # checks if a tank is trying to travel in a certain direction but not moving
  if (app.tankDirections[index][0] or app.tankDirections[index][1] 
    or app.tankDirections[index][2] or app.tankDirections[index][3] 
    or app.tankDirections[index][4] or app.tankDirections[index][5] 
    or app.tankDirections[index][6] or app.tankDirections[index][7]):
    if app.intersectionNow[index]:
      app.correctorNumber += 1
      if app.correctorNumber % 200 == 0:
        if app.tankDirections[index][0]:
          app.tankCenters[index][1] -= app.tankWidth/5
        elif app.tankDirections[index][1]:
          app.tankCenters[index][0] += app.tankWidth/5
        elif app.tankDirections[index][2]:
          app.tankCenters[index][1] += app.tankWidth/5
        elif app.tankDirections[index][3]:
          app.tankCenters[index][0] -= app.tankWidth/5
        elif app.tankDirections[index][4]:
          app.tankCenters[index][0] += app.tankWidth/7
          app.tankCenters[index][1] -= app.tankWidth/8
        elif app.tankDirections[index][5]:
          app.tankCenters[index][0] += app.tankWidth/7
          app.tankCenters[index][1] += app.tankWidth/8
        elif app.tankDirections[index][6]:
          app.tankCenters[index][0] -= app.tankWidth/7
          app.tankCenters[index][1] += app.tankWidth/8
        else:
          app.tankCenters[index][0] -= app.tankWidth/7
          app.tankCenters[index][1] -= app.tankWidth/8
    else:
      app.correctorNumber = 0
  
# checks if the attack tank hits the user
def checkAttackTankHitsUser(app):
  x, y = app.tankCenters[0][0], app.tankCenters[0][1]
  x1, y1 = app.tankCenters[2][0],app.tankCenters[2][1]
  distance = math.sqrt((x1-x)**2+(y1-y)**2)
  if distance < app.tankHeight:
    app.explosionInfo[0][0] = True
    app.explosionInfo[2][0] = True
    app.explosionInfo[0][1] = app.tankCenters[0][0]
    app.explosionInfo[0][2] = app.tankCenters[0][1] 
    app.explosionInfo[2][1] = app.tankCenters[2][0]
    app.explosionInfo[2][2] = app.tankCenters[2][1] 
    app.gameOver = True
    app.tankCenters[0][0] = - 100
    app.tankCenters[2][0] = - 100

# checks a tank against barriers and walls
def checkIntersects(app, listOfCords, tank):
  if tank == "user":
    index = 0
  elif tank == "normal":
    index = 1
  elif tank == "attack":
    index = 2
  
  illegalMove = False
  iBarrier = False
  # if tank intersects barrier
  for x in range(len(listOfCords)):
    if x % 2 == 0:
      for i in range(len(app.barrierCords)):
        if ((app.barrierCords[i][0]<listOfCords[x]<
          app.barrierCords[i][0]+app.barrierSizes[i][0]) and 
          (app.barrierCords[i][1]<listOfCords[x+1]<
          app.barrierCords[i][1]+app.barrierSizes[i][1])):
          illegalMove = True
          iBarrier = True

  # if tank intersects corner of barrier while moving diagonally
  if (app.tankDirections[index][4] or app.tankDirections[index][5] 
    or app.tankDirections[index][6] or app.tankDirections[index][7]):
    for i in range(len(app.barrierCords)):
      if app.tankDirections[index][4]:
        x = app.barrierCords[i][0]
        y = app.barrierCords[i][1]+app.barrierSizes[i][1]
      elif app.tankDirections[index][7]:
        x =  app.barrierCords[i][0]+app.barrierSizes[i][0]
        y = app.barrierCords[i][1]+app.barrierSizes[i][1]
      elif app.tankDirections[index][5]:
        x, y = app.barrierCords[i][0],app.barrierCords[i][1]
      elif app.tankDirections[index][6]:
        x =  app.barrierCords[i][0]+app.barrierSizes[i][0]
        y = app.barrierCords[i][1]
      distance = math.sqrt((app.tankCenters[index][0]-x)**2
                                  +(app.tankCenters[index][1]-y)**2)
      if distance <= app.tankWidth/2:
        illegalMove = True
        iBarier = True

  # if tank intersects the edges of the map 
  for x in range(len(listOfCords)):
    if x % 2 == 0:
      if ((listOfCords[x]>=app.width-app.margin) or 
        (listOfCords[x]<=app.margin) or 
        (listOfCords[x+1]>=app.height-app.margin) or 
        (listOfCords[x+1]<=app.topMargin)):
        illegalMove = True
        iEdge = True
  
  if illegalMove:
    app.intersectionNow[index] = True
    if tank == "user": 
      barrierBounce(app, tank)
    elif tank == "normal":
      if not app.findingPath[1]:
        if iBarrier:
          app.findingPath[1] = True
          app.centerHelpers[1][0] = True
          app.centerHelpers[1][1] = True
        else:
          app.findingPath[1] = True
          app.centerHelpers[1][0] = True
          rerouteB(app, tank)
    elif tank == "attack":
      if not app.findingPath[2]:
        if iBarrier:
          app.findingPath[2] = True
          app.centerHelpers[2][0] = True
          app.centerHelpers[2][1] = True
        else:
          app.findingPath[2] = True
          app.centerHelpers[2][0] = True
          rerouteB(app, tank)

  if (app.tankDirections[index][0]or app.tankDirections[index][2] 
  or app.tankDirections[index][1] or app.tankDirections[index][3]):
    for i in range(len(app.barrierCords)):
      if app.tankDirections[index][0] or app.tankDirections[index][2]:
        w = app.tankHeight
        h = app.tankWidth
      else:
        w = app.tankWidth
        h = app.tankHeight
      x, y = (app.barrierCords[i][0]+app.barrierSizes[i][0]/2,
              app.barrierCords[i][1]+app.barrierSizes[i][1]/2)
      distance = max(abs((app.tankCenters[index][0]-x)
                -(w+app.barrierSizes[i][0])/2),
                abs(app.tankCenters[index][1]-y)-(h+app.barrierSizes[i][1])/2)
      if distance <= app.tankHeight/2:
        app.noTurn[index] = True
      else:
        app.noTurn[index] = False
    if abs(app.tankCenters[index][0]-app.margin)<=app.tankHeight+10:
      app.tankCenters[index][0] += app.barrierBounce
    elif (abs(app.width-app.margin-app.tankCenters[index][0])
      <=app.tankHeight/2+10):
      app.tankCenters[index][0] -= app.barrierBounce
    elif (abs(app.margin+app.topMargin-app.tankCenters[index][1])
      <=app.tankHeight/2+10):
      app.tankCenters[index][1] += app.barrierBounce
    elif (abs(app.height-app.margin-app.tankCenters[index][1])
      <=app.tankHeight/2+10):
      app.tankCenters[index][1] -= app.barrierBounce

# checks a missile against barriers and walls
def checkBulletIntersects(app, bulletType):
  if bulletType == "user":
    index = 0
  else:
    index = 1
  
  # BULLET  
  # left
  leftToTop = leftToBottom = rightToBottom = rightToTop = False
  topToRight = topToLeft = bottomToLeft = bottomToRight = False
  if (app.bulletInfo[index][0]+app.bulletInfo[index][2] >= app.width-app.margin 
    and app.bulletSlopes[index] > 0):
    leftToBottom = True
  elif (app.bulletInfo[index][0]+app.bulletInfo[index][2] >= 
        app.width-app.margin and app.bulletSlopes[index] < 0):
    leftToTop = True
  # right
  elif (app.bulletInfo[index][0]-app.bulletInfo[index][2] <= app.margin and 
    app.bulletSlopes[index] < 0):
    rightToBottom = True
  elif (app.bulletInfo[index][0]-app.bulletInfo[index][2] <= app.margin and 
    app.bulletSlopes[index] > 0):
    rightToTop = True
  # top
  elif (app.bulletInfo[index][1]-app.bulletInfo[index][2] <= app.topMargin 
    and app.bulletInfo[index][0] > app.originalBulletPoints[index][0]):
    topToRight = True
  elif (app.bulletInfo[index][1]-app.bulletInfo[index][2] <= app.topMargin and 
    app.bulletInfo[index][0] < app.originalBulletPoints[index][0]):
    topToLeft = True
  # bottom
  elif (app.bulletInfo[index][1]+app.bulletInfo[index][2] >= 
    app.height-app.margin and app.bulletInfo[index][0] < 
    app.originalBulletPoints[index][0]):
    bottomToLeft = True
  elif (app.bulletInfo[index][1]+app.bulletInfo[index][2] >= 
    app.height-app.margin and app.bulletInfo[index][0] > 
    app.originalBulletPoints[index][0]):
    bottomToRight = True

  

  for i in range(len(app.barrierCords)):
    # left
    if (app.barrierCords[i][0]<=app.bulletInfo[index][0]
      -app.bulletInfo[index][2]<=app.barrierCords[i][0]+app.barrierSizes[i][0]<=
      app.originalBulletPoints[index][0] and app.barrierCords[i][1]<=
      app.bulletInfo[index][1]<=app.barrierCords[i][1]+app.barrierSizes[i][1] 
      and app.bulletSlopes[index] > 0):
      rightToTop = True
    elif (app.barrierCords[i][0]<=app.bulletInfo[index][index]
      -app.bulletInfo[index][2]<=app.barrierCords[i][0]+app.barrierSizes[i][0]
      <=app.originalBulletPoints[index][0] and app.barrierCords[i][1]
      <=app.bulletInfo[index][1]<=app.barrierCords[i][1]+app.barrierSizes[i][1] 
      and app.bulletSlopes[index] < 0):
      rightToBottom = True
    # right
    elif (app.originalBulletPoints[index][0]<=app.barrierCords[i][0]<=
      app.bulletInfo[index][0]+app.bulletInfo[index][2]<app.barrierCords[i][0]
      +app.barrierSizes[i][0] and app.barrierCords[i][1]
      <=app.bulletInfo[index][1]<=app.barrierCords[i][1]+app.barrierSizes[i][1] 
      and app.bulletSlopes[index] > 0):
      leftToBottom = True
    elif (app.originalBulletPoints[index][0]<=app.barrierCords[i][0]<=
      app.bulletInfo[index][0]+app.bulletInfo[index][2]<=
      app.barrierCords[i][index]+app.barrierSizes[i][0] and 
      app.barrierCords[i][1]<=app.bulletInfo[index][1]<=app.barrierCords[i][1]
      +app.barrierSizes[i][1] and app.bulletSlopes[index] < 0):
      leftToTop = True
     # top
    elif (app.barrierCords[i][1]<=app.bulletInfo[index][1]
      -app.bulletInfo[index][2]<=app.barrierCords[i][1]+app.barrierSizes[i][1]
      <=app.originalBulletPoints[index][1] and app.barrierCords[i][0]
      <=app.bulletInfo[index][0]<=app.barrierCords[i][0]+app.barrierSizes[i][0] 
      and app.originalBulletPoints[index][0]<app.bulletInfo[index][0]):
      topToRight = True
    elif (app.barrierCords[i][1]<=app.bulletInfo[index][1]
      -app.bulletInfo[index][2]<=app.barrierCords[i][1]+app.barrierSizes[i][1]
      <= app.originalBulletPoints[index][1] and app.barrierCords[i][0]<=
      app.bulletInfo[index][0]<=app.barrierCords[i][0]+app.barrierSizes[i][0] 
      and app.originalBulletPoints[index][0]>app.bulletInfo[index][0]):
      topToLeft = True
    # bottom
    elif (app.originalBulletPoints[index][1]<=app.barrierCords[i][1]<=
      app.bulletInfo[index][1]-app.bulletInfo[index][2]<=app.barrierCords[i][1]
      +app.barrierSizes[i][1] and app.barrierCords[i][0]<=
      app.bulletInfo[index][0]<=app.barrierCords[i][0]+app.barrierSizes[i][0] 
      and app.originalBulletPoints[index][0]>app.bulletInfo[index][0]):
      bottomToLeft = True
    elif (app.originalBulletPoints[index][1]<=app.barrierCords[i][1]<=
      app.bulletInfo[index][1]+app.bulletInfo[index][2]<= 
      app.barrierCords[i][1]+app.barrierSizes[i][1] and app.barrierCords[i][0]
      <=app.bulletInfo[index][0]<=app.barrierCords[i][0]+app.barrierSizes[i][0] 
      and app.originalBulletPoints[index][0]<app.bulletInfo[index][0]):
      bottomToRight = True
  
  if leftToBottom:
    app.bulletInfo[index][3] = app.originalBulletPoints[index][0]-app.width
    app.bulletInfo[index][4] = ((app.bulletInfo[index][1]
      -app.originalBulletPoints[index][1])*2-app.width*-app.bulletSlopes[index])
    app.bulletBounces[index] += 1
  elif leftToTop:
    app.bulletInfo[index][3] = app.originalBulletPoints[index][0]-app.width
    app.bulletInfo[index][4] = (-(app.bulletInfo[index][1]
      -app.originalBulletPoints[index][1])*2-app.width*-app.bulletSlopes[index])
    app.bulletBounces[index] += 1
  elif rightToBottom:
    app.bulletInfo[index][3] = app.originalBulletPoints[index][0]+app.width
    app.bulletInfo[index][4] = ((app.bulletInfo[index][1]
      -app.originalBulletPoints[index][1])*2+app.width*-app.bulletSlopes[index])
    app.bulletBounces[index] += 1
  elif rightToTop:
    app.bulletInfo[index][3] = app.originalBulletPoints[index][0]+app.width
    app.bulletInfo[index][4] = (-(app.bulletInfo[index][1]
      -app.originalBulletPoints[index][1])*2-app.width*+app.bulletSlopes[index])
    app.bulletBounces[index] += 1
  elif topToRight:
    app.bulletInfo[index][3] = ((app.bulletInfo[index][0]
                            -app.originalBulletPoints[index][0])*2+app.width)
    app.bulletInfo[index][4] = (app.originalBulletPoints[index][0]
                                        +app.width*-app.bulletSlopes[index])
    app.bulletBounces[index] += 1
  elif topToLeft:
    app.bulletInfo[index][3] = (-(app.bulletInfo[index][0]
                              -app.originalBulletPoints[index][0])*2-app.width)
    app.bulletInfo[index][4] = (app.originalBulletPoints[index][0]
                                            +app.width*app.bulletSlopes[index])
    app.bulletBounces[index] += 1
  elif bottomToRight:
    app.bulletInfo[index][3] = ((app.bulletInfo[index][0]
                              -app.originalBulletPoints[index][0])*2+app.width)
    app.bulletInfo[index][4] = (app.originalBulletPoints[index][0]
                              +app.width*-app.bulletSlopes[index])
    app.bulletBounces[index] += 1
  elif bottomToLeft:
    app.bulletInfo[index][3] = (-(app.bulletInfo[index][index]
                              -app.originalBulletPoints[index][0])*2-app.width)
    app.bulletInfo[index][4] = (app.originalBulletPoints[index][0]
                                            +app.width*app.bulletSlopes[index])
    app.bulletBounces[index] += 1

# checks missiles against tanks
def checkBulletHitTank(app, bulletType, tank):
  if bulletType == "user":
    bIndex = 0
  elif bulletType == "normal":
    bIndex = 1
  elif bulletType == "attack":
    bIndex = 2
  if tank == "user":
    tIndex = 0
  elif tank == "normal":
    tIndex = 1
  elif tank == "attack":
    tIndex = 2

  # diagonal 
  tankArea = app.tankWidth * app.tankHeight 
  area = 0
  for i in range(len(app.tankEdges[tIndex])):
    if i % 2 == 0:
      index1 = (i+2) % 7
      index2 = (i+3) % 7
      val = (abs((app.tankEdges[tIndex][index1] * app.tankEdges[tIndex][i+1] 
        - app.tankEdges[tIndex][i] * app.tankEdges[tIndex][index2]) 
        + (app.bulletInfo[bIndex][0] * app.tankEdges[tIndex][index2]
        - app.tankEdges[tIndex][index1] * app.bulletInfo[bIndex][1]) 
        + (app.tankEdges[tIndex][i] * app.bulletInfo[bIndex][1] 
        - app.bulletInfo[bIndex][0] * app.tankEdges[tIndex][i+1])) / 2)
      area += val

  xD, yD = app.tankCenters[tIndex][0], app.tankCenters[tIndex][1]
  xD1, yD1 = app.bulletInfo[bIndex][0], app.bulletInfo[bIndex][1]
  distance1 = math.sqrt((xD1-xD)**2+(yD1-yD)**2)

  # checks diagonal and straight
  if (area < tankArea or (app.tankEdges[tIndex][0]<app.bulletInfo[bIndex][0]<
    app.tankEdges[tIndex][4] and app.tankEdges[tIndex][1]<
    app.bulletInfo[bIndex][1]<app.tankEdges[tIndex][5]) or (distance1 < 
    app.tankHeight/2)):
    app.explosionInfo[tIndex][0] = True
    app.explosionInfo[tIndex][1] = app.tankCenters[tIndex][0]
    app.explosionInfo[tIndex][2] = app.tankCenters[tIndex][1] 
    if tIndex == 0:
      app.gameOver = True
      app.tankCenters[tIndex][0] = - 100
    else:
      if tank == "normal":
        app.score += 2
      elif tank == "attack":
        app.score += 1
      app.tanksRemaining -= 1
      app.explosionInfo[tIndex][0] = True
      app.shoot[bIndex] = False
      app.shootNow[bIndex] = False
      if app.tankCenters[0][1] > app.height/2:
        app.tankCenters[tIndex][0] = random.randint(200,1100)
        app.tankCenters[tIndex][1] = app.margin + app.tankWidth*2
        app.tankDirections[tIndex][2] = True
      else:
        app.tankCenters[tIndex][0] = random.randint(200,1100)
        app.tankCenters[tIndex][1] = app.height - app.margin - app.tankWidth *2
        app.tankDirections[tIndex][0] = True

##############################################################
# 8.) DRAW FUNCTIONS  
##############################################################
# DRAWING THE SCREENS
def drawInstructions(app, canvas):
  canvas.create_rectangle(0,0,app.width, app.height, fill = "light green") 
  canvas.create_text(app.width/2, app.margin + 50, text = 'INSTRUCTIONS', font="Times 40 bold", fill="black") 
  canvas.create_text(app.width/2, app.height/1.1, text = 'Press "i" to return to menu', font="Times 30 bold", fill="green") 
  canvas.create_text(app.width/2, app.height/2, text = """
Goal:
    - The goal of the game is to get the highest score possible by destroying enemy tanks.

Levels:
    - Each level offers its own unique barrier set up (can be used as shielding from the bullets of other tanks). 
    There are unlimited levels.
    - Every 3 levels, the speed of the enemy tanks, as well as the speed of the missiles increase.

Tanks:
    - The user tank (you) is the brown tank. 
    - The basic enemy tank is blue and is able to shoot bullets, avoid shots, and chase you around the map. If you are 
    hit by a shot, game over.
    - At level 4, a new tank is introduced called an "attack tank." This tank (yellow) cannot but moves much faster. It 
    is lethal at tracking down the user. If it makes contact with the loser, game over.
    - All tanks are able to move in 8 different directions.

Scoring:
    - Destroying a blue tank (basic enemy tank) is worth two points.
    - Destroying a yellow tank (attack enemy tank) is worth one point.

Controls:
    - The following keys control the direction of the user tank:

                            Q  W  E
                             A  S  D
                              Z  X  C

        "Q" -> NW | "W" -> N | "E" -> NE | "D" -> E | "C" -> SE
              "X" -> S | "Z" -> SW | "A" -> W | "S" -> STOP 
    - The mouse is used to control the gun of the tank. The gun will naturally follow the location of the mouse. 
      Click to shoot!
""",font="Times 16 bold", fill="black")

def drawHighScore(app, canvas): 
  canvas.create_rectangle(0,0,app.width, app.height, fill = "light green") 
  if app.highScore != None:
    canvas.create_text(app.width/2, app.height/4, text = "Your highest score while here was...",font="Times 60 bold", fill="green") 
    canvas.create_text(app.width/2, app.height/2, text = app.highScore, font="Times 200 bold", fill="green")
    canvas.create_text(app.width/2, app.height/1.5, text = "Can you beat it?",font="Times 40 bold", fill="green") 
  else:
    canvas.create_text(app.width/2, app.height/2, text = "< No High Score To Show >", font="Times 60 bold", fill="green")   
  canvas.create_text(app.width/2, app.height/1.1, text = 'Press "h" to return to menu', font="Times 30 bold", fill="green") 

def drawTitleAndScore(app, canvas):
  canvas.create_text(app.width/2, app.topMargin/2, 
                      text="|  |  |     TANKS!     |  |  |", font="Times  40 bold", fill="white")
  canvas.create_text(app.width/2, app.topMargin/2, 
                      text="|  |  |     TANKS!     |  |  |", font="Times  40 bold", fill="white")

  canvas.create_text(app.margin+60, app.topMargin/2+app.margin/2, 
                text=f"Level: {app.level}", font="Times 30 bold", fill="green")
  canvas.create_text(app.margin+230, app.topMargin/2+app.margin/2, 
                text=f"Tanks Left: {app.tanksRemaining}", font="Times 30 bold", fill="orange")
  canvas.create_text(app.margin+400, app.topMargin/2+app.margin/2, 
                text=f"Score: {app.score}", font="Times 30 bold", fill="red")
  canvas.create_text(app.width - 120, app.topMargin/2+app.margin/2, 
                text='press "l" to leave at any point', font="Times 16 bold", fill="white")
  
def drawTitleScreen(app, canvas):
  canvas.create_rectangle(0,0,app.width, app.height, fill = "light green")
  canvas.create_text(app.width/2, app.height/4, 
      text = "T A N K S !",font="Times 200 bold", fill="green")
  canvas.create_text(app.width/2, app.height/1.5, 
      text = "<   Press 1 To Play!   >",font="Times 50 bold", fill="green")
  canvas.create_text(app.width/2, app.height/1.1, 
      text = 'Press "h" For High Score    /    Press "i" For Instructions',font="Times 30 bold", fill="green")

def drawNextLevelScreen(app, canvas):
  canvas.create_rectangle(app.width/2-300, app.height/2-150, 
                          app.width/2+300, app.height/2+150, fill="white")
  canvas.create_text(app.width/2, app.height/2-90, 
              text=f"LEVEL {app.level}", font="Times 80 bold", fill="red")
  canvas.create_text(app.width/2, app.height/2-20, 
              text=f"Kills Need To Advance:", font="Times 30 bold", fill="blue")
  canvas.create_text(app.width/2, app.height/2+60, 
              text=app.tanksRemaining, font="Times 110 bold", fill="blue")
  canvas.create_text(app.width/2, app.height/2+120, 
              text='Press "p" to play...', font="Times 25 bold", fill="red")

def drawGameOver(app, canvas):
  canvas.create_text(app.width/2, app.height/2, 
                      text="GAME OVER!", font="Times 150 bold", fill="red")
                
def drawPaused(app, canvas):
  canvas.create_rectangle(app.width/2-130, app.height/2-30, 
                            app.width/2+130, app.height/2+30, fill = "black")
  canvas.create_text(app.width/2, app.height/2, text='< paused >',  
                                            font="Times 25 bold", fill="red")
                      
def drawFlickerContinue(app, canvas):
  canvas.create_text(app.width/2, app.height/2 + 200, 
                text="Press 1 to continue...", font="Times 50 bold", fill="red")
                    
# DRAWING THE LAYOUT
def drawGrid(app, canvas):
  canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
  canvas.create_rectangle(app.margin, app.topMargin, app.width-app.margin,
                            app.height-app.margin, fill = "light green")

def drawBarrier(app, canvas):
  for i in range(len(app.barrierIm)):
    im = app.barrierIm[i]
    x, y = app.barrierCords[i][0]+app.barrierSizes[i][0]/2,app.barrierCords[i][1]+app.barrierSizes[i][1]/2,
    canvas.create_image(x, y, image=ImageTk.PhotoImage(im))

# DRAWING ANIMATION
def drawExplosion(app, canvas, index):
  sprite = app.explosionIm[app.explosionSpriteCounter]
  canvas.create_image(app.explosionInfo[index][1], app.explosionInfo[index][2], image=ImageTk.PhotoImage(sprite))

# DRAWING THE TANKS
def drawUserTank(app, canvas):
  # tracks
  sprite = app.userTankIm[0][app.spriteCounter[0]]
  if app.directionDegree[0] == 180 or app.directionDegree[0] == 0:
    canvas.create_image(app.tankCenters[0][0]+app.tankHeight/2-5, app.tankCenters[0][1], 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[0][0]-app.tankHeight/2+5, app.tankCenters[0][1], 
                        image=ImageTk.PhotoImage(sprite))
  elif app.directionDegree[0] == 270 or app.directionDegree[0] == 90:
    canvas.create_image(app.tankCenters[0][0], app.tankCenters[0][1]+app.tankHeight/2-5, 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[0][0], app.tankCenters[0][1]-app.tankHeight/2+5, 
                        image=ImageTk.PhotoImage(sprite))
  elif app.directionDegree[0] == 45 or app.directionDegree[0] == 225:
    canvas.create_image(app.tankCenters[0][0]-app.tankHeight/4-math.sqrt(5), 
                        app.tankCenters[0][1]+app.tankHeight/4+math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[0][0]+app.tankHeight/4+math.sqrt(5), 
                        app.tankCenters[0][1]-app.tankHeight/4-math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
  else:
    canvas.create_image(app.tankCenters[0][0]-app.tankHeight/4-math.sqrt(5), 
                        app.tankCenters[0][1]-app.tankHeight/4-math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[0][0]+app.tankHeight/4+math.sqrt(5), 
                        app.tankCenters[0][1]+app.tankHeight/4+math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
  # base
  im = app.userTankIm[1][0]
  canvas.create_image(app.tankCenters[0][0], app.tankCenters[0][1], image=ImageTk.PhotoImage(im))

  # bullet
  canvas.create_oval(app.bulletInfo[0][0]-app.bulletInfo[0][2], app.bulletInfo[0][1]-app.bulletInfo[0][2], app.bulletInfo[0][0]+app.bulletInfo[0][2], app.bulletInfo[0][1]
                      +app.bulletInfo[0][2], fill='black')

  # gun
  im = app.userTankIm[2][0]
  canvas.create_image(app.tankCenters[0][0], app.tankCenters[0][1], image=ImageTk.PhotoImage(im))

def drawNormalTank(app, canvas):
  sprite = app.normalTankIm[0][app.spriteCounter[1]]
  if app.directionDegree[1] == 180 or app.directionDegree[1] == 0:
    canvas.create_image(app.tankCenters[1][0]+app.tankHeight/2-5, app.tankCenters[1][1], 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[1][0]-app.tankHeight/2+5, app.tankCenters[1][1], 
                        image=ImageTk.PhotoImage(sprite))
  elif app.directionDegree[1] == 270 or app.directionDegree[1] == 90:
    canvas.create_image(app.tankCenters[1][0], app.tankCenters[1][1]+app.tankHeight/2-5, 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[1][0], app.tankCenters[1][1]-app.tankHeight/2+5, 
                        image=ImageTk.PhotoImage(sprite))
  elif app.directionDegree[1] == 45 or app.directionDegree[1] == 225:
    canvas.create_image(app.tankCenters[1][0]-app.tankHeight/4-math.sqrt(5), 
                        app.tankCenters[1][1]+app.tankHeight/4+math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[1][0]+app.tankHeight/4+math.sqrt(5), 
                        app.tankCenters[1][1]-app.tankHeight/4-math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
  else:
    canvas.create_image(app.tankCenters[1][0]-app.tankHeight/4-math.sqrt(5), 
                        app.tankCenters[1][1]-app.tankHeight/4-math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[1][0]+app.tankHeight/4+math.sqrt(5), 
                        app.tankCenters[1][1]+app.tankHeight/4+math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))

  # base
  im = app.normalTankIm[1][0]
  canvas.create_image(app.tankCenters[1][0], app.tankCenters[1][1], image=ImageTk.PhotoImage(im))

  # bullet
  canvas.create_oval(app.bulletInfo[1][0]-app.bulletInfo[1][2], app.bulletInfo[1][1]-app.bulletInfo[1][2], app.bulletInfo[1][0]+app.bulletInfo[1][2], app.bulletInfo[1][1]
                      +app.bulletInfo[1][2], fill='black')    

  # gun
  im = app.normalTankIm[2][0]
  canvas.create_image(app.tankCenters[1][0], app.tankCenters[1][1], image=ImageTk.PhotoImage(im))

def drawAttackTank(app, canvas):
  sprite = app.attackTankIm[0][app.spriteCounter[2]]
  if app.directionDegree[2] == 180 or app.directionDegree[2] == 0:
    canvas.create_image(app.tankCenters[2][0]+app.tankHeight/2-5, app.tankCenters[2][1], 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[2][0]-app.tankHeight/2+5, app.tankCenters[2][1], 
                        image=ImageTk.PhotoImage(sprite))
  elif app.directionDegree[2] == 270 or app.directionDegree[2] == 90:
    canvas.create_image(app.tankCenters[2][0], app.tankCenters[2][1]+app.tankHeight/2-5, 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[2][0], app.tankCenters[2][1]-app.tankHeight/2+5, 
                        image=ImageTk.PhotoImage(sprite))
  elif app.directionDegree[2] == 45 or app.directionDegree[2] == 225:
    canvas.create_image(app.tankCenters[2][0]-app.tankHeight/4-math.sqrt(5), 
                        app.tankCenters[2][1]+app.tankHeight/4+math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[2][0]+app.tankHeight/4+math.sqrt(5), 
                        app.tankCenters[2][1]-app.tankHeight/4-math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
  else:
    canvas.create_image(app.tankCenters[2][0]-app.tankHeight/4-math.sqrt(5), 
                        app.tankCenters[2][1]-app.tankHeight/4-math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))
    canvas.create_image(app.tankCenters[2][0]+app.tankHeight/4+math.sqrt(5), 
                        app.tankCenters[2][1]+app.tankHeight/4+math.sqrt(5), 
                        image=ImageTk.PhotoImage(sprite))

  # base
  im = app.attackTankIm[1][0]
  canvas.create_image(app.tankCenters[2][0], app.tankCenters[2][1], image=ImageTk.PhotoImage(im))

  # gun
  im = app.attackTankIm[2][0]
  canvas.create_image(app.tankCenters[2][0], app.tankCenters[2][1], image=ImageTk.PhotoImage(im))

# REDRAWING ALL
def redrawAll(app, canvas):
  # Grid
  drawGrid(app, canvas)
  drawBarrier(app, canvas)
  
  # tanks
  drawUserTank(app, canvas)
  drawNormalTank(app, canvas)
  drawAttackTank(app, canvas)

  # explosions
  if app.explosionInfo[0][0]:
    drawExplosion(app, canvas, 0)
  elif app.explosionInfo[1][0]:
    drawExplosion(app, canvas, 1)
  elif app.explosionInfo[2][0]:
    drawExplosion(app, canvas, 2)
  
  # different screens
  drawTitleAndScore(app, canvas)
  if app.titleScreen:
    drawTitleScreen(app, canvas)
    drawUserTank(app, canvas)
    drawNormalTank(app, canvas)
  elif app.gameOver:
    drawGameOver(app, canvas)
  elif app.flicker:
    drawFlickerContinue(app, canvas)
  elif app.paused:
    drawPaused(app, canvas)
  if app.nextLevelScreen:
    drawNextLevelScreen(app, canvas)
  if app.showHighScore:
    drawHighScore(app, canvas)
  elif app.instructionScreen:
    drawInstructions(app, canvas)

##############################################################
# 9.) RUN THE APP
##############################################################
def main():
  width = 1440
  height = 808
  runApp(width=width, height=height)

if __name__ == '__main__':
  main()

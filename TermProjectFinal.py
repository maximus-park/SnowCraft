from Tkinter import * #andrew ID: hyunminp
from pygame import mixer
import random
#############Key Pressed
def keyPressed(event):
    if event.char == "w":
        canvas.data.greenPlayersList = [] #cheats
    if event.char == "l":
        canvas.data.redPlayersList = [] #cheats
    if event.char == "q":
        qPressed()
    if event.char == "h":
        hPressed()
    if event.keysym == "Return" and canvas.data.level == 0:#must be at starting
        enterPressed()                                     #screen
    if event.char == "r":
        rPressed()
    if event.char=="p" and canvas.data.instruction==False: 
        canvas.data.paused=not(canvas.data.paused)
    if event.char == "n"\
       and len(canvas.data.greenPlayersList)==0 and canvas.data.level!=0:
        nPressed() #can only go to next level when player has beaten level
    redrawAll()

def qPressed(): #quit to main menu
    canvas.data.instruction = False
    canvas.data.level = 0
    init()

def hPressed(): #show instructions
    canvas.data.instruction = not(canvas.data.instruction)
    canvas.data.paused= not(canvas.data.paused)

def enterPressed(): #start the game
    newLevel = canvas.data.sound["newLevel"]
    canvas.data.loadTimer = 100
    canvas.data.level = 1
    newLevel.play()
    init()

def rPressed(): #r is pressed
    newLevel = canvas.data.sound["newLevel"]
    if canvas.data.level != 0:
        newLevel.play()
    canvas.data.instruction = False
    canvas.data.loadTimer = 100
    init() #restart level

def nPressed(): #n is pressed
    newLevel = canvas.data.sound["newLevel"]
    canvas.data.loadTimer = 100
    canvas.data.level += 1 #next level
    if canvas.data.level == 3:
        canvas.data.level = 0 #go back to loading screen
    newLevel.play()
    init()
############
############Game Over 
def gameOver():
    width = canvas.data.width
    height = canvas.data.height
    text = """\n
    You Lose.\n
    Press 'r' to restart level.\n
    Press 'h' for help"""
    if len(canvas.data.redPlayersList)==0 and canvas.data.level>0: #red wins!
        canvas.create_text(width/2,height/2,\
                           text =text,fill = "Blue",font="Helvtica 20 bold")
    elif len(canvas.data.greenPlayersList)==0 and canvas.data.level >0:
        text = """\n
        You Win!!\n
        Press 'n' for next level. \n
        Press 'r' to restart level.\n
        Press 'h' for help"""
        canvas.create_text(width/2,height/2,\
                           text= text,\
                           fill = "Blue",font ="Helvtica 20 bold")#red loses.
    
############
############Snow Ball
def throwSnowBall(): #snow ball is thrown
    canvas.data.snowBallCounter +=1 #nth snowball
    canvas.data.redSnow +=[canvas.data.snowBallCounter] #add snowball to list
    snowballSize = canvas.data.snowballSize
    playerRadius = canvas.data.playerRadius
    d = canvas.data.d
    throwStrength = canvas.data.throwStrength
    [truth,x,y] = canvas.data.playerSelected
    canvas.create_oval(x+playerRadius-5,y-playerRadius+10,\
                       x+playerRadius+snowballSize-5,\
                       y-playerRadius+snowballSize+10,fill="white")
    canvas.data.d[canvas.data.snowBallCounter]= (x+playerRadius,\
                                                 y-playerRadius,\
                                                 x+playerRadius+snowballSize,\
                                                 y-playerRadius+snowballSize,\
                                                 throwStrength) 
    canvas.data.snowballThrown = True     #stores position in dictionary

############
############Timer Fired
def timerFired():
    if canvas.data.paused == False: #only if game isn't paused  
        if canvas.data.playerSelected[0]== True: canvas.data.throwStrength += 1
        snowBallSpeed = canvas.data.snowBallSpeed     #throw strength increases
        for element in canvas.data.redSnow:
            (l,t,r,b,throwStrength) = canvas.data.d[element] #move snowball
            canvas.data.d[element]=(l-snowBallSpeed,t-snowBallSpeed,\
                                    r-snowBallSpeed,b-snowBallSpeed,\
                                    throwStrength-1)
        for element in canvas.data.greenSnow: #move snowball
            (l,t,r,b,throwStrength) = canvas.data.d[element]
            canvas.data.d[element]=(l+snowBallSpeed,t+snowBallSpeed,\
                                    r+snowBallSpeed,b+snowBallSpeed,\
                                    throwStrength)
        greenPlayerAI()
        checkGreen()
        checkRed()
    redrawAll()
    delay = 5 # milliseconds
    canvas.after(delay,timerFired)
############
############Instructions
def drawInstructions(): #instruction screen
    x = canvas.data.width
    y = canvas.data.height
    text = """\n
    Click on red player to select player. \n
    Drag mouse to move player release mouse to throw snowball.\n
    Green bars next to player indicates strength of the throw.\n
    Hit each green player three times to knock them out. \n
    On seond hit green player will fall. \n
    Green player may not be hit while on ground. \n
    Once all green players are knocked out, you win! \n
    If red player is hit, player is stunned for a bit. \n
    If stunned player is hit again, player is knocked out. \n
    Players may not cross into enemy territory. \n 
    Press 'h' to resume play. \n
    Press 'p' to pause. \n
    Press 'q' to return to starting screen. \n
    Press 'r' to restart current level."""
    canvas.create_text(x/2,y/2,text=text,font="Helvtica 10 bold",fill= "blue")
    canvas.data.paused = True
############
############BackGround
def drawBackGround(): #draws the background
    background = canvas.data.image["background"]
    canvas.create_image(canvas.data.width/2, 0, anchor=N, image=background)
    rDead = canvas.data.image["rdead"]
    gDead = canvas.data.image["gdead"]
    playerRadius = canvas.data.playerRadius
    for player in canvas.data.deadRed: #draw dead players as part of the
        (x,y) = player                 #background
        canvas.create_image(x,y,anchor=N, image=rDead)
    for player in canvas.data.deadGreen:
        (x,y) = player
        canvas.create_image(x-playerRadius,y-playerRadius,anchor=N,image=gDead)
############
############redrawAll
def redrawAll():
    canvas.delete(ALL)
    drawBackGround() #draws background
    if canvas.data.instruction == True:
        drawInstructions() #draw instructions
        return None #don't do anything else
    if canvas.data.level == 0: gameStart() #starting screen
    if len(canvas.data.redPlayersList) ==0 or\
       len(canvas.data.greenPlayersList)==0:
        canvas.data.paused = True #game is paused in between levels
        canvas.data.playerSelected[0]=False #player is no longer selected
    for player in canvas.data.redPlayersList: createRedPlayers(player)
    for player in canvas.data.greenPlayersList: createGreenPlayers(player)
    if canvas.data.snowballThrown == True: drawSnowball()
    if canvas.data.playerSelected[0] == True: drawThrowStrength(), snowHand()
    drawFallingSnowBall(),drawSnowSplashes(),drawLevelLoad(),gameOver()

def drawLevelLoad(): #draws loading screen for level
    x = canvas.data.width
    y = canvas.data.height
    level = canvas.data.level
    if level>0 and canvas.data.loadTimer>0: #until load timer = 0, show text
        canvas.data.paused = True
        canvas.data.loadTimer-= 1
        canvas.create_text(x/2,y/2,text = "Level "+str(level),fill = "blue", \
                           font = "Helvetica 50 bold")
    if canvas.data.loadTimer == 0:
        canvas.data.paused = False
        canvas.data.loadTimer -= 1


def drawThrowStrength():#draws the meter next to selected player indicating the
    [truth,x,y] = canvas.data.playerSelected            #strength of the throw
    playerRadius = canvas.data.playerRadius
    boxHeight,boxWidth = canvas.data.boxHeight,canvas.data.boxWidth
    l,t = x+playerRadius,y+playerRadius-boxHeight 
    r,b = l+boxWidth,t+boxHeight  #5 bars shows maximum throw strength
    n = canvas.data.throwStrength/(canvas.data.throwStrengthMaximum/5)
    if n>0: #draw only one bar
        canvas.create_rectangle(l,t,r,b,fill="green")
    if n>1: #draw two bars
        canvas.create_rectangle(l,t-(boxHeight+1),r,b-(boxHeight+1),\
                                fill="green")
    if n>2: #draw three bars
        canvas.create_rectangle(l,t-(boxHeight+1)*2,r,b-(boxHeight+1)*2,\
                                fill="green")
    if n>3: #draw four bars
        canvas.create_rectangle(l,t-(boxHeight+1)*3,r,b-(boxHeight+1)*3,\
                                fill="green")
    if n>4: #draw five bars
        canvas.create_rectangle(l,t-(boxHeight+1)*4,r,b-(boxHeight+1)*4,\
                                fill="green")

def drawSnowball(): #draws snowball and shadow for both green and red
    canvas.data.snow = canvas.data.redSnow + canvas.data.greenSnow 
    shadowDistance = canvas.data.shadowDistance
    for snowball in canvas.data.snow: #for each snowball
        (l,t,r,b,throwStrength) = canvas.data.d[snowball] 
        canvas.create_oval(l,t,r,b,fill="white")
        canvas.create_oval(l,t+shadowDistance,r,b+shadowDistance,fill="black")

def drawFallingSnowBall(): #draws the falling snow ball at the end of it's
    snowSplash = canvas.data.image["snowsplash"] #thrown distance
    for snowBall in canvas.data.fallingSnowBall: #go through each snowball
        (l,t,r,b,shadowDistance) = snowBall
        if shadowDistance ==0: #snowball has hit the ground
            canvas.data.fallingSnowBall.remove(snowBall)
            x = (l+r)/2
            y = t
            splashTime = 5 #splash stays on screen for 5 miliseconds
            canvas.data.snowSplashes += [(x,y,splashTime)]
            continue
        n = canvas.data.fallingSnowBall.index(snowBall)
        fSpeed = canvas.data.fallSpeed           #shadow distance decreases
        canvas.create_oval(l,t,r,b,fill="white") #draw snowball and shadow
        canvas.create_oval(l,t+shadowDistance-1,r,b+shadowDistance-1)
        canvas.data.fallingSnowBall[n] = (l-1,t+fSpeed,r-1,b+fSpeed,\
                                          shadowDistance-fSpeed) 
                                                        

def drawSnowSplashes(): #at the end of the snowball's fall, the snowball makes
    snowSplash = canvas.data.image["snowsplash"] #a little splash
    for splash in canvas.data.snowSplashes: #for each fallen snowball
        (x,y,splashTime) = splash
        if splashTime ==0:                  #to make sure the splash doesn't
            canvas.data.snowSplashes.remove(splash) #stay on screen forever
            continue
        n = canvas.data.snowSplashes.index(splash)
        canvas.create_image(x,y,anchor=N,image=snowSplash) #splash image is
        canvas.data.snowSplashes[n] = (x,y,splashTime-1)   #shown for short
                                                           #duration

def checkGreen(): #go through each player in list
    for player in canvas.data.greenPlayersList:
        (x,y,hitCount,hitTime)=player
        n = canvas.data.greenPlayersList.index(player)
        if hitTime>0: #player is resting from hit
            player = (x,y,hitCount,hitTime-1)
            canvas.data.greenPlayersList[n] = player
            if hitCount ==2: continue #if it is second hit, player is on ground 
        checkGreenHit(player,x,y,hitCount)       #so snowball cannot hit player
        #otherwise, check if player is hit

def checkGreenHit(player,x,y,hitCount): #for specific green player check if 
    greenHit = canvas.data.sound["greenHit"] #player has been hit
    playerRadius,addedHitTime = canvas.data.playerRadius,canvas.data.hitTime
    for rSnow in canvas.data.redSnow: #go through each snowball thrown by red
            (l,t,r,b,throwStrength)=canvas.data.d[rSnow]#snowball is off screen
            if (l<0) or (t<0) or (r>canvas.data.width) or\
               (b>canvas.data.height) or throwStrength == 0: 
                if throwStrength ==0: #snowball has gone it's distance
                    (l,t,r,b,throwStrength) = canvas.data.d[rSnow]
                    shadowDistance = canvas.data.shadowDistance #snowball falls 
                    canvas.data.fallingSnowBall+= [(l,t,r,b,shadowDistance)]
                del canvas.data.d[rSnow]
                canvas.data.redSnow.remove(rSnow) #green player has been hit!
            elif (x-playerRadius)<=l and (y-playerRadius)<= t and\
                 (x+playerRadius)>=r and (y+playerRadius)>=b:
                del canvas.data.d[rSnow] #snowball is gone
                canvas.data.redSnow.remove(rSnow),greenHit.play()
                n = canvas.data.greenPlayersList.index(player)
                canvas.data.greenPlayersList[n] = (x,y,hitCount+1,addedHitTime)
                #hit count goes up and hit time goes up

def checkRed(): #check if a red player has been hit
    redHit = canvas.data.sound["redHit"]
    playerRadius,addedHitTime = canvas.data.playerRadius,canvas.data.hitTime
    for player in canvas.data.redPlayersList: #check each red player
        (x,y,hitTime)=player
        n = canvas.data.redPlayersList.index(player)#subtract one from hit time
        if hitTime>0: canvas.data.redPlayersList[n] = (x,y,hitTime-1)
        for gSnow in canvas.data.greenSnow: #check each snowball if it hit a
            (l,t,r,b,throwStrength) = canvas.data.d[gSnow]              #player
            if (l<0) or (t<0) or\
               (r>canvas.data.width) or (b>canvas.data.height):
                del canvas.data.d[gSnow] #snowball is out of bounds
                canvas.data.greenSnow.remove(gSnow),randomizeCommand(abs(gSnow))
            elif (x-playerRadius)<= l and (y-playerRadius)<= t and\
                 (x+playerRadius)>=r and (y+playerRadius)>=b: #it hit a player
                del canvas.data.d[gSnow]
                canvas.data.greenSnow.remove(gSnow) #snowball is gone
                randomizeCommand(abs(gSnow)),redHit.play() #hit time goes up
                canvas.data.redPlayersList[n]= (x,y,hitTime+addedHitTime)
                if [x,y]==canvas.data.playerSelected[1:3]: #hit player cannot
                    canvas.data.playerSelected=[False,0,0] #be selected

def snowHand(): #draws snowball in the hand of the selected player
    if canvas.data.paused == False:
        if canvas.data.playerSelected[0] == True:
            [truth,x,y]=canvas.data.playerSelected
            playerRadius = canvas.data.playerRadius
            snowballSize = canvas.data.snowballSize
            l = x+playerRadius-5 #magic numbers here are to adjust position
            r = l+snowballSize   #of snowball onto image better so it looks
            t = y-playerRadius+10#like snowball is in the hand
            b = t+snowballSize
            canvas.create_oval(l,t,r,b,fill="white")
            
############
############Mouse Events
def leftMousePressed(event):
    if canvas.data.paused == False: #only if game is not puased
        canvas.data.throwStrength = 0
        canvas.data.mouse["leftPosn"] = (event.x, event.y)
        playerRadius = canvas.data.playerRadius
        for player in xrange(len(canvas.data.redPlayersList)): #check if player
            (x,y,hitTime)=canvas.data.redPlayersList[player]   #is selected
            if event.x>=(x-playerRadius) and event.x<=(x+playerRadius) and\
               event.y>=(y-playerRadius) and event.y<=(y+playerRadius) and\
               hitTime ==0: #hit player cannot be selected
                canvas.data.playerSelected = [True,x,y] #store selected player
                canvas.data.xDistance = event.x-x#the difference between player
                canvas.data.yDistance = event.y-y #and the position of click
                
def leftMouseMoved(event):  #only if game is not paused and player is selected
    if canvas.data.paused == False and canvas.data.playerSelected[0] == True:
        canvas.data.mouse["leftPosn"] = (event.x, event.y)
        playerRadius = canvas.data.playerRadius
        [truth,x,y]= canvas.data.playerSelected
        xDistance,yDistance = canvas.data.xDistance, canvas.data.yDistance
        xPlayer,yPlayer = event.x-xDistance, event.y-yDistance
        hitTime = 0 #if player is selected, player could not have been hit
        if event.x+event.y<=canvas.data.width:xPlayer=canvas.data.width-yPlayer
        #player cannot move to enemy territory
        if event.x>=canvas.data.width:xPlayer=canvas.data.width-playerRadius
        #player may not move out of bounds
        if event.y>=canvas.data.width:yPlayer=canvas.data.width-playerRadius
        else: #player may not move out of bounds
            if event.x<0: xPlayer,yPlayer =0,canvas.data.height
            if event.y<0: yPlayer,xPlayer = 0,canvas.data.width
        n = canvas.data.redPlayersList.index((x,y,hitTime))
        canvas.data.redPlayersList[n]=(xPlayer,yPlayer,hitTime)#store player at
        canvas.data.playerSelected = [truth,xPlayer,yPlayer]    #new location
                
def leftMouseReleased(event):
    if canvas.data.playerSelected[0] == True:     #only if player had
        redThrow = canvas.data.sound["redThrow"]  #already been selected
        redThrow.play()
        canvas.data.mouse["leftPosn"] = (event.x, event.y)
        canvas.data.playerSelected[0] = False     #player is no longer selected
        throwSnowBall() #upon release, snowball is thrown

    
############
############Green AI

def greenPlayerAI():  #the AI for the green players
    for player in xrange(len(canvas.data.greenPlayersList)):
        if canvas.data.greenPlayersList[player][3]>0: #green player is doing
            pass                                      #something
        elif canvas.data.greenOrders[player] ==0:#green player is doing nothing
            randomizeCommand(player)#give player a command
        elif canvas.data.greenOrders[player]==1: #green player is throwing
            greenSnow(player)
            canvas.data.greenOrders[player]=-1
        elif canvas.data.greenOrders[player]==-1: #green player is still
            pass                                  #throwing
        else:
            moveGreen(player) #otherwise it is moving

def randomizeCommand(player): #gives the player a random command from list
    commands = canvas.data.commands     #of commands
    n = random.randint(0,len(commands)-1)
    greenCommand(player,commands[n])
    
def greenSnow(player): #creates the snowball that green player has thrown
    canvas.data.greenSnow +=[-player]
    snowballSize = canvas.data.snowballSize
    playerRadius = canvas.data.playerRadius
    d = canvas.data.d #dictionary of snowballs
    throwStrength = -1#green player snowballs are thrown all the way off screen
    (x,y,hitCount,hitTime)=canvas.data.greenPlayersList[player]
    canvas.create_oval(x+playerRadius,y-playerRadius,\
                       x+playerRadius+snowballSize,\
                       y-playerRadius+snowballSize,fill="white")#draws snowball
    canvas.data.d[-player]= (x+playerRadius,y-playerRadius,\
                             x+playerRadius+snowballSize,\
                             y-playerRadius+snowballSize,throwStrength)
    canvas.data.snowballThrown = True    #stores the snowball
    
def greenCommand(player,command): #gives the given green player a command
    if command == "Throw": #green player throws snowball
        canvas.data.greenOrders[player]=1
        greenThrow = canvas.data.sound["greenThrow"]
        greenThrow.play() #play the green player throwing sound
    elif command == "Move": #green player is told to move
        directions = canvas.data.directions
        n = random.randint(0,len(directions)-1)
        direction = directions[n] #randomizes the direction
        steps = canvas.data.steps
        canvas.data.greenOrders[player]=(steps,direction) #player moves
                                                          #in random direction
    
def moveGreen(player): #moves green player in a given direction
    (steps,direction) = canvas.data.greenOrders[player]
    (x,y,hitCount,hitTime)=canvas.data.greenPlayersList[player]
    width,height = canvas.data.width,canvas.data.height
    playerRadius = canvas.data.playerRadius
    if steps ==0: canvas.data.greenOrders[player]=0
    else:
        if steps%(canvas.data.steps/2) == 0: 
            footstep = canvas.data.sound["footstep"]
            footstep.play() #the footstep sound is only played twice
        steps -=1       #otherwise the sound overlaps and doesn't sound good
        stepSize = 2 #player moves 2 pixels at a time     #player may not move
        if direction == "Left" and x-playerRadius>0: x -= stepSize #out of
        elif direction == "Up" and y-playerRadius>0: y -= stepSize #screen
        elif (x+playerRadius)+(y+playerRadius)!= canvas.data.width:
        #player may not cross into enemy territory
            if direction == "Right" and x<=canvas.data.width: x += stepSize
            if direction == "Down" and y<=canvas.data.height: y += stepSize
        canvas.data.greenOrders[player]=(steps,direction)
        canvas.data.greenPlayersList[player]=(x,y,hitCount,hitTime)

############
############Initialize
def initialGreenLevelOne(): #creates green initial green players for level one
    greenOneX = canvas.data.width/10
    greenOneY = canvas.data.height/10
    greenTwoX = greenOneX
    greenTwoY = greenOneY+(4*canvas.data.playerRadius)
    greenThreeX = greenOneX+(4*canvas.data.playerRadius)
    greenThreeY = greenOneX
    hitCount = 0
    hitTime = 0
    canvas.data.greenPlayersList +=[(greenOneX,greenOneY,hitCount,hitTime),\
                                    (greenTwoX,greenTwoY,hitCount,hitTime),\
                                    (greenThreeX,greenThreeY,hitCount,hitTime)]
    canvas.data.greenOrders = [0]*len(canvas.data.greenPlayersList)
    canvas.data.commands = ["Move","Throw"]
    canvas.data.directions = ["Left","Up","Right","Down"]
    for player in canvas.data.greenPlayersList:
        createGreenPlayers(player)

def createGreenPlayers(x,y,hitCount,hitTime): #creates green players
    gStand = canvas.data.image["gstand"]        #at given location
    gHit,gThrow = canvas.data.image["ghit"],canvas.data.image["gthrow"]
    gBrushOne = canvas.data.image["gbrushOne"]
    gBrushTwo = canvas.data.image["gbrushTwo"]
    maxHitCount = canvas.data.maxHitCount
    n = canvas.data.greenPlayersList.index((x,y,hitCount,hitTime))
    if hitCount ==maxHitCount: #player has been hit 3 times, player is dead
        dead = canvas.data.sound["dead"] #add player to dead list
        canvas.data.deadGreen += [(x,y)] #remove from alive list
        canvas.data.greenPlayersList.remove((x,y,hitCount,hitTime)),dead.play()
    elif hitTime>0: #player is hit
        if hitCount ==1: #first time being hit,player brushes snow off face
            if hitTime>50: canvas.create_image(x,y,anchor=N,image=gBrushOne)
            else: canvas.create_image(x,y,anchor=N,image=gBrushTwo)
        elif hitCount ==2: canvas.create_image(x,y,anchor=N,image=gHit)
    elif canvas.data.greenOrders[n]==-1: #player must wait until snowball lands 
        canvas.create_image(x,y,anchor=N,image=gThrow)
    else: canvas.create_image(x, y, anchor=N, image=gStand)
            
def initImages(): #stores the images in dictionary
    canvas.data.image = {}
    background = PhotoImage(file="snowcraft background.gif")
    rStand,gStand = PhotoImage(file="rstand.gif"),PhotoImage(file="gstand.gif")
    rDead,gThrow=PhotoImage(file="rdead.gif"),PhotoImage(file="gthrow.gif")
    rSelected = PhotoImage(file="rselected.gif")
    gDead,gHit = PhotoImage(file="gdead.gif"),PhotoImage(file="ghit.gif")
    rPlayerHit = PhotoImage(file="rplayerhit.gif")
    gBrushOne = PhotoImage(file="gBrushOne.gif")
    gBrushTwo = PhotoImage(file="gBrushTwo.gif")
    snowSplash = PhotoImage(file="snowsplash.gif")
    canvas.data.image["snowsplash"] = snowSplash
    canvas.data.image["background"] = background
    canvas.data.image["rstand"],canvas.data.image["gstand"]=rStand,gStand
    canvas.data.image["rdead"],canvas.data.image["rselected"]=rDead ,rSelected       
    canvas.data.image["gdead"],canvas.data.image["ghit"] = gDead,gHit
    canvas.data.image["gthrow"] = gThrow
    canvas.data.image["rplayerhit"]=rPlayerHit
    canvas.data.image["gbrushOne"]=gBrushOne
    canvas.data.image["gbrushTwo"]=gBrushTwo

def initSound(): #stores the sounds in dictionary
    mixer.init(44100) #initializes the mixer from pygame
    canvas.data.sound = {}
    dead = mixer.Sound("dead.wav")
    greenHit = mixer.Sound("greenHit.wav")
    greenThrow = mixer.Sound("greenThrow.wav")
    redHit = mixer.Sound("redHit.wav")
    redThrow = mixer.Sound("redThrow.wav")
    footstep = mixer.Sound("footstep.wav")
    newLevel = mixer.Sound("newLevel.wav")
    canvas.data.sound["footstep"] = footstep
    canvas.data.sound["dead"]= dead
    canvas.data.sound["greenHit"] = greenHit
    canvas.data.sound["greenThrow"] = greenThrow
    canvas.data.sound["redHit"] = redHit
    canvas.data.sound["redThrow"] = redThrow
    canvas.data.sound["newLevel"] = newLevel
    
def init(): #stores initial values
    initImages(),initSound()
    canvas.data.deadRed,canvas.data.deadGreen,canvas.data.snowSplashes=[],[],[]
    canvas.data.fallingSnowBall,canvas.data.snowBallSpeed = [],5
    canvas.data.boxHeight,canvas.data.boxWidth = 5,10
    canvas.data.playerSelected,width = [False,0,0],canvas.data.width
    canvas.data.hitTime, canvas.data.fallSpeed= 100,5
    canvas.data.redPlayersList,canvas.data.greenPlayersList = [],[]
    canvas.data.redSnow,canvas.data.greenSnow = [],[]
    canvas.data.throwStrength,canvas.data.d = 0,{}
    canvas.data.throwStrengthMaximum = (width)/canvas.data.snowBallSpeed
    canvas.data.shadowDistance,canvas.data.maxHitCount = 25,3
    canvas.data.mouse["leftPosn"],canvas.data.steps = (0,0),50
    canvas.data.snowBallCounter,canvas.data.playerRadius = 0,width/30
    canvas.data.paused,canvas.data.snowballThrown = False,False
    canvas.data.snowballSize = canvas.data.playerRadius/2
    if canvas.data.level == 1: initialRedPlayers(),initialGreenLevelOne()
    if canvas.data.level ==2:
        initialRedPlayers(),initialGreenLevelOne(),initialGreenLevelTwo()
    for element in canvas.data.redPlayersList: createRedPlayers(element)

def initialGreenLevelTwo(): #creates initial green players for level two
    greenFourX = (canvas.data.width/10)+(8*canvas.data.playerRadius)
    greenFourY = canvas.data.height/10
    greenFiveX = greenFourX-(4*canvas.data.playerRadius)
    greenFiveY = greenFourY+(4*canvas.data.playerRadius)
    greenSixX = greenFourX-(8*canvas.data.playerRadius)
    greenSixY = greenFourY+(8*canvas.data.playerRadius)
    hitCount = 0
    hitTime = 0
    canvas.data.greenPlayersList +=[(greenFourX,greenFourY,hitCount,hitTime),\
                                    (greenFiveX,greenFiveY,hitCount,hitTime),\
                                    (greenSixX,greenSixY,hitCount,hitTime)]
    canvas.data.greenOrders = [0]*len(canvas.data.greenPlayersList)
    for player in canvas.data.greenPlayersList:
        createGreenPlayers(player)
    
def initialRedPlayers(): #creates 3 red players at initial locations
    width = canvas.data.width
    height = canvas.data.height
    hitTime = 0
    playerRadius = canvas.data.playerRadius
    redOneX = ((width*3)/5)+playerRadius   
    redOneY = ((height/3)*2)+playerRadius
    redTwoX = redOneX+(playerRadius*3)
    redTwoY = redOneY
    redThreeX = redOneX+(playerRadius*3)
    redThreeY = redOneY-(playerRadius*3)
    canvas.data.redPlayersList += [(redOneX,redOneY,hitTime),\
                                   (redTwoX,redTwoY,hitTime),\
                                   (redThreeX,redThreeY,hitTime)]
    
def createRedPlayers(x,y,hitTime):  #creates red players at given location
    rStand = canvas.data.image["rstand"]
    rSelected = canvas.data.image["rselected"]
    rPlayerHit = canvas.data.image["rplayerhit"]
    dead = canvas.data.sound["dead"]
    playerRadius = canvas.data.playerRadius
    if hitTime> canvas.data.hitTime: #the player was hit while stunned
        dead.play()
        canvas.data.redPlayersList.remove((x,y,hitTime))  #player is dead
        canvas.data.deadRed += [(x,y)] #draw dead player on background
    elif hitTime>0: #the player was hit while not stunned
        canvas.create_image(x,y-playerRadius,anchor = N,image = rPlayerHit)
    elif canvas.data.playerSelected==[True,x,y]:#draw image for selected player
        canvas.create_image(x, y-playerRadius, anchor=N, image=rSelected)
    else: canvas.create_image(x, y-playerRadius, anchor=N, image=rStand)
    #otherwise, player is just standing
    
        
def gameStart(): #the loading page
    width = canvas.data.width
    height = canvas.data.height
    textSize = 50
    x = width/2
    y = height/3
    canvas.create_text(x,y,text = "Snow Craft", fill = "blue",\
                       font="Helvtica "+str(textSize)+" bold")
    canvas.create_text(x,y+textSize, text = "Press 'enter' to start",\
                       fill="blue",font = "Helvetica "+str(textSize/3)+" bold")
    canvas.create_text(x,y+textSize+(textSize/2), text = "Press 'h' for help",\
                       fill = "blue",font = "Helvetica "+\
                       str(textSize/3)+" bold")
############
############   
def run(): 
    global canvas # create the root and the canvas
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    width,height = 500,500
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width,canvas.data.height,canvas.data.mouse = width,height,{}
    canvas.data.level,canvas.data.loadTimer,canvas.data.instruction = 0,0,False
    init()
    # set up events
    root.bind("<Button-1>", leftMousePressed),root.bind("<Key>", keyPressed)
    canvas.bind("<B1-Motion>", leftMouseMoved)
    root.bind("<B1-ButtonRelease>", leftMouseReleased)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS
                     #(so your program waits until you close the window!)

run()

'''
Created on Feb 25, 2015

@author: Owner
'''
import  pygame, cPickle, thread, time,random, storymode,weapon
from socket import *
from character import *
from color import *

SIZE = (800,480)

TIMEREVENT = pygame.USEREVENT
FPS = 60
SERVERFPS = 120
ping = 100
local = True #Set to true if playing on same machine.
numVans = 6
maxhealth = 6
DEATHTIME = 3
kicktimeout = 2
chatMessageTime = 5
NO_CONNECT = 2
YES_CONNECT = 1
FLAG_CHARUPDATE = "CHAR_UPDATE"
FLAG_PROJUPDATE = "PROJ_UPDATE"
FLAG_OBJUPDATE = "OBJECTIVE_UPDATE"
FLAG_CHATUPDATE = "CHAT_UPDATE"
projectiles = []
vanspeed = 30
cutscenetime = 3
SCALE = 4
projectileIDs = range(256)
takenIDs = 1
maxIDs = 2**8


levelTheme = storymode.story[0]
viewedQuest = False
questQueue = []
chatQueue = []
soundQueue = []
sendMessages = []
skipCUpdate = False
skipPUpdate = False

skyRect = (0,0,800,120)
groundRect = (0,120,800,360)

clients = []
servers = []
possibleIP = gethostbyname(gethostname())
print possibleIP
possibleIP = possibleIP[:possibleIP.rfind(".")+1]
possibleIP += "%i"
print possibleIP
#possibleIP = "0.0.0.%i"
maxPlayers = 16

compName = gethostname()
serverName = "Test server #1"
clientName = "Brandon"
port = 8888

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SIZE)

    
pygame.font.init()
namefont = pygame.font.SysFont("MS Sans Serif",12)
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
pygame.display.set_caption("Unsuspicious Van Quest")
imageBank = [None for i in range(40)]
skyBGBank = [None for i in range(10)]
soundBank = [None for i in range(10)]
musicBank = [None for i in range(10)]
groundBGBank = [None for i in range(10)]
imageBank[0] = ratioScale(pygame.image.load("assets/manhole.png"),SCALE)
imageBank[1] = ratioScale(pygame.image.load("assets/firehydrant.png"),SCALE)
imageBank[2] = ratioScale(pygame.image.load("assets/cactus.png"),SCALE*2)
imageBank[3] = ratioScale(pygame.image.load("assets/shrub.png"),SCALE)
imageBank[4] = ratioScale(pygame.image.load("assets/shrub2.png"),SCALE)
imageBank[5] = ratioScale(pygame.image.load("assets/kitten.png"),SCALE)
imageBank[6] = ratioScale(pygame.image.load("assets/blood.png"),SCALE)
imageBank[7] = ratioScale(pygame.image.load("assets/bandit.png"),SCALE)
imageBank[8] = ratioScale(pygame.image.load("assets/kittenjihaad.png"),SCALE)
imageBank[9] = ratioScale(pygame.image.load("assets/debris.png"),SCALE)
imageBank[10] = ratioScale(pygame.image.load("assets/debris2.png"),SCALE)
imageBank[11] = ratioScale(pygame.image.load("assets/bullet.png"),SCALE*2)
imageBank[12] = ratioScale(pygame.image.load("assets/pistol.png"),SCALE)
imageBank[13] = ratioScale(pygame.image.load("assets/bullet2.png"),SCALE*2)
imageBank[14] = ratioScale(pygame.image.load("assets/horse.png"),SCALE)
imageBank[15] = ratioScale(pygame.image.load("assets/heart.png"),4)
imageBank[16] = ratioScale(pygame.image.load("assets/dumpster.png"),SCALE/2)
imageBank[17] = ratioScale(pygame.image.load("assets/explosion.png"),SCALE/2)
imageBank[18] = ratioScale(pygame.image.load("assets/crowgod.png"),SCALE*4)
imageBank[19] = ratioScale(pygame.image.load("assets/bullet3.png"),SCALE*4)
imageBank[20] = ratioScale(pygame.image.load("assets/bullet.png"),SCALE*4)
imageBank[21] = ratioScale(pygame.image.load("assets/boulder.png"),SCALE*2)
imageBank[22] = ratioScale(pygame.image.load("assets/boulder2.png"),SCALE*2)
imageBank[23] = ratioScale(pygame.image.load("assets/seagull.png"),SCALE*2)
imageBank[24] = ratioScale(pygame.image.load("assets/kingseagull.png"),SCALE*4)
imageBank[25] = ratioScale(pygame.image.load("assets/machineGun.png"),SCALE)
imageBank[26] = ratioScale(pygame.image.load("assets/relic.png"),SCALE*2)
imageBank[27] = ratioScale(pygame.image.load("assets/sword.png"),SCALE)
imageBank[28] = ratioScale(pygame.image.load("assets/swordslash.png"),SCALE*2)
imageBank[29] = ratioScale(pygame.image.load("assets/cube.png"),SCALE)
imageBank[30] = ratioScale(pygame.image.load("assets/crossbow.png"),SCALE)
imageBank[31] = ratioScale(pygame.image.load("assets/bolt.png"),SCALE)
imageBank[32] = ratioScale(pygame.image.load("assets/spider.png"),SCALE)
imageBank[33] = ratioScale(pygame.image.load("assets/spacekitten.png"),SCALE*2)
imageBank[34] = ratioScale(pygame.image.load("assets/pirate.png"),SCALE)
imageBank[35] = ratioScale(pygame.image.load("assets/americandream.png"),SCALE*4)
imageBank[36] = ratioScale(pygame.image.load("assets/kittenfire.png"),SCALE)
imageBank[37] = ratioScale(pygame.image.load("assets/dollar.png"),SCALE)
imageBank[38] = ratioScale(pygame.image.load("assets/spacedragon.png"),SCALE*4)
soundBank[0] = pygame.mixer.Sound("assets/sound/explosion.wav")
soundBank[1] = pygame.mixer.Sound("assets/sound/gunshot.wav")
soundBank[2] = pygame.mixer.Sound("assets/sound/itemget.wav")
soundBank[3] = pygame.mixer.Sound("assets/sound/hurt.wav")
#for i in range(len(imageBank)):
#    if imageBank[i]:
#        imageBank[i] = imageBank[i].convert()
skyBGBank[0] = pygame.image.load("assets/waitingRoom.png")
skyBGBank[1] = ratioScale(pygame.image.load("assets/citybg.png"),4)
skyBGBank[2] = ratioScale(pygame.image.load("assets/ruins2.png"),4)
skyBGBank[3] = ratioScale(pygame.image.load("assets/highseas2.png"),4)
skyBGBank[4] = ratioScale(pygame.image.load("assets/building2.png"),4)

groundBGBank[0] = ratioScale(pygame.image.load("assets/citybg2.png"),4)
groundBGBank[1] = ratioScale(pygame.image.load("assets/ruins.png"),4)
groundBGBank[2] = ratioScale(pygame.image.load("assets/highseas.png"),4)
groundBGBank[3] = ratioScale(pygame.image.load("assets/building.png"),4)
groundBGBank[4] = ratioScale(pygame.image.load("assets/earth.png"),4)
groundBGBank[5] = ratioScale(pygame.image.load("assets/skyfall.png"),4)
musicBank[0] = pygame.mixer.Sound("assets/sound/eraseform.wav")
musicBank[1] = pygame.mixer.Sound("assets/sound/beachwedding.wav")
musicBank[2] = pygame.mixer.Sound("assets/sound/outofcave.wav")
musicBank[3] = pygame.mixer.Sound("assets/sound/catnip.wav")
musicBank[4] = pygame.mixer.Sound("assets/sound/world10.wav")
musicBank[5] = pygame.mixer.Sound("assets/sound/rainbowride.wav")
musicBank[6] = pygame.mixer.Sound("assets/sound/twinkle.wav")
musicBank[7] = pygame.mixer.Sound("assets/sound/itsalongwaytothetop.wav")
musicBank[8] = pygame.mixer.Sound("assets/sound/selecta.wav")
musicBank[9] = pygame.mixer.Sound("assets/sound/raveonyou.wav")

musicPlayer = pygame.mixer.Channel(0)
currentlyPlaying = 8
musicPlayer.play(musicBank[currentlyPlaying], -1)

colourWheel = [RED,GREEN,YELLOW,PINK,GREY,BEIGE]
#Load all the different vans
vans = []
vanImage = ratioScale(pygame.image.load("assets/whitevan.png"),SCALE)
for i in range(numVans):
    vans.append(tint(vanImage,colourWheel[i],0.5))
    
#Load all the different drivers
drivers = []
for i in range(8):
    drivers.append(ratioScale(pygame.image.load("assets/driver%i.png"%(i+1)),SCALE))


def playSound(id):
    pygame.mixer.Sound.play(soundBank[id])


isServer = raw_input("Server(Y/N): ") == "Y"
if isServer:
    pygame.time.set_timer(TIMEREVENT, 1000 / SERVERFPS) #Starts timer for sync
else:
    pygame.time.set_timer(TIMEREVENT, 1000 / FPS) #Starts timer for sync
    
def addToQueue(m):
    if m == "":
        return None
    bigFont = pygame.font.Font("assets/f/strider.TTF",42)
    slate = pygame.Surface(SIZE)
    message = m.split(" ")
    lines = []
    word = 0
    ysize = bigFont.size("T")[1]
    width = SIZE[0]
    #split up the lines
    while word < len(message):
        line = ""
        while word < len(message):
            templine = line + message[word] + " "
            if bigFont.size(templine)[0] < width and line.find("@") == -1:
                line = templine
            else:
                break
            word += 1
        line = line.replace("@","")
        lines.append(line)

    #Draw each line
    for i in range(len(lines)):
        line = lines [i]
        lineImage = outlineText(line,bigFont,WHITE,BLACK,1)
        slate.blit(lineImage,[20, 20+ i*ysize*5/4])
    questQueue.append([slate.convert(),FPS*cutscenetime])    
    
def serverBackground(serverSocket):
    global sendMessages
    """
    @type serverSocket : socket
    @type checkSocket : socket
    """
    while True:
        try:
            checkSocket = serverSocket
            checkSocket.settimeout(60*5)
            client, address = checkSocket.accept()
            print "Pinged for information by", address
            serverInfo = {'name' : serverName, 'players':len(clients)}   
            try:
                client.send(cPickle.dumps(serverInfo))
                client.settimeout(2)
                message = client.recv(16)
                #print message
                if int(message) == YES_CONNECT:
                    newClient = cPickle.loads(client.recv(1024))
                    newClient['socket'] = client
                    newClient['ip'] = address
                    newClient['character'] = character(numVans)
                    newClient['weapon'] = weapon.weaponList[4]()
                    #newClient['character'].color = random.rangerange(numVans)
                    for c in clients:
                        if newClient['name'] == c['name']:
                            print " name is already taken"
                            continue
                    clients.append(newClient)
                    m =  "client", address,"connected"
                    print m
                    sendMessages.append("%s has joined the server."%(newClient['name']))
                else:# int(message) == NO_CONNECT:
                    print "client didn't connect", address
            except:
                print "Problem with sending server information"
        except:
            print "Server background socket timed out, restarting"
def full_recv(sock):
    total = []
    while True:
        data = sock.recv(1024)
        if not data: break
        total.append(data)
    return ''.join(total)
    
def clientBackground(clientSocket):
    global clients, projectiles,questQueue, levelTheme, ping,skipCUpdate, skipPUpdate, soundQueue,currentlyPlaying,newMusic
    """
    @type clientSocket : socket
    """
    received = False
    t = time.time()
    while 1:
        if True:
            for i in range(1):
                clientMult = int(math.log(len(clients)+ 2)/math.log(2))
                info = clientSocket.recv(4096*clientMult)
                #print info
                received = True
                if info.find(FLAG_CHARUPDATE) == 0:
                    skipCUpdate = True
                    raw = info [len(FLAG_CHARUPDATE):]
                    raw = raw [:raw.find(FLAG_CHARUPDATE)]
                    info = info[info.rfind(FLAG_CHARUPDATE) + len(FLAG_CHARUPDATE):]
                    replaceClient = None
                    cindex = -1
                    for c in clients:
                        if c['name'] == clientName:
                            replaceClient = c 
                            cindex = clients.index(c)
                            
                    processed = cPickle.loads(raw)
                    #Prediction here
                    
                    oldclients = clients [:]
                    clients = processed
                    if len(clients) == len(oldclients):
                        for i in range(len(clients)):
                            for j in range(2):
                                clients[i]['velocity'][j] = (clients[i]['position'][j] - oldclients[i]['position'][j])/4
                            clients[i]['position'] = oldclients[i]['position']
                    if cindex > -1:
                        clients[cindex]['position'] = replaceClient['position']
                        clients[cindex]['velocity'] = replaceClient['velocity']
                            
                    print "Received client information from server"
                    k = list(pygame.key.get_pressed())
                    print "Sending own information to server"
                    sendPackage = cPickle.dumps([k,replaceClient], protocol = 2)
                    clientSocket.send(sendPackage)
                    skipCUpdate = False
                if info.find(FLAG_PROJUPDATE) == 0:
                    skipPUpdate = True
                    raw = info [len(FLAG_PROJUPDATE):]
                    raw = raw [:raw.find(FLAG_PROJUPDATE)]
                    info = info[info.rfind(FLAG_PROJUPDATE) + len(FLAG_PROJUPDATE):]
                    processed = cPickle.loads(raw)
                    for p in projectiles[:]:
                        if p['retain']:
                            inprocessed = None
                            
                            for p2 in processed:
                                if p['id'] == p2['id']:
                                    inprocessed = p2
                                    break
                            if inprocessed:
                                for j in range(2):
                                    p2['velocity'][j] = (p2['position'][j] - p['position'][j])
                                p2['position'] = p['position']
                            try:
                                projectiles.remove(p)
                            except:
                                print "WHOOPS, THERE'S A DESYNC??"
                    projectiles += processed
                    print "Received projectile information from server"
                    skipPUpdate = False
                if info.find(FLAG_OBJUPDATE) == 0:
                    raw = info [len(FLAG_OBJUPDATE):]
                    raw = raw [:raw.find(FLAG_OBJUPDATE)]
                    info = info[info.rfind(FLAG_OBJUPDATE) + len(FLAG_OBJUPDATE):]
                    print raw
                    processed = cPickle.loads(raw)
                    print processed
                    bigFont = pygame.font.Font("assets/f/strider.TTF",42)
                    #print levelTheme, bigFont
                    newQueue = levelTheme['ending'].split("/n") + processed['message'].split("/n")
                    #print newQueue
                    questQueue = []
                    for m in newQueue:
                        addToQueue(m)
                    levelTheme = processed
                    newMusic = levelTheme['music']
                    if newMusic != currentlyPlaying:
                        currentlyPlaying = newMusic
                        musicPlayer.play(musicBank[newMusic], -1)
                    projectiles = []
                    print "Received new directive information from server"
                if info.find(FLAG_CHATUPDATE) == 0:
                    raw = info [len(FLAG_CHATUPDATE):]
                    raw = raw [:raw.find(FLAG_CHATUPDATE)]
                    info = info[info.rfind(FLAG_CHATUPDATE) + len(FLAG_CHATUPDATE):]
                    processed = cPickle.loads(raw)
                    #print processed
                    bigFont = pygame.font.Font("assets/f/strider.TTF",12)
                    for m in processed:
                        if m.find("@playsound") != -1:
                            m = m[len("@playsound"):]
                            soundID = int(m)
                            soundQueue.append(soundID)
                            #playSound(soundID)
                        else:
                            chatRender = outlineText(m,bigFont,WHITE,BLACK,1)
                            chatQueue.append([chatRender,chatMessageTime*FPS])
                        
                    print "Received message information from server"
        else:
            pass
        if received:
            ping = (time.time() - t)
            print "ping :%i ms"%(ping*1000)
            received = False
            t = time.time()

skyScroll = 0
groundScroll = 0
def drawScreen():
    global skipCUpdate, skipPUpdate,skyScroll, groundScroll
    if ping > 0 and ping < 150:
        frameDiff = ((1/ping)/FPS)#*0.986
    else:
        frameDiff = SERVERFPS/FPS/4
    frameDiff = 1/4.0
        
    if type(levelTheme['skyColor']) == int:
        if levelTheme['scrollSky']:
            skyScroll += int(levelTheme['slidespeed']*frameDiff/2)
            if skyScroll >= SIZE[0]:
                skyScroll = skyScroll - SIZE[0]
            screen.blit(skyBGBank[levelTheme['skyColor']],(SIZE[0] - skyScroll,0))
        else:
            skyScroll = 0
        screen.blit(skyBGBank[levelTheme['skyColor']],(-skyScroll,0))
    else:
        pygame.draw.rect(screen,levelTheme['skyColor'],skyRect,0)
        
    if type(levelTheme['groundColor']) == int:
        if levelTheme['scrollGround']:
            groundScroll += int(levelTheme['slidespeed']*frameDiff)
            if groundScroll >= SIZE[0]:
                groundScroll = groundScroll - SIZE[0]
            screen.blit(groundBGBank[levelTheme['groundColor']],(SIZE[0] - groundScroll,SIZE[1]/4))
        else:
            groundScroll = 0
        screen.blit(groundBGBank[levelTheme['groundColor']],(-groundScroll,SIZE[1]/4))
    else:
        pygame.draw.rect(screen,levelTheme['groundColor'],groundRect,0)
        
        
    for p in projectiles[:]:
        image = imageBank[p['image']]
        if p['hit']: image = tint(image,RED,0.5)
        screen.blit(image,(int(p['position'][0]),int(p['position'][1])))
        if skipPUpdate:
            #skipPUpdate = False
            #break
            pass
        else:
            for i in range(2):
                p['position'][i] += p['velocity'][i]*frameDiff
            if p['position'][0] < -imageBank[p['image']].get_width() or p['position'][0] > 2*SIZE[0]:
                if p in projectiles:
                    projectiles.remove(p)
    for c in clients[:]:
        if c['name'] == clientName:
            keys = pygame.key.get_pressed()
            if not c['death']:
                if keys[pygame.K_d]:
                    c['velocity'][0] = vanspeed
                elif keys[pygame.K_a]:
                    c['velocity'][0] = -vanspeed
                else:
                    c['velocity'][0] = 0
                if keys[pygame.K_w]:
                    c['velocity'][1]  = -vanspeed
                elif keys[pygame.K_s]:
                    c['velocity'][1] = vanspeed
                else:
                    c['velocity'][1] = 0
        if skipCUpdate:
            pass
        else:
            for i in range(2):
                c['position'][i] += c['velocity'][i]*frameDiff
            if c['position'][0] < 0:
                c['position'][0] = 0
            elif c['position'][0] > SIZE[0]-32*SCALE:
                c['position'][0] = SIZE[0]-32*SCALE
            if c['position'][1] < SIZE[1]/4:
                c['position'][1] = SIZE[1]/4
            elif c['position'][1] > SIZE[1]-16*SCALE:
                c['position'][1] = SIZE[1]-16*SCALE
        if not c['death']:
            image = vans[c['color']]
            if c['hit']: image = tint(image,RED,0.5)
            screen.blit(image,(int(c['position'][0]),int(c['position'][1])))
            screen.blit(drivers[c['driver']],(int(c['position'][0]+19*SCALE),int(c['position'][1]+5*SCALE)))
            nameRender = outlineText(c['name'],namefont,BLACK,WHITE, 1) 
            screen.blit(nameRender, c['position'])
def sendInfo(c, sock, superFinal):
    try:
        sock.settimeout(2)
        sock.send(superFinal)
        if finalPackage != "":
            #sock.send(finalPackage)
            rawClientInfo = sock.recv(1024)
            clientInfo = cPickle.loads(rawClientInfo)
            # print "received keys"
            keys = clientInfo[0]
            replaceClient = clientInfo[1]
            #print keys, replaceClient
            if replaceClient != None:
                existing = clients[clients.index(c)]
                existing['character'].position = replaceClient['position']
            if not c['character'].outtimer:
                if keys[pygame.K_d]:
                    c['character'].velocity[0] = vanspeed
                elif keys[pygame.K_a]:
                    c['character'].velocity[0] = -vanspeed
                else:
                    c['character'].velocity[0] = 0
                if keys[pygame.K_w]:
                    c['character'].velocity[1]  = -vanspeed
                elif keys[pygame.K_s]:
                    c['character'].velocity[1] = vanspeed
                else:
                    c['character'].velocity[1] = 0
                if keys[pygame.K_SPACE]:
                    if c['weapon'].reload <= 0:
                        sendMessages.append("@playsound1")
                        c['weapon'].fire(c,projectiles)
                        if c['weapon'].ammo <= 0:
                            c['weapon'] = weapon.weaponList[0]()
                c['weapon'].reloading()
                
            c['character'].kick  = 0
                                
    except:        
        #clients.remove(c)
        c['character'].kick += 1
        if c['character'].kick > kicktimeout*SERVERFPS/updateEvery:           
            sock.close()
            clients.remove(c)
            sendMessages.append("%s disconnected."%(c['name']))
        print "Connection error with " + c['name']
if isServer:
    bosses = []
    idleFrames = 0
    updateEvery = 8
    uCount = 0
    projTime = SERVERFPS*1
    randomDropTime = SERVERFPS*1
    specProjTime = SERVERFPS*1
    questTimer = SERVERFPS*levelTheme['length']
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    serverSocket.bind((compName,port))
    serverSocket.listen(maxPlayers)
    print "Server started on port %i"%(port)
    # Run a listening service in the background
    thread.start_new_thread(serverBackground, (serverSocket,))
    t1 = 0
    fpsFont = pygame.font.Font("assets/f/vanilla.TTF",32)
    while 1: 
        events = pygame.event.get()
        for ev in events:
            if ev.type == TIMEREVENT:
                uCount += 1
                if not time.time() - t1 == 0:
                        screen.fill(BLACK)
                        screen.blit(outlineText("fps %.2f"%(1/(time.time() - t1)),fpsFont, BLACK,WHITE,2),(0,0))
                        pygame.display.flip()
                t1 = time.time()
                if questTimer % SERVERFPS == 0:
                    print "%is left until next plotline"%(questTimer/SERVERFPS)
                if len(clients):
                    bossAlive = False
                    for b in bosses:
                        if b.health > 0:
                            bossAlive = True
                    if not bossAlive:
                        questTimer -= 1
                        print questTimer
                    for p in projectiles:
                        p.motion(clients,projectiles)
                        if p.touchable:
                            for c in clients:
                                if c['character'].outtimer > 0:
                                    continue
                                if collideimage(vanImage,c['character'].position,imageBank[p.image],p.position):
                                    if p in projectiles:
                                        if not p.pierce:
                                            projectiles.remove(p)
                                            p.onDeath(projectiles)
                                        if p.weapon != None:
                                            newWeapon =  weapon.weaponList[p.weapon]()
                                            if c['weapon'].image ==  newWeapon.image:
                                                newWeapon.ammo += c['weapon'].ammo
                                            c['weapon'] = newWeapon
                                            sendMessages.append("@playsound2")
                                        elif p.points > 0:
                                            print "gget cat"
                                            if p.points == 1337:
                                                c['character'].health += 1
                                                if c['character'].health > maxhealth:
                                                    c['character'].health = maxhealth
                                            else:
                                                c['character'].points += p.points
                                            sendMessages.append("@playsound2")
                                        elif c['character'].health > 0:
                                            c['character'].hit = True
                                            c['character'].health += p.points
                                            if c['character'].health <= 0:
                                                c['character'].health = 0
                                                c['character'].outtimer = SERVERFPS*DEATHTIME
                                                c['character'].points /= 2
                                                c['character'].deaths += 1
                                                newMessage = random.choice(p.deathMessages)
                                                newMessage = newMessage.replace("%s",c['name'])
                                                sendMessages.append(newMessage)
                                                sendMessages.append("@playsound0")
                                                for i in range(3):
                                                    newp = projectile()
                                                    newp.image = 17
                                                    newp.position = c['character'].position[:]
                                                    newp.position[0] += random.randrange(-5,5)*SCALE
                                                    newp.position[1] += random.randrange(-5,5)*SCALE
                                                    newp.velocity [0] = -levelTheme['slidespeed']
                                                    newp.bound = False
                                                    projectiles.append(newp)
                                            else:
                                                sendMessages.append("@playsound3")
                                            
                                                
                                        continue
                        if p.allied:
                            for p2 in projectiles:
                                if not (p2.allied or p2.bulletproof):
                                    if collideimage(imageBank[p.image],p.position,imageBank[p2.image],p2.position):
                                        if p in projectiles:
                                            if not p.pierce:
                                                projectiles.remove(p)
                                            p2.health -= p.damage
                                            p2.hit = True
                                            sendMessages.append("@playsound3")
                                            p.onDeath(projectiles)
                                        if p2 in projectiles:
                                            if p2.health < 1:
                                                projectiles.remove(p2)
                                                p2.onDeath(projectiles)
                                                chance = random.randrange(10)
                                                if chance == 0:
                                                    newp = randomDrop()
                                                    if newp.weapon != None:
                                                        newp.image = weapon.weaponList[newp.weapon]().image
                                                    newp.position = p2.position[:]
                                                    newp.velocity[0] = -levelTheme['slidespeed']
                                                    projectiles.append(newp)
                                                    
                                                
                        if p.health < 1:
                            if p in projectiles:
                                projectiles.remove(p)
                                p.onDeath(projectiles)
                            
                        for i in range(2):
                            p.position[i] += p.velocity[i]/updateEvery
                        if p.position[0] < -imageBank[p.image].get_width() or p.position[0] > 2*SIZE[0]:
                            if p in projectiles:
                                projectiles.remove(p)
                        if p.bound:
                            if p.position[1] < SIZE[1]/4:
                                p.position[1] = SIZE[1]/4
                            elif p.position[1] > SIZE[1]-imageBank[p.image].get_height():
                                p.position[1] = SIZE[1]-imageBank[p.image].get_height()
                    for c in clients:
                        for i in range(2):
                            c['character'].position[i] += c['character'].velocity[i]/updateEvery
                        if c['character'].outtimer > 0:
                            c['character'].outtimer -= 1
                            if c['character'].outtimer <= 0:
                                c['character'].health = maxhealth
                        if c['character'].position[0] < 0:
                            c['character'].position[0] = 0
                        elif c['character'].position[0] > SIZE[0]-32*SCALE:
                            c['character'].position[0] = SIZE[0]-32*SCALE
                        if c['character'].position[1] < SIZE[1]/4:
                            c['character'].position[1] = SIZE[1]/4
                        elif c['character'].position[1] > SIZE[1]-16*SCALE:
                            c['character'].position[1] = SIZE[1]-16*SCALE
                            
                    clientMult = int(math.log(len(clients) + 1)/math.log(2))
                    if not idleFrames > 0 and len(clients):
                        if projTime <= 0:
                            projTime = random.randrange(SERVERFPS/4,SERVERFPS/4*3)/clientMult
                            for j in range(len(levelTheme['foliageSprites'])):
                                projNum = random.randrange(4)
                                for i in range(projNum):
                                    newp = projectile()
                                    newp.image = levelTheme['foliageSprites'][j]
                                    newp.position[0] = SIZE[0] + random.randrange(SIZE[0]/2)
                                    newp.position[1] = random.randrange(SIZE[1]/4, SIZE[1])
                                    newp.velocity[0] = -levelTheme['slidespeed']
                                    projectiles.append(newp)
                                
                            for j in range(len(levelTheme['horizonSprites'])):
                                projNum2 = random.randrange(3)
                                for i in range(projNum2):
                                    newp = projectile()
                                    newp.image = levelTheme['horizonSprites'][j]
                                    newp.position[0] = SIZE[0]
                                    newp.position[1] = SIZE[1]/4 - imageBank[newp.image].get_height()
                                    newp.velocity[0] = -levelTheme['slidespeed']
                                    newp.bound = False
                                    projectiles.append(newp)
                        if specProjTime <= 0 and len(projectiles) < 16*clientMult:
                            specProjTime = random.randrange(SERVERFPS,SERVERFPS*2)/clientMult
                            for i in range(len(levelTheme['specialProj'])):
                                addBoss = False
                                if levelTheme['specialSpawn'][i] == -1:
                                    levelTheme['specialSpawn'][i] = 0
                                    projNum = 1
                                    addBoss = True
                                else:
                                    #projNum = random.randrange(levelTheme['specialSpawn'][i])
                                    projNum = levelTheme['specialSpawn'][i]
                                
                                for j in range(projNum):
                                    newp = specialList[levelTheme['specialProj'][i]]()
                                    newp.position[0] = SIZE[0] + random.randrange(SIZE[0]/2)
                                    newp.position[1] = random.randrange(SIZE[1]/4, SIZE[1])
                                    newp.velocity[0] = -levelTheme['slidespeed']
                                    projectiles.append(newp) 
                                    if addBoss: 
                                        newp.health *= clientMult
                                        bosses.append(newp)
                        if randomDropTime <= 0:
                            randomDropTime = random.randrange(SERVERFPS*5,SERVERFPS*10)/clientMult
                            newp = randomDrop()
                            if newp.weapon != None:
                                newp.image = weapon.weaponList[newp.weapon]().image
                            newp.position[0] = SIZE[0] + random.randrange(SIZE[0]/2)
                            newp.position[1] = random.randrange(SIZE[1]/4, SIZE[1])
                            newp.velocity[0] = -levelTheme['slidespeed']
                            projectiles.append(newp) 
                    projTime -= 1
                    specProjTime -= 1
                    randomDropTime -= 1
                    idleFrames -= 1
                if uCount >= updateEvery:
                    uCount = 0   
                    finalPackage = ""
                    finalPackage2 = ""
                    finalPackage3 = ""
                    finalPackage4 = ""
                    allDead = True
                    for c in clients:
                        if c['character'].outtimer <= 0:
                            allDead = False
                    if len(clients) > 1 and allDead:
                        questTimer = 0
                        levelTheme['paths'] = [0]
                        
                        for c in clients:
                            c['character'].outtimer = 0
                        #csort = sorted(clients, lambda x: x['character'].points,reverse = True)
                        #sendMessages.append("%s won with %i points"%(csort['name'],csort[0]['character'].points))
                    if questTimer <= 0:
                        #request vote
                        sendPackage = storymode.story[random.choice(levelTheme['paths'])].copy()
                        sendPackage ["message"] = sendPackage ["message"].replace("%s",random.choice(clients)['name'])
                        sendPackage ["ending"] = sendPackage ["ending"].replace("%s",random.choice(clients)['name'])
                        checkFrames = levelTheme['ending'].split("/n") + sendPackage['message'].split("/n")
                        while "" in checkFrames:
                            checkFrames.remove("")
                        specProjTime = 0
                        idleFrames = len(checkFrames)*SERVERFPS*cutscenetime
                        serialisedPackage =cPickle.dumps(sendPackage)
                        finalPackage3 = FLAG_OBJUPDATE + serialisedPackage + FLAG_OBJUPDATE
                        levelTheme = sendPackage
                        questTimer = levelTheme['length']*SERVERFPS
                        projectiles = []
                    if not idleFrames > 0:
                        #drawScreen()      
                        # Begin constructing a sendpackage
                        sendPackage = []
                        for c in clients:
                            sendClient = {}
                            sendClient['name'] = c['name']
                            sendClient['position'] = c['character'].position
                            sendClient['velocity'] = c['character'].velocity
                            sendClient['health'] = c['character'].health
                            sendClient['points'] = c['character'].points
                            sendClient['deaths'] = c['character'].deaths
                            sendClient['weapon'] = c['weapon'].image
                            sendClient['weaponammo'] = c['weapon'].ammo
                            sendClient['death'] = c['character'].outtimer
                            sendClient['hit'] = c['character'].hit
                            #sendClient['aimAngle'] = c['character'].aimAngle
                            #sendClient['faceRight'] = c['character'].faceRight
                            sendClient['color'] = c['character'].color
                            sendClient['driver'] = c['character'].driver
                            c['character'].hit = False
                            sendPackage.append(sendClient)
                        serialisedPackage =cPickle.dumps(sendPackage)
                        finalPackage = FLAG_CHARUPDATE + serialisedPackage + FLAG_CHARUPDATE
                        sendPackage = []
                        for p in projectiles:
                            if p.id == -1:
                                p.id = takenIDs
                                takenIDs += 1
                                print takenIDs
                                if takenIDs > maxIDs:
                                    takenIDs = 1
                                    
                            if p.new or p.retain:
                                p.new = False
                                sendProjectile = {}
                                sendProjectile['position'] = p.position
                                sendProjectile['velocity'] = p.velocity
                                sendProjectile['image'] = p.image
                                sendProjectile['retain'] = p.retain
                                sendProjectile['hit'] = p.hit
                                sendProjectile['id'] = p.id
                                p.hit = False
                                sendPackage.append(sendProjectile)
                        #print sendPackage
                        serialisedPackage =cPickle.dumps(sendPackage)
                        finalPackage2 = FLAG_PROJUPDATE + serialisedPackage  + FLAG_PROJUPDATE
                        sendPackage = []
                        if len(sendMessages) > 0:
                            sendPackage = sendMessages[:]
                            sendMessages = []
                            #print sendPackage
                            serialisedPackage =cPickle.dumps(sendPackage)
                            finalPackage4 = FLAG_CHATUPDATE + serialisedPackage  + FLAG_CHATUPDATE
                    #super wagon adventure, tank trouble, auralux, tilt to live
                    superFinal = finalPackage + finalPackage2 + finalPackage3 + finalPackage4
                    for c in clients:
                        """
                        @type c : socket
                        """
                        sock = c['socket']
                        if sock != serverSocket:
                            thread.start_new_thread(sendInfo, (c,sock, superFinal))
                #print projTime
                
else:
    pass
    
pygame.time.set_timer(TIMEREVENT, 1000 / FPS)

bigFont = buttonFont = pygame.font.Font('assets/f/dokoitsu.TTF',32)
semiFont = buttonFont = pygame.font.Font('assets/f/dokoitsu.TTF',24)
smallFont = buttonFont = pygame.font.Font('assets/f/dokoitsu.TTF',24)
firstRender = outlineText("1st place:",bigFont,WHITE,BLACK,1,False)
lookingForServer = True
serverBoxes = []
boxx = 400
boxy = 100
waitingRender = outlineText("Looking for servers...",bigFont,BLACK,WHITE,2)

tempName = ""
gotName = False
clientName = ""

while True:
    #receive information
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.KEYDOWN and not gotName:
            keys = pygame.key.get_pressed()
            k = ev.key
            if k == pygame.K_BACKSPACE:
                if len(tempName):
                    tempName = tempName[:len(tempName)-1]
                    continue
            elif k == pygame.K_RETURN:
                clientName = tempName
                continue
            elif k < 256:
                add = chr(k)
                if keys[pygame.K_LSHIFT]:
                    add = add.upper()
                tempName += add
        if ev.type == TIMEREVENT:
            if len(soundQueue) > 0:
                for i in soundQueue[:]:
                    soundQueue.remove(i)
                    playSound(i)
            if len(questQueue) > 0:
                questQueue[0][1] -= 1
                screen.fill(BLACK)
                screen.blit(questQueue[0][0],(0,0))
                if questQueue[0][1] <= 0:
                    del questQueue[0]
            elif  (len(clientName) < 6 or len(clientName) > 10):
                screen.fill(SKYBLUE)
                promptRender = outlineText("Please enter a name: ",bigFont,BLACK,WHITE,2)
                nameRender = outlineText(tempName,bigFont,BLACK,WHITE,2)
                screen.blit(promptRender,(0,0))
                screen.blit(nameRender,(promptRender.get_width(),0))
            elif lookingForServer:
                screen.fill(GREEN)
                if len(servers) < 1:
                    serverBoxes = []
                    servers = []
                    for i in range(24):       
                        checkIp = (possibleIP%(i))
                        if local:
                            checkIp = gethostname()
                        try:
                            clientSocket = socket(AF_INET, SOCK_STREAM)
                            clientSocket.settimeout(0.05)
                            clientSocket.connect((checkIp, port))
                            print "Server found on %s"%(checkIp)
                            serverInfo = cPickle.loads(clientSocket.recv(1024))
                            clientSocket.send(str(NO_CONNECT))
                            serverInfo ['ip'] = checkIp
                            print serverInfo
                            servers.append(serverInfo)
                            clientSocket.settimeout(2)
                            serverBoxes.append(pygame.Rect(SIZE[0]/2 - boxx/2, boxy*len(servers),boxx,boxy))
                        except:
                            print "Server not found on %s"%(checkIp)
                            pass
                        clientSocket.close()
                        if local and len(servers):
                            break
                    screen.blit(waitingRender,(SIZE[0]/2 - waitingRender.get_width()/2,SIZE[1]/2 - waitingRender.get_height()/2))
                else:
                    mouse = pygame.mouse.get_pos()
                    pickedIndex = -1
                    serverListRender = outlineText("SERVER LIST",bigFont,WHITE,BLACK,4,False)
                    screen.blit(serverListRender, (SIZE[0]/2 - serverListRender.get_width()/2,40))
                    for i in range(len(serverBoxes)):
                        outlinecol = GREEN
                        fillcol = GREY
                        serverNameRender = outlineText(servers[i]['name'],smallFont,WHITE,BLACK,1)
                        serverIpRender = outlineText("ip: " + servers[i]['ip'],smallFont,WHITE,BLACK,1)
                        serverPopRender = outlineText("players %i/%i"%(servers[i]['players'],maxPlayers),smallFont,WHITE,BLACK,1)
                        serverRect = serverBoxes[i]
                        mouseClick = pygame.mouse.get_pressed()[0]
                        if serverRect.collidepoint(mouse):
                            outlinecol = RED
                            if mouseClick:
                                pickedIndex = i
                                break
                        pygame.draw.rect(screen,fillcol,serverRect,0)
                        pygame.draw.rect(screen,outlinecol,serverRect,4)
                        screen.blit(serverNameRender,[serverRect[0]+10,serverRect[1]+10])
                        screen.blit(serverIpRender,[serverRect[0]+10,serverRect[1]+40])
                        screen.blit(serverPopRender,[serverRect[0]+10+200,serverRect[1]+70])
                    if pickedIndex != -1:
                        try:
                            clientSocket = socket(AF_INET, SOCK_STREAM)
                            #Join the selected server
                            print "Joining %s"%(servers[pickedIndex]['name'])
                            clientSocket.connect((servers[pickedIndex]['ip'], port))
                            print clientSocket.recv(1024)
                            clientSocket.send(str(YES_CONNECT)) #confirm connection
                            newClient = {'name' : clientName}
                            clientSocket.send(cPickle.dumps(newClient)) #send clientInfo
                            thread.start_new_thread(clientBackground, (clientSocket,)) #start background thread
                            lookingForServer = False
                        except:
                            print "Problem connecting to server"
                            servers = []
                            serverBoxes = []
                            
            
            
            else:
                drawScreen()
                keys = pygame.key.get_pressed()
                #draw gun
                weaponOrigin = [400,20]
                pygame.draw.rect(screen,WHITE,(weaponOrigin[0],weaponOrigin[1],16*SCALE,16*SCALE),0)
                pygame.draw.rect(screen,BLACK,(weaponOrigin[0],weaponOrigin[1],16*SCALE,16*SCALE),2)
                pygame.draw.rect(screen,WHITE,(weaponOrigin[0],weaponOrigin[1],16*SCALE,16*SCALE),1)
                for c in clients:
                    if c['name'] == clientName:
                        screen.blit(imageBank[c['weapon']], weaponOrigin)
                        ammoRender = outlineText(str(c['weaponammo']),semiFont,WHITE,BLACK,1,False)
                        screen.blit(ammoRender,(weaponOrigin[0],weaponOrigin[1]+16*SCALE))
                        heartOrigin = [weaponOrigin[0]+16*SCALE+16,0]
                        for i in range(c['health']):
                            hx = i*imageBank[15].get_width()+ heartOrigin[0]
                            hy = heartOrigin[1]
                            screen.blit(imageBank[15],[hx,hy])
                        break
                #draw chat
                chatOrigin = [0,10]
                if len(chatQueue) > 0:
                    for i in range(len(chatQueue)-1,-1,-1):
                        screen.blit(chatQueue[i][0],[chatOrigin[0],chatOrigin[1] + chatQueue[i][0].get_height()*i])
                        chatQueue[i][1] -= 1
                    for q in chatQueue:
                        if q[1] <= 0:
                            chatQueue.remove(q)
                            
                clientsorted = sorted(clients, key = lambda x: x['points'],reverse = True)
                if len(clientsorted) > 0 and False:
                    first = clientsorted[0]
                    nameRender = outlineText(first["name"],bigFont,WHITE,BLACK,1,False)
                    pointsRender = outlineText(str(first["points"])+"points",semiFont,WHITE,BLACK,1,False)
                    screen.blit(firstRender,(SIZE[0] - firstRender.get_width() - nameRender.get_width(),0))
                    screen.blit(nameRender,(SIZE[0] - nameRender.get_width(),10))
                    screen.blit(pointsRender,(SIZE[0] - 32*SCALE*2 - pointsRender.get_width(),firstRender.get_height()))
                    screen.blit(ratioScale(vans[first['color']],2),(SIZE[0] - 32*SCALE*2,firstRender.get_height()))
                    screen.blit(ratioScale(drivers[first['driver']],2),(SIZE[0] - 32*SCALE*2+19*SCALE*2,firstRender.get_height()+5*SCALE*2))
                #Draw scoreboard if tab held
                if keys [pygame.K_TAB]:
                    scoreBoard = pygame.Rect(0,40,600,400)
                    surf = pygame.Surface(scoreBoard.size)
                    surf.set_alpha(200)
                    pygame.draw.rect(surf,SKYBLUE,scoreBoard,0)
                    pygame.draw.rect(surf,WHITE,scoreBoard,5)
                    scoreBoardRender = outlineText("SCOREBOARD",bigFont,WHITE,BLACK,2,False)
                    surf.blit(scoreBoardRender, (scoreBoard.centerx - scoreBoardRender.get_width()/2,40))
                    for i in range(len(clientsorted)):
                        first = clientsorted[i]
                        nameRender = outlineText(first["name"],bigFont,WHITE,BLACK,1,False)
                        pointsRender = outlineText("Points "+str(first["points"]),semiFont,WHITE,BLACK,1,False)
                        deathsRender = outlineText("Deaths "+str(first["deaths"]),semiFont,WHITE,BLACK,1,False)
                        ypos = 100 + 40*i
                        xpos = 20
                        surf.blit(nameRender,(xpos+ 100,ypos))
                        surf.blit(pointsRender,(xpos + 200,ypos))
                        surf.blit(deathsRender,(xpos + 300,ypos))
                        surf.blit(ratioScale(vans[first['color']],1),(xpos + 0*32*SCALE,ypos))
                        surf.blit(ratioScale(drivers[first['driver']],1),(xpos + 0*32*SCALE+19*SCALE,ypos+5*SCALE))
                        
                        
                    
                    
                    scoreBoard.centerx = SIZE[0]/2
                    screen.blit(surf,scoreBoard)
                    
            pygame.display.flip()
            
            
                    

    
        
        
    
    
    


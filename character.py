'''
Created on Feb 25, 2015

@author: Owner
'''
import  pygame, cPickle, thread, time,random, math
SERVERFPS = 120

def makeBlood(p, projectiles, amount = 15,spread = 40):
        for i in range(15):
            x = random.randrange(-spread,spread)
            y = random.randrange(-spread,spread)
            newp = projectile()
            newp.image = 6
            newp.velocity = [-45,0]#[p.velocity[0],0]
            newp.position = [p.position[0] + x, p.position[1] + y]
            projectiles.append(newp)
class character:
    def __init__(self, colours):
        self.position = [0,0]
        self.velocity = [0,0]
        self.hit = False
        self.aimAngle = 0
        self.kick = 0
        self.faceRight = True
        self.health = 3
        self.points = 0
        self.deaths = 0
        self.color = random.randrange(colours)
        self.driver = random.randrange(8)
        self.outtimer = 0 
        self.kicktime = 0
        
class projectile(object):
    def __init__(self):
        self.position = [0,0]
        self.velocity = [0,0]
        self.image = 0
        self.points = 0
        self.hit = False
        self.new = True
        self.allied = False
        self.pierce = False
        self.id = -1
        self.damage = 0
        self.retain = False
        self.weapon = None
        self.bound = True
        self.bulletproof = True
        self.touchable = False
        self.health = 1
        self.deathMessages = ["%s died lol."]
    def motion(self,clients,projectiles):
        pass
    def onDeath(self,projectiles):
        pass

class randomDrop(projectile):
    def __init__(self):
        super(randomDrop,self).__init__()
        self.retain = True
        self.touchable = True
        weapon = random.choice([True,False])
        if weapon:
            self.weapon = random.randrange(1,5)
        else:
            self.points = 1337
            self.image = 26
class kitten(projectile):
    def __init__(self):
        super(kitten,self).__init__()
        self.points = 5
        self.image = 5
        self.bulletproof = False
        self.touchable = True
        self.retain = True
        self.timer = 3
        self.t = 0
        self.velocity[1] = random.randrange(-5,5)
    def motion(self,clients,projectiles):
        self.t += 1
        if self.t > self.timer:
            self.t = 0
    def onDeath(self,projectiles):
        for i in range(10):
            x = random.randrange(-20,20)
            y = random.randrange(-20,20)
            newp = projectile()
            newp.image = 6
            newp.velocity = [self.velocity[0],0]
            newp.position = [self.position[0] + x, self.position[1] + y]
            projectiles.append(newp)
class spaceKitten(projectile):
    def __init__(self):
        super(spaceKitten,self).__init__()
        self.points = -1
        self.image = 33
        self.bulletproof = False
        self.touchable = True
        self.retain = True
        self.timer = 3
        self.t = 0
        self.deathMessages = ["%s was hugged to death.","%s somehow died to a kitten.","%s was shown the errors of his ways."]
    def onDeath(self,projectiles):
        makeBlood(self,projectiles)
class kittenHostile(projectile):
    def __init__(self):
        super(kittenHostile,self).__init__()
        self.points = -1
        self.retain = True
        self.image = 8
        self.bulletproof = False
        self.touchable = True
        self.timer = 4
        self.t = 0
        #self.velocity[1] = random.randrange(-5,5)
        self.deathMessages = ["%s was hugged to death.","%s somehow died to a kitten.","%s was publicly humiliated."]
    def motion(self,clients,projectiles):
        self.t += 1
        if self.t > self.timer:
            self.t = 0
    def onDeath(self,projectiles):
        makeBlood(self,projectiles)
            

class bullet(projectile):
    def __init__(self):
        super(bullet,self).__init__()
        self.points = -1
        self.bound = False
        self.timer = 0
        self.retain = True
        self.image = 11
        self.touchable = True
        self.bulletproof = True
        self.bullets = [11,13]
        self.deathMessages = ["%s died as a bullet entered their brain.","% got shot in the vitals.","%s was filled with lead."]

    def motion(self,clients,projectiles):
        self.timer += 1
        if self.timer % 8 == 0:
            self.image = self.bullets[0]
        elif self.timer % 4 == 0:
            self.image = self.bullets[1]
        if self.position[1] > 600 or self.position[1] < -20:
            self.position[0] = -200
        
class bandit(projectile):
    def __init__(self):
        super(bandit,self).__init__()
        self.points = -5
        self.retain = True
        self.image = 7
        self.bulletproof = False
        self.touchable = False
        self.touchable = True
        self.pierce = True
        self.timer = SERVERFPS
        self.t = 0
        self.velocity[1] = random.randrange(-5,5)
    def motion(self,clients,projectiles):
        self.velocity[0] = -10
        if self.position[0] <= 700:
            self.position[0] = 700
            self.velocity[0] = 0
            self.velocity[1] = 0
        self.t += 1
        if self.t > self.timer:
            self.t = 0
            newp = bullet()
            newp.position = self.position[:]
            newp.velocity[0] = -40
            projectiles.append(newp)
    def onDeath(self,projectiles):
        makeBlood(self,projectiles)
        newp = projectile()
        newp.image = 14
        newp.position = self.position[:]
        newp.velocity[0] = -45
        newp.touchable = True
        newp.retain = True
        newp.points = 5
        projectiles.append(newp)
        
class pirate(projectile):
    def __init__(self):
        super(pirate,self).__init__()
        self.points = -5
        self.retain = True
        self.image = 34
        self.health = 3
        self.bulletproof = False
        self.touchable = False
        self.touchable = True
        self.pierce = True
        self.timer = SERVERFPS*2
        self.t = 0
        self.velocity[1] = random.randrange(-5,5)
    def motion(self,clients,projectiles):
        self.velocity[0] = -20
        self.t += 1
        if self.t > self.timer:
            self.t = 0
            newp = bullet()
            newp.position = self.position[:]
            newp.velocity[0] = -60
            projectiles.append(newp)
    def onDeath(self,projectiles):
        makeBlood(self,projectiles)
class slowBandit(bandit):
    def __init__(self):
        super(slowBandit,self).__init__()
    def motion(self,clients,projectiles):
        self.velocity[0] = -20
        self.t += 1
        if self.t > self.timer:
            self.t = 0
            newp = bullet()
            newp.position = self.position[:]
            newp.velocity[0] = -70
            projectiles.append(newp)
class crowGod(projectile):
    def __init__(self):
        super(crowGod,self).__init__()
        self.points = -5
        self.retain = True
        self.image = 18
        self.bound = False
        self.health = 20
        self.bulletproof = False
        self.touchable = False
        self.touchable = True
        self.pierce = True
        self.timer = SERVERFPS*2
        self.t = 0
        self.locked = False
        self.moving = False
        self.velocity[1] = 0
    def motion(self,clients,projectiles):
        if not self.locked:
            self.position[1] = 480/2 - 256/2
            self.velocity[1] = 0
            self.locked = True
        if self.health < 15:
            if not self.moving:
                self.moving = True
                self.velocity[1] = -15
            if self.position[1] <= -64:
                self.velocity[1] = 15
            elif self.position[1] >= 480 - 256 + 64:
                self.velocity[1] = -15
        self.velocity[0] = -10
        if self.position[0] <= 500:
            self.position[0] = 500
            self.velocity[0] = 0
            
        self.t += 1
        plist = []
        if self.t > self.timer:
            self.t = 0
            for s in [45,60]:
                for i in range(120,260,20):
                    angle = math.radians(i)
                    newp = bullet()
                    newp.deathMessages = ["%s was burned alive.","%s was incinerated.","%s was consecrated."]
                    newp.position = self.position[:]
                    newp.bullets = [13,19]
                    newp.position[1] += 128
                    newp.velocity[0] = math.cos(angle)*s
                    newp.velocity[1] = math.sin(angle)*s
                    plist.append(newp)
        projectiles += plist
    def onDeath(self,projectiles):
        makeBlood(self,projectiles,30,100)
        newp = projectile()
        newp.image = 18
        newp.position = self.position[:]
        newp.velocity[0] = -45
        newp.touchable = True
        newp.retain = True
        newp.points = 50
        projectiles.append(newp)
        
class boulder(projectile):
    def __init__(self):
        super(boulder,self).__init__()
        self.points = -1
        self.bound = False
        self.timer = 0
        self.retain = True
        self.image = 21
        self.touchable = True
        self.bulletproof = True
        self.start = False
        self.bullets = [21,22]
        self.deathMessages = ["%s slowly bled to death after being crushed.","%s was buried alive.","%s's skull was crushed."]

    def motion(self,clients,projectiles):
        if not self.start:
            self.start = True
            self.position[0] = 1400 + random.randrange(800)
            self.position[1] = -100 -random.randrange(100)
            self.velocity[1] = 30
        self.timer += 1
        if self.timer % 4 == 0:
            self.image = self.bullets[0]
        elif self.timer % 2 == 0:
            self.image = self.bullets[1]
        if self.position[1] > 600:
            self.position[0] = -200
            
class seagull(projectile):
    def __init__(self):
        super(seagull,self).__init__()
        self.points = -1
        self.retain = True
        self.image = 23
        self.bulletproof = False
        self.touchable = True
        self.velocity[1] = 0
        self.deathMessages = ["%s's eyes were pecked out.","A seagull pierced %s's skull.","%s became a seagull's home."]
    def onDeath(self,projectiles):
        makeBlood(self,projectiles)
class spider(projectile):
    def __init__(self):
        super(spider,self).__init__()
        self.points = -1
        self.retain = True
        self.image = 32
        self.bulletproof = False
        self.touchable = True
        self.velocity[1] = 0
        self.locked = False
        self.deathMessages = ["A spider injected venom in %s.","%s's limbs were torn apart by a spider.","A spider layed its eggs into %s."]
    def motion(self,clients,projectiles):
        if not self.locked:
            self.velocity[0] = 30
            self.position[0] = -64 + 1
            self.velocity[1] = 0
            self.locked = True
        if self.position[0] > 800:
            self.position[0] =   -200
    def onDeath(self,projectiles):
        makeBlood(self,projectiles,30,100)
        newp = projectile()
        newp.image = self.image
        newp.position = self.position[:]
        newp.velocity[0] = -45
        newp.touchable = True
        newp.retain = True
        newp.points = 5
        projectiles.append(newp)
        makeBlood(self,projectiles)
        
class kingSeagull(projectile):
    def __init__(self):
        super(kingSeagull,self).__init__()
        self.points = -5
        self.retain = True
        self.image = 24
        self.bound = False
        self.health = 30
        self.touchable = True
        self.pierce = True
        self.bulletproof = False
        self.touchable = False
        self.timer = SERVERFPS/3
        self.t = 0
        self.locked = False
        self.moving = False
        self.velocity[1] = 0
    def motion(self,clients,projectiles):
        if not self.locked:
            self.position[1] = 480/2 - 64/2
            self.velocity[1] = 0
            self.locked = True
        if self.health < 15:
            if not self.moving:
                self.moving = True
                self.velocity[1] = -10
            if self.position[1] <= -16:
                self.velocity[1] = 10
            elif self.position[1] >= 480 - 64 + 16:
                self.velocity[1] = -10
        self.velocity[0] = -10
        if self.position[0] <= 550:
            self.position[0] = 550
            self.velocity[0] = 0
            
        self.t += 1
        if self.t > self.timer:
            self.t = 0
            for s in [45,60]:
                for i in range(-60,120,60):
                    newp = bullet()
                    newp.deathMessages = ["%s's eyes were pecked out.","A seagull pierced %s's skull.","%s became a seagull's home."]
                    newp.position = self.position[:]
                    newp.bullets = [23,23]
                    newp.image = 23
                    newp.position[1] += 32 + -i
                    newp.velocity[0] = -s
                    projectiles.append(newp)
    def onDeath(self,projectiles):
        makeBlood(self,projectiles,30,100)
        newp = projectile()
        newp.image = self.image
        newp.position = self.position[:]
        newp.velocity[0] = -45
        newp.touchable = True
        newp.retain = True
        newp.points = 50
        projectiles.append(newp)
        
class americanDream(projectile):
    def __init__(self):
        super(americanDream,self).__init__()
        self.points = -5
        self.retain = True
        self.image = 35
        self.touchable = True
        self.pierce = True
        self.bound = False
        self.health = 40
        self.bulletproof = False
        self.touchable = False
        self.timer = SERVERFPS*3/4
        self.t = 0
        self.locked = False
        self.moving = False
        self.velocity[1] = 0
    def motion(self,clients,projectiles):
        if not self.locked:
            self.position[1] = 480/2 - 256/2
            self.velocity[1] = 0
            self.locked = True
        if self.health < 15:
            if not self.moving:
                self.moving = True
                self.velocity[1] = -15
            if self.position[1] <= -64:
                self.velocity[1] = 15
            elif self.position[1] >= 480 - 256 + 64:
                self.velocity[1] = -15
        self.velocity[0] = -10
        if self.position[0] <= 550:
            self.position[0] = 550
            self.velocity[0] = 0
            
        self.t += 1
        if self.t > self.timer:
            self.t = 0
            for s in [30,45]:
                for i in range(120,260,40):
                    angle = math.radians(i)
                    newp = bullet()
                    newp.deathMessages = ["%s became capital.","%s is a part of the american dream."]
                    newp.position = self.position[:]
                    newp.bullets = [37,37]
                    newp.position[1] += 128
                    newp.velocity[0] = math.cos(angle)*s
                    newp.velocity[1] = math.sin(angle)*s
                    projectiles.append(newp)
    def onDeath(self,projectiles):
        makeBlood(self,projectiles,30,100)
        newp = projectile()
        newp.image = self.image
        newp.position = self.position[:]
        newp.velocity[0] = -45
        newp.touchable = True
        newp.retain = True
        newp.points = 50
        projectiles.append(newp)


class kittenfire(projectile):
    def __init__(self):
        super(kittenfire,self).__init__()
        self.points = -1
        self.retain = True
        self.image = 36
        self.bulletproof = False
        self.touchable = True
        self.velocity[1] = 0
        self.locked = False
        self.deathMessages = ["%s was smashed to pieces.","%s collided with a kitten.","%s face was melted."]
    def motion(self,clients,projectiles):
        if not self.locked:
            self.velocity[0] = 60
            self.position[0] = -64 + 1
            self.velocity[1] = 0
            self.locked = True
        if self.position[0] > 800:
            self.position[0] =   -200
    def onDeath(self,projectiles):
        makeBlood(self,projectiles,30,100)
        newp = projectile()
        newp.image = self.image
        newp.position = self.position[:]
        newp.velocity[0] = -45
        newp.touchable = True
        newp.retain = True
        newp.points = 5
        projectiles.append(newp)
        makeBlood(self,projectiles)
        
class spaceDragon(projectile):
    def __init__(self):
        super(spaceDragon,self).__init__()
        self.points = -5
        self.retain = True
        self.image = 38
        self.bound = False
        self.health = 20
        self.bulletproof = False
        self.touchable = False
        self.timer = 20
        self.t = 0
        self.locked = False
        self.moving = False
        self.velocity[1] = 0
    def motion(self,clients,projectiles):
        if not self.locked:
            self.position[1] = 480/2 - 256/2
            self.velocity[1] = 0
            self.locked = True
        if self.health < 15:
            if not self.moving:
                self.moving = True
                self.velocity[1] = -15
            if self.position[1] <= -64:
                self.velocity[1] = 15
            elif self.position[1] >= 480 - 256 + 64:
                self.velocity[1] = -15
        self.velocity[0] = -10
        if self.position[0] <= 500:
            self.position[0] = 500
            self.velocity[0] = 0
            
    def onDeath(self,projectiles):
        makeBlood(self,projectiles,30,100)
        newp = projectile()
        newp.image = self.image
        newp.position = self.position[:]
        newp.velocity[0] = -45
        newp.touchable = True
        newp.retain = True
        newp.points = 50
        projectiles.append(newp)
        
specialList = [kitten,kittenHostile,bandit,slowBandit, crowGod,boulder,seagull,kingSeagull,spider,spaceKitten,pirate, americanDream, kittenfire,spaceDragon]


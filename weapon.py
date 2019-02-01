'''
Created on Feb 25, 2015

@author: Owner
'''
import  pygame, cPickle, thread, time, random, character
from color import *

class weapon(object):
    def __init__(self):
        self.ammo = 6
        self.reloadTime = 0
        self.reload = 0
        self.image = 0
        self.id = 0
        self.bound = True 
    def fire(self,client,projectiles):
        pass
    def reloading(self):
        self.reload -= 1


class allyBullet(character.projectile):
    def __init__(self):
        super(allyBullet,self).__init__()
        self.points = -1
        self.retain = True
        self.allied = True
        self.timer = 0
        self.image = 11
        self.damage = 1
        self.bullets = [13,11]
    def motion(self,clients,projectiles):
        self.timer += 1
        if self.timer % 8 == 0:
            self.image = self.bullets[0]
        elif self.timer % 4 == 0:
            self.image = self.bullets[1]
        

class noobGunPistol(weapon):
    def __init__(self):
        super(noobGunPistol,self).__init__()
        self.ammo = 999
        self.reloadTime = 4
        self.image = 12
        self.id = 0
    def fire(self,client,projectiles):
        print "Gunfire"
        if self.reload < 1:
            newp = allyBullet()
            newp.position = client['character'].position[:]
            newp.velocity[0] = 60
            projectiles.append(newp)
            self.reload = self.reloadTime
            if self.ammo < 999:
                self.ammo -= 1
            print "fired"
class machineGun(noobGunPistol):
    def __init__(self):
        super(machineGun,self).__init__()
        self.ammo = 30
        self.reloadTime = 1
        self.image = 25
        
        
class allySlash(character.projectile):
    def __init__(self):
        super(allySlash,self).__init__()
        self.points = -1
        self.retain = True
        self.allied = True
        self.timer = 120/4
        self.pierce = True
        self.image = 28
        self.damage = 2
    def motion(self,clients,projectiles):
        self.timer += 1
        if self.timer % 30 == 0:
            self.position[0] = -400
            
class eastern(weapon):  
    def __init__(self):
        super(eastern,self).__init__()  
        self.ammo = 10
        self.image = 27
        self.reloadTime = 3
    def fire(self,client,projectiles):
        print "Gunfire"
        if self.reload < 1:
            newp = allySlash()
            newp.position = client['character'].position[:]
            newp.position[0] += 40
            newp.velocity[0] = 40
            projectiles.append(newp)
            self.reload = self.reloadTime
            if self.ammo < 999:
                self.ammo -= 1
            print "fired"    
class flux(weapon):  
    def __init__(self):
        super(flux,self).__init__()  
        self.ammo = 5  
        self.image = 29
        self.reloadTime = 3
    def fire(self,client,projectiles):
        print "Gunfire"
        if self.reload < 1:
            client['character'].position[0] += 100
            client['character'].health += 1
            self.reload = self.reloadTime
            if self.ammo < 999:
                self.ammo -= 1
            print "fired"   
             
class crossBow(noobGunPistol):
    def __init__(self):
        super(crossBow,self).__init__()
        self.ammo = 10
        self.reloadTime = 5
        self.image = 30
    def fire(self,client,projectiles):
        print "Gunfire"
        if self.reload < 1:
            newp = allyBullet()
            newp.position = client['character'].position[:]
            newp.velocity[0] = 50
            newp.pierce = True
            newp.image = 31
            newp.bullets = [31,31]
            projectiles.append(newp)
            self.reload = self.reloadTime
            if self.ammo < 999:
                self.ammo -= 1
            print "fired"
weaponList = [noobGunPistol,machineGun,eastern,flux,crossBow]
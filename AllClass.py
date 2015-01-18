#Classes and Attributes
import pygame
import sys
from pygame import *

#[Level,             health, numberofenemies, speed,picture,money ]
Waves=[
["Level 1: Piece of Cake",500,13,1,"data/Waves/wave1.png",3],
["Level 2: Piece of Pie",600,14,2,"data/Waves/wave2.png",5],
["Level 3: Piece of Cheese",700,6,5,"data/Waves/wave3.png",5],
["Level 4: Read Monsters",500,20,2,"data/Waves/wave4.png",6],
["Level 5: Cash Injection",700,25,2,"data/Waves/wave5.png",7],
["Level 6: More money",800,25,4,"data/Waves/wave6.png",8],
["Level 7: Use the Freeze",2000,1,10,"data/Waves/wave7.png",1500],
#["Level 8: Almost Boss",1500,8,3,"data/wave8.png",10],
#["Level 9: First Boss",5000,1,3,"data/wave9.png",10],
]





#[Name,Range, Attack, BulletType,life,shot speed, bullet speed,    cost]
# 0     1      2       3           4     5         6
TowersTypes=[["Basic Tower",80,40,"data/heromissile.png",5,15,10,20],
["Turret",90,70,"data/heromissile.png",5,15,10,30],
["Laser",100,90,"data/heromissile.png",5,12,10,70],
["Grenade Launcher",110,100,"data/heromissile.png",5,12,10,100],
["It's High Tech",120,120,"data/heromissile.png",5,12,10,150],
["Plasma Cannon",220,250,"data/heromissile.png",5,12,10,250]

]


#pretty self explanatory attributes for each type of object on the scren, used pngs so have to set transparency with  
#self.image.set_colorkey((0,0,0))
#self.image=self.image.convert_alpha()

class Basic_Image(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, filename):
        pygame.sprite.Sprite.__init__(self)
	self.image=pygame.image.load(filename)
	self.image.set_colorkey((0,0,0))
	self.image=self.image.convert_alpha()
	
	self.rect=self.image.get_rect()
	self.x=self.rect.x=xpos
	self.y=self.rect.y=ypos
	self.original=self.image
	
	self.startpointx=xpos
	self.startpointy=ypos
	self.endpointx=xpos
	self.endpointy=ypos
	
	self.active=False	

class BlackImage(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, filename):
	pygame.sprite.Sprite.__init__(self)
	self.image=pygame.image.load(filename)
	self.rect=self.image.get_rect()
	self.x=self.rect.x=xpos
	self.y=self.rect.y=ypos

class CharacterGuy(Basic_Image):
    def __init__(self, xpos, ypos, filename):
	Basic_Image.__init__(self,xpos,ypos,filename)	
	self.image.set_colorkey((255,255,255))
	self.image=self.image.convert_alpha()
	self.active=True
	self.speed=5
	self.firingdelay=5
	self.cfire=50
	self.fire=False
	self.hitx=0
	self.hity=0
	self.bulletspeed=10
	self.attack=100
	
	self.attackcost=10
	
	self.lives=10
	self.originallives=self.lives
	
	self.money=400
	

class Tower(Basic_Image):
    def __init__(self, towertype,filename):
	Basic_Image.__init__(self,0,0,filename)

	
	
	self.life=TowersTypes[towertype][4]
	self.attack=TowersTypes[towertype][2]
	self.alive=False
	self.rangeatt=TowersTypes[towertype][1]
	self.isattack=False
	self.shottime=TowersTypes[towertype][5]
	self.delayshot=TowersTypes[towertype][5]-1
	self.towerspeed=TowersTypes[towertype][6]
	
	self.cost=TowersTypes[towertype][7]
	
class Bullet(Basic_Image):
    def __init__(self, towertype,filename):
	Basic_Image.__init__(self,0,0,filename)
	self.attack=0
	self.speed=0

class LvlBuggies(Basic_Image):
    def __init__(self, wave):
	Basic_Image.__init__(self,0,0,Waves[wave-1][4])
	self.image=pygame.image.load(Waves[wave-1][4])
	self.image.set_colorkey((0,0,0))
	self.image=self.image.convert_alpha()	

	
	self.alive=False
	self.moving=False
	self.totalhealth=Waves[wave-1][1]
	self.health=self.totalhealth
	self.attackers=Waves[wave-1][2]
	self.speed=Waves[wave-1][3]
	self.currentwaypoint=-1
	self.firstactive=False	
	
	self.value=Waves[wave-1][5]
	

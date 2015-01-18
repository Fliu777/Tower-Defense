import pygame
import sys
from pygame import *
import math
import random
import AllClass as CLASS
import os.path
from pygame.color import THECOLORS

## If you get the no available video device error, copy and paste the below code ##
import platform, os
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'
### If you get the no available video device error, copy and paste the above code ###



def Main(difficulty,maptype):    
    pygame.init()
    HEIGHT=512+234
    WIDTH=768
    screen = pygame.display.set_mode((WIDTH,HEIGHT))#,FULLSCREEN)
    pygame.display.set_caption('Tower Defence')
    myfont=pygame.font.SysFont("Vera", 30)
    clock=pygame.time.Clock()    
        
    def render(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def rotate(self,angle):
        self.image=pygame.transform.rotate(self.original, angle)
        self.rect==pygame.transform.rotate(self.original, angle)
        
    def objectmovement(currx,curry,lastx,lasty,rate):
        #stats[0]=done? True is finished, False is still going
        #stats[1]= angle
        #stats[2]= (newx,newy)
    
        stats=[]
        angle1=math.atan2(currx-lastx, curry-lasty)
        
        distleft=((currx-lastx)**2+(curry-lasty)**2)**0.5
        #distleft=0
        if distleft<=rate:
            stats.append(True)
            stats.append(angle1)
            stats.append((lastx,lasty))
        else:
            stats.append(False)
            stats.append(angle1)
            stats.append((currx-rate*math.sin(angle1),curry-rate*math.cos(angle1)))
        return stats
        
    def bulletmovement(currx,curry,lastx,lasty):
        xincrement=(lastx-currx)
        yincrement=(lasty-curry)
        result=[]
        while True:
            lastx+=xincrement
            lasty+=yincrement
            if lasty<0:
                result.append(int(lastx))
                result.append(int(lasty))
                return result
            elif lasty>=HEIGHT-234:
                result.append(int(lastx))
                result.append(int(lasty))
                return result
            if lastx<0:
                result.append(int(lastx))
                result.append(int(lasty))
                return result
            elif lastx>=WIDTH:
                result.append(int(lastx))
                result.append(int(lasty))
                return result
    
    def isbuttonclicked(clickx,clicky):
        if clickx>579 and clickx<622 and clicky>640 and clicky<667:
            return "Start"
        elif clickx>669 and clickx<742 and clicky>640 and clicky<667:
            return "Pause"
        elif clickx>579 and clickx<622 and clicky>676 and clicky<700:
            return "Menu"
        elif clickx>669 and clickx<742 and clicky>676 and clicky<700:
            return "Exit"
        return False
    
    
    def towerchoice(clickx,clicky):
        if clickx>33 and clickx<88 and clicky>559 and clicky<614:
            return 0
        if clickx> 109 and clickx<164 and clicky>559 and clicky<614:
            return 1  
        if clickx>189 and clickx<245 and clicky>559 and clicky<614:
            return 2   
        if clickx>33 and clickx<88 and clicky>632 and clicky<685:
            return 3
        if clickx> 109 and clickx<164 and clicky>632 and clicky<685:
            return 4  
        if clickx>189 and clickx<245 and clicky>632 and clicky<685:
            return 5      
 
        return -1
  
    Buggies=pygame.sprite.Group()
    Towers=[]
    waypoints=[]
    Bullets=pygame.sprite.Group()   
    Mines=pygame.sprite.Group() 
    
    Towertypenum=6
    Displaytower=[]
    for x in range(Towertypenum):
        Displaytower.append(CLASS.Tower(x,'data/Towers/tower'+str(x)+'.png'))


    #nNew map
    if os.path.isfile("Maps/Map"+str(maptype)+".txt")==True:
        mapfile=open("Maps/Map"+str(maptype)+".txt","r")
        tempmap="".join(mapfile.readlines())
        mapfile.close()
        mapthing=[]
        #Standard size of map (number of tiles down and across)       
        
        for x in range(1,9):
            mapthing.append(tempmap[(x-1)*12:x*12])
        for x in range(len(mapthing)):
            mapthing[x]=list(mapthing[x])
                
                
        if os.path.isfile("Maps/Path"+str(maptype)+".txt")==True:
            pathfile=open("Maps/Path"+str(maptype)+".txt","r")
            temppath="".join(pathfile.readlines()).splitlines()
            pathfile.close()
            for x in range(len(temppath)):
                firstpoint=temppath[x][temppath[x].find("(")+1:temppath[x].find(",")]
                secondpoint=temppath[x][temppath[x].find(",")+1:temppath[x].find(")")]
                waypoints.append((int(firstpoint),int(secondpoint)))

    for x in range(100):
        Bullets.add(CLASS.Bullet(1, 'data/heromissile.png'))
        

    bug=CLASS.LvlBuggies(1)
    
    Hero=CLASS.CharacterGuy(0,0,'data/player.png')
    
    heromode=True
    towermode=False
    towerstats=""
    
    
    backdrop=pygame.image.load('BACKGROUNDTEMP.png')
    # Loop and draw the background
    running=True
    
    clocationx=clocationy=0
    blockx=blocky=0
    openspot=False
    framerate=49
    key.set_repeat(1, 1)
    
    ctower=0
    settower=False
    
    
    
    Wavelevel=0
    NextWave=True
    Pause=False
    
    thistower=0
    
    for x in range(CLASS.LvlBuggies(Wavelevel).attackers):
        Buggies.add(CLASS.LvlBuggies(Wavelevel))
    
    bottom=CLASS.BlackImage(0,HEIGHT-234,'data/sidesc.png')
    
    while running:
        menubutton=""
        
        screen.blit(backdrop, (0, 0))
        render(bottom)
        counter=0
        Hero.cfire=Hero.cfire+1
        goright=goleft=godown=goup=False
        
        for event in pygame.event.get():
            counter+=1
            if event.type == pygame.QUIT:
                running==False
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_d:
                    goright=True
                elif event.key==K_a :
                    goleft=True
                elif event.key==K_s:
                    godown=True
                elif event.key==K_w:
                    goup=True
                if event.key==K_ESCAPE:
                    heromode=True
                    towermode=False
        
            if event.type==KEYUP:
                if event.key==K_n:
                    NextWave=True           
                    
                        
            if event.type==MOUSEBUTTONDOWN:
                #unpauses
                Pause=False
                locationx,locationy=event.pos
                print event.pos
                temptower=towerchoice(locationx,locationy)
                
                filething="data/Towers/tower"+str(ctower)+".png"                        
                thistower=CLASS.Tower(ctower,filething)
                if temptower!=-1:
                    heromode=False
                    towermode=True
                    ctower=temptower
                
                if towermode==True:
                    if locationy<512 and locationx<WIDTH:
                        
                        if Hero.money>=thistower.cost:
                            if mapthing[locationy/64][locationx/64]=="#":
                                mapthing[locationy/64][locationx/64]="1"  
                                
                                Towers.append(thistower)
                                Hero.money-=thistower.cost
                                Towers[-1].rect.x=locationx/64*64
                                Towers[-1].rect.y=locationy/64*64
                                towermode=False
                                heromode=True
                            else:
                                print "OCCUPIED"
                        else:
                            print "rejected"
                            towermode=False
                            heromode=True
                    else:
                        menubutton=isbuttonclicked(locationx,locationy)

                    
                else:
                    if locationy<512 and locationx<WIDTH:
                        Hero.fire=True
                        Hero.hitx=locationx
                        Hero.hity=locationy
                    else:
                        menubutton=isbuttonclicked(locationx,locationy)                    
                    
                
            if event.type==MOUSEMOTION:
                clocationx,clocationy=event.pos
                if heromode==True:
                    angle1=math.atan2(Hero.rect.x-clocationx, Hero.rect.y-clocationy)
                    rotate(Hero,angle1*180/math.pi)
                if towermode==True:
                    if clocationy<512 and clocationx<WIDTH:
                        blockx=clocationx/64*64
                        blocky=clocationy/64*64
                        if mapthing[clocationy/64][clocationx/64]=="#":
                            openspot=True
                        else:
                            openspot=False
        if Pause==False:
            if menubutton=="Start":
                NextWave=True
            elif menubutton=="Pause":
                Pause=True
                print "pause?"
            elif menubutton=="Menu":
                print "Back to Menu"
            elif menubutton=="Exit":
                running=False
                
            if Hero.fire==True and Hero.cfire>=Hero.firingdelay:
                Hero.fire=False
                Hero.cfire=0
                for shot in Bullets:
                    if shot.active==False:
                        shot.active=True
                        shot.startpointx=Hero.rect.x+16
                        shot.startpointy=Hero.rect.y+16
                        shot.endpointx=bulletmovement(Hero.rect.x+16,Hero.rect.y+16,Hero.hitx,Hero.hity)[0]
                        shot.endpointy=bulletmovement(Hero.rect.x+16,Hero.rect.y+16,Hero.hitx,Hero.hity)[1]
                        shot.attack=Hero.attack
                        shot.speed=Hero.bulletspeed
                        break
             
            if NextWave==True:
                wavegoing=True
                NextWave=False
                for Baddie in Buggies:
                    if Baddie.alive==True and Baddie.firstactive==True:
                        wavegoing=False
                        break
                if wavegoing==True:
                    Wavelevel+=1
                    Buggies.empty()
                    for x in range(CLASS.LvlBuggies(Wavelevel).attackers):
                        Buggies.add(CLASS.LvlBuggies(Wavelevel))
                    framerate=49
            if towermode==True:                
                if openspot==True:
                    pygame.draw.circle(screen,(0,255,0),(blockx+32,blocky+32),Displaytower[ctower].rangeatt,1)
                    render(bottom)
                    Displaytower[ctower].rect.x=blockx
                    Displaytower[ctower].rect.y=blocky
                    render(Displaytower[ctower])       
                else:
                    pygame.draw.circle(screen,(255,0,0),(blockx+32,blocky+32),Displaytower[ctower].rangeatt,1)
                if thistower!=0:
                    screen.blit(myfont.render("Attack:"+str(thistower.attack), 1,THECOLORS['white']),(304,629))
                    screen.blit(myfont.render("Range:"+str(thistower.rangeatt), 1,THECOLORS['white']),(304,667))
                    screen.blit(myfont.render("Shot Speed:"+str(thistower.shottime), 1,THECOLORS['white']),(304,710))
                
            for tower in Towers:
                tower.active=True
            
            if goup==True:
                if Hero.rect.y>0:
                    Hero.rect.y-=Hero.speed
                #rotate(Hero,0)  
            if godown==True:
                if Hero.rect.y+32<512:
                    Hero.rect.y+=Hero.speed
              #  rotate(Hero,180)    
            if goleft==True:
                if Hero.rect.x>0:
                    Hero.rect.x-=Hero.speed
              #  rotate(Hero,90) 
            if goright==True:
                if Hero.rect.x+32<WIDTH:
                    Hero.rect.x+=Hero.speed
              #  rotate(Hero,270)    
            
        
            framerate=framerate+1
            
            if framerate>=50:
                framerate=0
                for Badthing in Buggies:
                    if Badthing.firstactive==False:
                        Badthing.firstactive=True
                        Badthing.alive=True
                        break
                
            for baddie in Buggies:
                if baddie.firstactive==True:
                    if baddie.moving==True and baddie.currentwaypoint+1<len(waypoints) and baddie.alive==True:
                        stats=objectmovement(baddie.startpointx,baddie.startpointy,baddie.endpointx,baddie.endpointy,baddie.speed)
                        #bug.rotate(stats[1]*180/math.pi)
                        baddie.rect.x=stats[2][0]
                        baddie.rect.y=stats[2][1]
                        baddie.startpointx=baddie.rect.x
                        baddie.startpointy=baddie.rect.y
                        if stats[0]==True:
                            baddie.moving=False
                    
                    elif baddie.moving==False and baddie.currentwaypoint+2<len(waypoints)and baddie.alive==True:
                        baddie.moving=True    
                        baddie.currentwaypoint+=1
                        baddie.startpointx=waypoints[baddie.currentwaypoint][0]         
                        baddie.startpointy=waypoints[baddie.currentwaypoint][1]
                        baddie.endpointx=waypoints[baddie.currentwaypoint+1][0]
                        baddie.endpointy=waypoints[baddie.currentwaypoint+1][1]
                    else:
                        Hero.lives-=1
                        baddie.alive=False;
            
            for towerthing in Towers:
                if towerthing.active==True:
                    towerthing.delayshot+=1
                    render(towerthing)        
                    for baddie in Buggies:
                        if baddie.alive==True:
                            if ((towerthing.rect.x-baddie.rect.x)**2+(towerthing.rect.y-baddie.rect.y)**2)**0.5<towerthing.rangeatt and towerthing.delayshot>=towerthing.shottime:
                                towerthing.delayshot=0
                                for shot in Bullets:
                                    if shot.active==False:
                                        shot.active=True
                                        shot.startpointx=towerthing.rect.x+32
                                        shot.startpointy=towerthing.rect.y+32
                                        shot.endpointx=baddie.rect.x+32
                                        shot.endpointy=baddie.rect.y+32
                                        shot.attack=towerthing.attack
                                        shot.speed=towerthing.towerspeed
                                        stats=objectmovement(shot.startpointx,shot.startpointy,shot.endpointx,shot.endpointy,shot.speed)
                                        rotate(towerthing,stats[1]*180/math.pi)
                                        break
            for shot in Bullets:
                if shot.active==True:
                    stats=objectmovement(shot.startpointx,shot.startpointy,shot.endpointx,shot.endpointy,shot.speed)
                    rotate(shot,stats[1]*180/math.pi)
                    
                    shot.startpointx=stats[2][0]
                    shot.rect.x=shot.startpointx
                    
                    shot.startpointy=stats[2][1]
                    shot.rect.y=shot.startpointy
                    
                    render(shot)
                    if shot.rect.x<0 or shot.rect.y>512 or shot.rect.x<0 or shot.rect.y>768:
                        shot.active=False
                    
                    if stats[0]==True:
                        shot.active=False
                  
                    for baddie in Buggies:
                        if baddie.alive==True: #and baddie.firstactive==True:
                            if pygame.sprite.collide_rect(shot,baddie)==True:
                                shot.active=False
                                baddie.health=baddie.health-shot.attack
                                if baddie.health<0:
                                    baddie.alive=False
                                    Hero.money+=baddie.value                            
                                break
    
            for baddie in Buggies:
                if baddie.alive==True:
                    if baddie.health!=baddie.totalhealth:
                        pygame.draw.rect(screen, (0, 255, 0), (baddie.rect.x, baddie.rect.y-10, 64*baddie.health/baddie.totalhealth,3))
                        pygame.draw.rect(screen, (255, 0, 0), (baddie.rect.x+64*baddie.health/baddie.totalhealth, baddie.rect.y-10, 64*(baddie.totalhealth-baddie.health)/baddie.totalhealth,3))
                    else:
                        pygame.draw.rect(screen, (0, 255, 0), (baddie.rect.x, baddie.rect.y-10, 64,3))
                    render(baddie)    
                if baddie.firstactive==True and baddie.alive==False:
                    baddie.remove(Buggies)
            if Hero.lives<=0:
                print "GAME OVER"
                break
        else:
            screen.blit(myfont.render("Paused. Click to unpause", 1,THECOLORS['white']),(350,350))
            
        
        screen.blit(myfont.render("Money:"+str(Hero.money), 1,THECOLORS['white']),(558,547))
        screen.blit(myfont.render("Lives:"+str(Hero.lives), 1,THECOLORS['white']),(558,587))

            
        render(Hero)
        pygame.display.update()
        clock.tick(60)
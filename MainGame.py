import pygame
import sys
from pygame import *
import math
import random
import AllClass as CLASS
import os.path


## If you get the no available video device error, copy and paste the below code ##
import platform, os
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'
### If you get the no available video device error, copy and paste the above code ###





def Main(difficulty,maptype):
    pygame.init()
    HEIGHT=480+234
    WIDTH=736
    screen = pygame.display.set_mode((WIDTH,HEIGHT))#,FULLSCREEN)
    pygame.display.set_caption('Tower Defence')
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
        if clickx>548 and clickx<622 and clicky>640 and clicky<667:
            return "Start"
        elif clickx>636 and clickx<711 and clicky>640 and clicky<667:
            return "Pause"
        elif clickx>548 and clickx<622 and clicky>676 and clicky<700:
            return "Menu"
        elif clickx>636 and clickx<711 and clicky>676 and clicky<700:
            return "Exit"
        return False
    
        
    Buggies=pygame.sprite.Group()
    Towers=[]
    waypoints=[]
    Bullets=pygame.sprite.Group()   
    Mines=pygame.sprite.Group() 
    
    Towertypenum=4
    Displaytower=[]
    towerdefaultchoice=0
    for x in range(Towertypenum):
        Displaytower.append(CLASS.Tower(x,'data/tower'+str(x)+'.png'))


    #nNew map
    if os.path.isfile("Maps/Map"+str(maptype)+".txt")==True:
        mapfile=open("Maps/Map"+str(maptype)+".txt","r")
        tempmap="".join(mapfile.readlines())[:-1]
        mapfile.close()
        mapthing=[]
        #Standard size of map (number of tiles down and across)       
        
        for x in range(1,16):
            mapthing.append(tempmap[(x-1)*23:x*23])
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

    print waypoints
    for item in mapthing:
        print "".join(item)
    for x in range(100):
        Bullets.add(CLASS.Bullet(1, 'data/heromissile.png'))
        
    bug=CLASS.LvlBuggies(1)
    
    CharacterGuy=CLASS.CharacterGuy(0,0,'data/bug.png')
    
    heromode=True
    
    #Displaytower=Tower(1,'data/towerblack.png')
    
    current=-1
    
    #for x in range(len(mapthing)):
        #print x,"".join(mapthing[x])
    
    backdrop=pygame.image.load('data/BACKGROUNDTEMP.png')
    # Loop and draw the background
    running=True
    
    clocationx=clocationy=0
    blockx=blocky=0
    openspot=False
    framerate=49
    cout=0
    key.set_repeat(1, 1)
    
    
    
    Wavelevel=0
    NextWave=True
    Pause=False
    
    for x in range(CLASS.LvlBuggies(Wavelevel).attackers):
        Buggies.add(CLASS.LvlBuggies(Wavelevel))
    
    bottom=CLASS.BlackImage(0,HEIGHT-234,'data/sidesc.png')
    
    while running:
        menubutton=""
        screen.blit(backdrop, (0, 0))
        render(bottom)
        counter=0
        goright=goleft=godown=goup=False
        
        for event in pygame.event.get():
            counter+=1
            if event.type == pygame.QUIT:
                running==False
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_RIGHT:
                    goright=True
                elif event.key==K_LEFT :
                    goleft=True
                elif event.key==K_DOWN:
                    godown=True
                elif event.key==K_UP:
                    goup=True
                if event.key==K_ESCAPE:
                    sys.exit()
        
            if event.type==KEYUP:
                if event.key==K_s:
                    towerdefaultchoice+=1
                    towerdefaultchoice%=4
                if event.key==K_n:
                    NextWave=True           
                    
                        
            if event.type==MOUSEBUTTONDOWN:
                locationx,locationy=event.pos
                if heromode!=True:
                    if locationy<480 and locationx<WIDTH:
                        print locationx/32,locationy/32
                        if mapthing[locationy/32][locationx/32]=="#":
                            mapthing[locationy/32][locationx/32]=1  
        
                            filething="data/tower"+str(towerdefaultchoice)+".png"
                            Towers.append(CLASS.Tower(towerdefaultchoice,filething))
                            Towers[-1].rect.x=locationx/32*32
                            Towers[-1].rect.y=locationy/32*32
                        else:
                            print "OCCUPIED"
                    else:
                        menubutton=isbuttonclicked(locationx,locationy)
                
            if event.type==MOUSEMOTION:
                clocationx,clocationy=event.pos
                if clocationy<480 and clocationx<WIDTH:
                    blockx=clocationx/32*32
                    blocky=clocationy/32*32
                    if mapthing[clocationy/32][clocationx/32]=="#":
                        openspot=True
                    else:
                        openspot=False
            
        if menubutton=="Start":
            NextWave=True
        elif menubutton=="Pause":
            Pause=True
        elif menubutton=="Menu":
            print "Back to Menu"
        elif menubutton=="Exit":
            running=False
        
         
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
        if heromode!=True:    
            
            if openspot==True:
                pygame.draw.circle(screen,(0,255,0),(blockx+16,blocky+16),Displaytower[towerdefaultchoice].rangeatt,1)
                Displaytower[towerdefaultchoice].rect.x=blockx
                Displaytower[towerdefaultchoice].rect.y=blocky
                render(Displaytower[towerdefaultchoice])       
            else:
                pygame.draw.circle(screen,(255,0,0),(blockx+16,blocky+16),Displaytower[towerdefaultchoice].rangeatt,1)
            
        for tower in Towers:
            tower.active=True
        
        if goup==True:
            if CharacterGuy.rect.y>0:
                CharacterGuy.rect.y-=CharacterGuy.speed
            rotate(CharacterGuy,0)  
        if godown==True:
            if CharacterGuy.rect.y+32<480:
                CharacterGuy.rect.y+=CharacterGuy.speed
            rotate(CharacterGuy,180)    
        if goleft==True:
            if CharacterGuy.rect.x>0:
                CharacterGuy.rect.x-=CharacterGuy.speed
            rotate(CharacterGuy,90) 
        if goright==True:
            if CharacterGuy.rect.x+32<WIDTH:
                CharacterGuy.rect.x+=CharacterGuy.speed
            rotate(CharacterGuy,270)    
        
    
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
                                    shot.startpointx=towerthing.rect.x+16
                                    shot.startpointy=towerthing.rect.y+16
                                    shot.endpointx=baddie.rect.x+16
                                    shot.endpointy=baddie.rect.y+16
                                    shot.attack=towerthing.attack
                                    shot.speed=towerthing.towerspeed
                                    stats=objectmovement(shot.startpointx,shot.startpointy,shot.endpointx,shot.endpointy,shot.speed)
                                    rotate(towerthing,stats[1]*180/math.pi)     
                                    firststat=bulletmovement(shot.startpointx,shot.startpointy,shot.endpointx,shot.endpointy)   
                                    #shot.endpointx=firststat[0]
                                    #shot.endpointy=firststat[1]                
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
                
                if stats[0]==True:
                    shot.active=False
              
                for baddie in Buggies:
                    if baddie.alive==True:
                        if pygame.sprite.collide_rect(shot,baddie)==True:
                            shot.active=False
                            baddie.health=baddie.health-shot.attack
                            break
                if baddie.health<0:
                    baddie.alive=False
        for baddie in Buggies:
            if baddie.alive==True:
                if baddie.health!=baddie.totalhealth:
                    pygame.draw.rect(screen, (0, 255, 0), (baddie.rect.x, baddie.rect.y-10, 32*baddie.health/baddie.totalhealth,3))
                    pygame.draw.rect(screen, (255, 0, 0), (baddie.rect.x+32*baddie.health/baddie.totalhealth, baddie.rect.y-10, 32*(baddie.totalhealth-baddie.health)/baddie.totalhealth,3))
                else:
                    pygame.draw.rect(screen, (0, 255, 0), (baddie.rect.x, baddie.rect.y-10, 32,3))
                render(baddie)    
            if baddie.firstactive==True and baddie.alive==False:
                baddie.remove(Buggies)
    
        render(CharacterGuy)
        pygame.display.update()
        clock.tick(60)
        
#Main(1,1)
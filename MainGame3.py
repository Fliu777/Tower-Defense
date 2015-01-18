#Game
#This is the main Game
#Frank Liu
#January 27,2012


from pygame import *
import math
import random
import AllClass as CLASS
import os.path
from pygame.color import THECOLORS
from time import sleep
import pygame
from pygame import *

## If you get the no available video device error, copy and paste the below code ##
import platform, os
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'
### If you get the no available video device error, copy and paste the above code ###



def Main(difficulty,maptype):   
    
    #Initializes pygame and sizes and fonts
    pygame.init()
    mapheight=512
    HEIGHT=mapheight+234
    WIDTH=768
    screen = pygame.display.set_mode((WIDTH,HEIGHT),0,32)
    pygame.display.set_caption('Tower Defence')
    myfont=pygame.font.SysFont("Vera", 30)
    clock=pygame.time.Clock()   
    otherfont=pygame.font.SysFont("Vera", 20)
        
    #renders an image at its current location
    def render(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    #rotates the original image by the angle to maintain some sort of resolution
    def rotate(self,angle):
        self.image=pygame.transform.rotate(self.original, angle)
        self.image=self.image.convert_alpha()
        self.rect==pygame.transform.rotate(self.original, angle)
        
    #moves object from a to b given starting and ending points and rate, moves distance by rate each time, getting closer to b,
    def objectmovement(currx,curry,lastx,lasty,rate):
        #stats[0]=done? True is finished, False is still going
        #stats[1]= angle
        #stats[2]= (newx,newy)
    
        stats=[]
        #calculate angle
        angle1=math.atan2(currx-lastx, curry-lasty)
        
        distleft=((currx-lastx)**2+(curry-lasty)**2)**0.5
        #distleft=0
        
        #if the distance is smaller than the rate, then point A is now also point B
        if distleft<=rate:
            stats.append(True)
            stats.append(angle1)
            stats.append((lastx,lasty))
        else:
            stats.append(False)
            stats.append(angle1)
            stats.append((currx-rate*math.sin(angle1),curry-rate*math.cos(angle1)))
        return stats
     
    #Given point A and B, extends B until it is off screen
    def bulletmovement(currx,curry,lastx,lasty):
        #change of x and y
        xincrement=(lastx-currx)
        yincrement=(lasty-curry)
        result=[]
        
        while True:
            #applies change
            lastx+=xincrement
            lasty+=yincrement
            
            #checks if it is off screen
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
    
    #Checks if the buttons are clicked by location
    def isbuttonclicked(clickx,clicky):
        if clickx>581 and clickx<674 and clicky>657 and clicky<698:
            return "Start"
        elif clickx>670 and clickx<744 and clicky>657 and clicky<698:
            return "Pause"
        elif clickx>581 and clickx<674 and clicky>701 and clicky<742:
            return "Menu"
        elif clickx>670 and clickx<744 and clicky>701 and clicky<742:
            return "Exit"
        return False
    
    #Checks which tower is selected
    def towerchoice(clickx,clicky):
        if clickx>33 and clickx<88 and clicky>589 and clicky<646:
            return 0
        if clickx> 109 and clickx<164 and clicky>589 and clicky<646:
            return 1  
        if clickx>189 and clickx<245 and clicky>589 and clicky<646:
            return 2   
        if clickx>33 and clickx<88 and clicky>665 and clicky<722:
            return 3
        if clickx> 109 and clickx<164 and clicky>665 and clicky<722:
            return 4  
        if clickx>189 and clickx<245 and clicky>665 and clicky<722:
            return 5      
 
        return -1
    
        
    #initialization
    Buggies=pygame.sprite.Group()
    Towers=[]
    waypoints=[]
    Bullets=pygame.sprite.Group()   
    Mines=pygame.sprite.Group() 
    Towertypenum=6
    Displaytower=[]
    heromode=True
    towermode=False
    towerstats=""
    clocationx=clocationy=0
    blockx=blocky=0
    openspot=False
    framerate=49
    key.set_repeat(1, 1)
    ctower=0
    settower=False
    status=""
    Wavelevel=0
    NextWave=True
    Pause=False
    thistower=0
    displaymessage=""
    
    #Makes display towers
    for x in range(Towertypenum):
        Displaytower.append(CLASS.Tower(x,'data/Towers/tower'+str(x)+'.png'))


    #New map
    #this is the file i/o handling, this part only reads a predefined map and the waypoints that are generated by background.py
    
    #First checks if the file exists
    if os.path.isfile("Maps/Map"+str(maptype)+".txt")==True:
        mapfile=open("Maps/Map"+str(maptype)+".txt","r")
        tempmap="".join(mapfile.readlines())
        mapfile.close()
        mapthing=[]
        #reads the txt file and converts the tiles to a 2d array  
        #Standard size of map (number of tiles down and across)
        #converts the points into the array since there is a standart amount of tiles across and down
        for x in range(1,9):
            mapthing.append(tempmap[(x-1)*12:x*12])
        for x in range(len(mapthing)):
            mapthing[x]=list(mapthing[x])
                
            
        #Reads the points that the buggies must traverse, mostly reading through the formatting
        if os.path.isfile("Maps/Path"+str(maptype)+".txt")==True:
            pathfile=open("Maps/Path"+str(maptype)+".txt","r")
            temppath="".join(pathfile.readlines()).splitlines()
            pathfile.close()
            
            #Each point is in format (x,y), so we are dissecting the points out here into a list with tuples
            for x in range(len(temppath)):
                firstpoint=temppath[x][temppath[x].find("(")+1:temppath[x].find(",")]
                secondpoint=temppath[x][temppath[x].find(",")+1:temppath[x].find(")")]
                waypoints.append((int(firstpoint),int(secondpoint)))
        else:
            print "FILE NOT FOUND"
            pygame.quit()
    else:
        print "FILE NOT FOUND"
        pygame.quit()

                
    #Sets maximum amount of bullets on screen to be 100            
    for x in range(100):
        Bullets.add(CLASS.Bullet(1, 'data/heromissile.png'))
        

    #Creats player
    Hero=CLASS.CharacterGuy(377,480,'data/player.png')
    
    #Sets default background
    backdrop=pygame.image.load('BACKGROUNDTEMP.png')
    bottom=CLASS.BlackImage(0,HEIGHT-234,'data/sidesc.png')
    running=True
    

    #Starts the first wave
    for x in range(CLASS.LvlBuggies(Wavelevel).attackers):
        Buggies.add(CLASS.LvlBuggies(Wavelevel))
    
    
    while running:
        #Sets button as none and other initialization stuff
        menubutton=""
        goright=goleft=godown=goup=False
        
        #Renders the background
        screen.blit(backdrop, (0, 0))
        render(bottom)
        
        #Delay time that the hero can shoot
        Hero.cfire=Hero.cfire+1

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running==False
                sys.exit()
            if event.type==KEYDOWN:
                #Moves player according to key
                if event.key==K_d:
                    goright=True
                elif event.key==K_a :
                    goleft=True
                elif event.key==K_s:
                    godown=True
                elif event.key==K_w:
                    goup=True
                if event.key==K_ESCAPE:
                    #Exits out of tower placing mode and back to hero mode
                    heromode=True
                    towermode=False                       
                        
            if event.type==MOUSEBUTTONDOWN:

                #sets pause as false
                if Pause==True:
                    Pause=False
                    break
                
                #Sets display as empty
                displaymessage=""
                
                #Checks to see if the user wants to place a tower
                locationx,locationy=event.pos
                print event.pos
                temptower=towerchoice(locationx,locationy)   
                
                #Creates tower so that we can display statistics on in
                filething="data/Towers/tower"+str(ctower)+".png"
                thistower=CLASS.Tower(ctower,filething)
                
                #There has been a tower selected, go out of hero mode and into tower mode
                if temptower!=-1:
                    heromode=False
                    towermode=True
                    
                    #this is for later for the display
                    ctower=temptower
                    
                #Tower mode is true
                if towermode==True:
                    
                    #checks if tower is in bounds, essentially, the second click
                    if locationy<mapheight and locationx<WIDTH:
                        
                        #Checksif there is enough money
                        if Hero.money>=thistower.cost:
                            
                            #checks if the spot is currently empty
                            if mapthing[locationy/64][locationx/64]=="#":
                                
                                #Mark it as occupied, subtract money and place the tower in the spot
                                mapthing[locationy/64][locationx/64]="1"  
                                
                                Towers.append(thistower)
                                Hero.money-=thistower.cost
                                Towers[-1].rect.x=locationx/64*64
                                Towers[-1].rect.y=locationy/64*64
                                
                                #Back to hero mode
                                towermode=False
                                heromode=True
                                
                            else:
                                #sets message
                                displaymessage="OCCUPIED"
                        else:
                            #sets message
                            displaymessage="Insufficient Funds"
                            #back to hero mode
                            towermode=False
                            heromode=True
                    else:
                        #must be in bottom menu and thus checks for this
                        menubutton=isbuttonclicked(locationx,locationy)

                    
                else:
                    #hero mode so it tries to fire a bullet
                    if locationy<mapheight and locationx<WIDTH:
                        Hero.fire=True
                        Hero.hitx=locationx
                        Hero.hity=locationy
                    else:
                        #must be in menu place
                        menubutton=isbuttonclicked(locationx,locationy)                    
                    
                
            if event.type==MOUSEMOTION:
                clocationx,clocationy=event.pos
                if heromode==True:
                    # rotates hero based on the mosue
                    angle1=math.atan2(Hero.rect.x-clocationx, Hero.rect.y-clocationy)
                    rotate(Hero,angle1*180/math.pi)
                if towermode==True:
                    #renders the range of the tower and sets variable if it is open
                    if clocationy<mapheight and clocationx<WIDTH:
                        blockx=clocationx/64*64
                        blocky=clocationy/64*64
                        if mapthing[clocationy/64][clocationx/64]=="#":
                            openspot=True
                        else:
                            openspot=False
                            
        if Pause==False:
            #Displays message
            if displaymessage!="":
                screen.blit(myfont.render(displaymessage, 1,THECOLORS['white']),(311,570))
                
            #Checks which menu button it is
            if menubutton=="Start":
                NextWave=True
            elif menubutton=="Pause":
                Pause=True
            elif menubutton=="Menu":
                break
            elif menubutton=="Exit":
                pygame.quit()
             
            #Checks to see if hero can fire a bullet and the delay is sufficient
            if Hero.fire==True and Hero.cfire>=Hero.firingdelay and Hero.money>=Hero.attackcost:
                Hero.fire=False
                Hero.cfire=0
                Hero.money-=Hero.attackcost
                
                #Finds a bullet that can be used and sets its attributes based on the hero's strength and stats
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
                      
            #checks to see if user wants next wave 
            if NextWave==True:
                wavegoing=True
                NextWave=False
                
                #checks if all bad guys have been killed, if this is true then the nextwave can be sent
                for Baddie in Buggies:
                    if Baddie.alive==True and Baddie.firstactive==True:
                        wavegoing=False
                        break
              
                                          
                if wavegoing==True:             
                    #Level goes up by 1
                    Wavelevel+=1       
                    
                    #Removes bad guys                
                    Buggies.empty()
                    
                    #Remakes the attackers and gives them statistics that are affected by the difficulty
                    for x in range(CLASS.LvlBuggies(Wavelevel).attackers):
                        currentattacker=CLASS.LvlBuggies(Wavelevel)
                        Buggies.add(currentattacker)
                        currentattacker.speed*=difficulty
                        currentattacker.health*=0.9+difficulty/10
                        currentattacker.totalhealth=currentattacker.health
                    framerate=49
                
            #If the user wants to place a tower, show the stats and draw a green circle if it can be placed and a red if it can't
            if towermode==True:                
                if openspot==True:
                    pygame.draw.circle(screen,(0,255,0),(blockx+32,blocky+32),Displaytower[ctower].rangeatt,1)
                    render(bottom)
                    Displaytower[ctower].rect.x=blockx
                    Displaytower[ctower].rect.y=blocky
                    render(Displaytower[ctower])       
                else:
                    pygame.draw.circle(screen,(255,0,0),(blockx+32,blocky+32),Displaytower[ctower].rangeatt,1)
                if Displaytower[ctower]!=0:
                    screen.blit(myfont.render("Attack:"+str(Displaytower[ctower].attack), 1,THECOLORS['white']),(304,629))
                    screen.blit(myfont.render("Range:"+str(Displaytower[ctower].rangeatt), 1,THECOLORS['white']),(304,667))
                    screen.blit(myfont.render("Shot Speed:"+str(Displaytower[ctower].shottime), 1,THECOLORS['white']),(304,710))
            #sets all towers as active    
            for tower in Towers:
                tower.active=True
            
            #moves the hero depending on the direction and speed, also makes sure it does not go out of bounds
            if goup==True:
                if Hero.rect.y>0:
                    Hero.rect.y-=Hero.speed
                #rotate(Hero,0)  
            if godown==True:
                if Hero.rect.y+32<mapheight:
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
            
            #Checks to see if the delay between badguys if enough and will go if it is, so tells the next attacker to start
            if framerate>=50:
                framerate=0
                for Badthing in Buggies:
                    if Badthing.firstactive==False:
                        Badthing.firstactive=True
                        Badthing.alive=True
                        break
           
            #Moves the bad guy depending on where they are
            for baddie in Buggies:          
                
                #baddie has started going
                if baddie.firstactive==True:
                    
                    #currently moving and checks to see if it is on its last path
                    if baddie.moving==True and baddie.currentwaypoint+1<len(waypoints) and baddie.alive==True:
                        stats=objectmovement(baddie.startpointx,baddie.startpointy,baddie.endpointx,baddie.endpointy,baddie.speed)
                        #bug.rotate(stats[1]*180/math.pi)
                        baddie.rect.x=stats[2][0]
                        baddie.rect.y=stats[2][1]
                        baddie.startpointx=baddie.rect.x
                        baddie.startpointy=baddie.rect.y
                        if stats[0]==True:
                            baddie.moving=False
                    
                    #not moving and thus must start moving to next path if there is one
                    elif baddie.moving==False and baddie.currentwaypoint+2<len(waypoints)and baddie.alive==True:
                        baddie.moving=True    
                        baddie.currentwaypoint+=1
                        baddie.startpointx=waypoints[baddie.currentwaypoint][0]         
                        baddie.startpointy=waypoints[baddie.currentwaypoint][1]
                        baddie.endpointx=waypoints[baddie.currentwaypoint+1][0]
                        baddie.endpointy=waypoints[baddie.currentwaypoint+1][1]
                    
                    #must of reached end
                    else:
                        Hero.lives-=1
                        baddie.alive=False;
            
            #this huge triple for loops looks for each tower, finds the first bad guy and looks for a shot to fire
            for towerthing in Towers:
                #Checks if delay of tower has been reached
                if towerthing.active==True:
                    towerthing.delayshot+=1
                    render(towerthing)        
                    
                    #looks for a bad guy in range
                    for baddie in Buggies:
                        if baddie.alive==True:
                            if ((towerthing.rect.x-baddie.rect.x)**2+(towerthing.rect.y-baddie.rect.y)**2)**0.5<towerthing.rangeatt and towerthing.delayshot>=towerthing.shottime:
                                towerthing.delayshot=0
                                
                                #Finds bullet to use and fires at badguy
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
                                    
            #checks collisions between the bullets on screen and the bad guys
            for shot in Bullets:
                #bullet is active
                if shot.active==True:
                    
                    #moves bullet by its spee
                    stats=objectmovement(shot.startpointx,shot.startpointy,shot.endpointx,shot.endpointy,shot.speed)
                    rotate(shot,stats[1]*180/math.pi)
                    
                    shot.startpointx=stats[2][0]
                    shot.rect.x=shot.startpointx
                    
                    shot.startpointy=stats[2][1]
                    shot.rect.y=shot.startpointy
                    
                    render(shot)
                    
                    #if bullet is out of bounds, get rid of it
                    if shot.rect.x<0 or shot.rect.y>mapheight or shot.rect.x<0 or shot.rect.y>768:
                        shot.active=False
                    
                    #if it has reached final destination, get rid of it
                    if stats[0]==True:
                        shot.active=False
                  
                    #checks each bad guy to see if the bullet has hit tehm
                    for baddie in Buggies:
                        if baddie.alive==True: 
                            if pygame.sprite.collide_rect(shot,baddie)==True:
                                shot.active=False
                                baddie.health=baddie.health-shot.attack
                                #subtracts health
                                
                                #if dead, you get money
                                if baddie.health<0:
                                    baddie.alive=False
                                    Hero.money+=baddie.value                            
                                break
            
            #draws health bar over each bad guy        
            for baddie in Buggies:
                if baddie.alive==True:
                    #Has lost health
                    if baddie.health!=baddie.totalhealth:
                        #draws red and green bars
                        pygame.draw.rect(screen, (0, 255, 0), (baddie.rect.x, baddie.rect.y-10, 32*baddie.health/baddie.totalhealth,3))
                        pygame.draw.rect(screen, (255, 0, 0), (baddie.rect.x+32*baddie.health/baddie.totalhealth, baddie.rect.y-10, 32*(baddie.totalhealth-baddie.health)/baddie.totalhealth,3))
                        
                    #full health
                    else:
                        pygame.draw.rect(screen, (0, 255, 0), (baddie.rect.x, baddie.rect.y-10, 32,3))
                    render(baddie)    
                #if dead, remove it
                if baddie.firstactive==True and baddie.alive==False:
                    baddie.remove(Buggies)
                    
            #If you're dead, its game over and you lose and go back to Main Menu
            if Hero.lives<=0:
                print "GAME OVER"
                status="lose"
                break
        else:
            screen.blit(myfont.render("Paused. Click screen to unpause", 1,THECOLORS['white']),(250,350))
            
        #shows money and lives left
        
        screen.blit(myfont.render("Money:"+str(Hero.money), 1,THECOLORS['white']),(597,579))
        screen.blit(myfont.render("Lives:"+str(Hero.lives), 1,THECOLORS['white']),(597,597))
        
        #This part checks if you have won the game, that being you are done to the last level
        totalwaves=7
        count=0
        for x in Buggies:
            count+=1
        if count==0:
            if Wavelevel+1>totalwaves:
                status="win"
                break      
            
        #Wave shows progress
        screen.blit(otherfont.render(str(Wavelevel)+"/"+str(totalwaves), 1,THECOLORS['red']),(592,524))
        
        #shows hero    
        render(Hero)
        pygame.display.update()
        clock.tick(60)
        
    #DELAY   and shows win or lose screen
    if status=="win":
        screen.blit(myfont.render("Congratulations, you have won!", 1,THECOLORS['white']),(250,350))
        pygame.display.update()
        sleep(2)
    elif status=="lose":
        screen.blit(myfont.render("FAILURE", 1,THECOLORS['white']),(300,350))
        pygame.display.update()
        sleep(2)
        
    #returns win or loss
    return status
        

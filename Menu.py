#Menu
#This is the entry to the rest of the game
#Frank Liu
#January 27,2012

import pygame
import sys
from pygame import *
import AllClass as CLASS
from pygame.color import THECOLORS
import math

from time import sleep

import MainGame3 as Game

## If you get the no available video device error, copy and paste the below code ##
import platform, os
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'
### If you get the no available video device error, copy and paste the above code ###


#Initializes pygame and sets screen sizes
pygame.init()
HEIGHT=512+234
WIDTH=768
screen = pygame.display.set_mode((WIDTH,HEIGHT))#,FULLSCREEN)

#Sets captions and sets running as default
pygame.display.set_caption('Tower Defence')
running=True

#Initialize font
myfont=pygame.font.SysFont("Vera", 30)
  
#Function used to draw an image onto its current location
def render(self):
    screen.blit(self.image, (self.rect.x, self.rect.y))
    
 
def buttonclick(clickx,clicky):
    if backdrop=="menu":
        if clickx>183 and clickx<183+147 and clicky>483 and clicky<483+36:
            return "Start"
        elif clickx>183 and clickx<183+147 and clicky>529 and clicky<529+36:
            return "Instructions"
        elif clickx>183 and clickx<183+147 and clicky>577 and clicky<577+36:
            return "Credits"
        elif clickx>183 and clickx<183+147 and clicky>629 and clicky<629+36:
            return "Exit"
    
    #difficulty select
    elif backdrop=="Difficultyselect":
        if clickx>204 and clickx<581 and clicky>215 and clicky<304:
            return 1
        elif clickx>204 and clickx<581 and clicky>356 and clicky<446:
            return 2
        elif clickx>204 and clickx<581 and clicky>514 and clicky<604:
            return 3
    else:
        if clickx>39 and clickx<225 and clicky>670 and clicky<701:
            return "back"        
    return False

#Function used to determine if the mouse is on any button   
def buttonhighlight(clickx,clicky):
    
    #Main menu screen
    if backdrop=="menu":
        if clickx>183 and clickx<183+147 and clicky>483 and clicky<476+36:
            return (183,476)
        elif clickx>183 and clickx<183+147 and clicky>529 and clicky<529+36:
            return (183,529)
        elif clickx>183 and clickx<183+147 and clicky>577 and clicky<577+36:
            return (183,577)
        elif clickx>183 and clickx<183+147 and clicky>629 and clicky<629+36:
            return (183,629)  
        #elif clickx>170 and clickx<317 and clicky>648 and clicky<683:
        #    return (168,640)   
    
        
    #Currently on difficulty select panel
    elif backdrop=="Difficultyselect":
        offset=-10
        if clickx>219+offset and clickx<610+offset and clicky>226+offset and clicky<320+offset:
            return (219+offset,226+offset)
        elif clickx>219+offset and clickx<610+offset and clicky>382+offset and clicky<473+offset:
            return (219+offset,382+offset)
        elif clickx>219+offset and clickx<610+offset and clicky>543+offset and clicky<633+offset:
            return (219+offset,543+offset)
    
    #The only screen thats left is instructions and credits, so only back button needs to be detected
    else:
        if clickx>39 and clickx<225 and clicky>670 and clicky<701:
            return (39,670)
        
    return False




#Loads different screens and buttons
menu=pygame.image.load('./data/Opening_Menus/menu.jpg')
Highlightbutton=CLASS.Basic_Image(0,0,'./data/Opening_Menus/button.png')
Highlightbig=CLASS.Basic_Image(0,0,'./data/Opening_Menus/button2.png')
Instructions=pygame.image.load('./data/Opening_Menus/instructions.jpg')
Credits=pygame.image.load('./data/Opening_Menus/Credits.jpg')
#Highscores=pygame.image.load('data/Opening_Menus/Highscores.jpg')
Difficultyselect=pygame.image.load('./data/Opening_Menus/difficulty.jpg')
Gameover=pygame.image.load('./data/Opening_Menus/gameover.jpg')


#Sets framerate by initializing clock 
clock=pygame.time.Clock()

#Sets the highlighted button as false
buttonactive=False

#Sets default background as menu
backdrop="menu"

#Sets default highlighted button as small version
renderbutton=Highlightbutton

#Difficulty level is 0
diflevel=0

while running:
    #Makes background image depending on what the mode is
    if backdrop=="menu":
        screen.blit(menu, (0, 0))
    elif backdrop=="Instructions":
        screen.blit(Instructions, (0, 0))
    elif backdrop=="Credits":
        screen.blit(Credits, (0, 0))
    #elif backdrop=="Highscores":
    #    screen.blit(Highscores, (0, 0))
    elif backdrop=="Difficultyselect":
        screen.blit(Difficultyselect, (0, 0))
  
        
    #Sets choice as nothing
    menuchoice=""
    #Sets location of temporary button to be 0,0
    location=(0,0)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running==False
            sys.exit()
        if event.type==MOUSEMOTION:
            clocationx,clocationy=event.pos

            #Depending on what screen it is in, the buttons that are highlighted when they mouse over are different
            #Also sets the location of the button they hover over as the highlighted button location
            if backdrop=="menu":
                renderbutton=Highlightbutton
                location=buttonhighlight(clocationx,clocationy)
                if location!=False:
                    renderbutton.rect.x=location[0]
                    renderbutton.rect.y=location[1]
                    buttonactive=True
                else:
                    buttonactive=False
            elif backdrop!="Difficultyselect":
                renderbutton=Highlightbutton
                location=buttonhighlight(clocationx,clocationy)
                if location!=False:
                    renderbutton.rect.x=location[0]
                    renderbutton.rect.y=location[1]
                    buttonactive=True
                else:
                    buttonactive=False
            else:
                renderbutton=Highlightbig
                location=buttonhighlight(clocationx,clocationy)
                if location!=False:
                    renderbutton.rect.x=location[0]
                    renderbutton.rect.y=location[1]
                    buttonactive=True
                else:
                    buttonactive=False    
                    
                    
    
        if event.type==MOUSEBUTTONDOWN:
            clocationx,clocationy=event.pos
            print event.pos
            #Gets the button that they clicked on and sets highlighted button to none
            menuchoice=buttonclick(clocationx,clocationy)
            buttonactive=False
            
            
    #Changes background dependant on what screen it is on  (nain menu choices)
    if backdrop=="menu":
        if menuchoice=="Start":
            backdrop="Difficultyselect"
        elif menuchoice=="Instructions":
            backdrop="Instructions"
        elif menuchoice=="Credits":
            backdrop="Credits"
        #elif menuchoice=="Highscores":
        #    backdrop="Highscores"
        elif menuchoice=="Exit":
            running=False
            sys.exit()
            
    #Sets difficulty based on what they chose        
    elif backdrop=="Difficultyselect":
        if menuchoice==1 or menuchoice==2 or menuchoice==3:
            diflevel=menuchoice
    
    #Sets screen as main screen if they chose to go back
    else:
        if menuchoice=="back":
            backdrop="menu"
    
    #renders the highlighted buttons and text needed for each screen
    if backdrop=="menu":
    
        if buttonactive==True:
            render(renderbutton)
    
        screen.blit(myfont.render("Start", 1,THECOLORS['white']),(178+10,483+5))
        screen.blit(myfont.render("Instructions", 1,THECOLORS['white']),(178+10,529+5))
        screen.blit(myfont.render("Credits", 1,THECOLORS['white']),(178+10,577+5))
        screen.blit(myfont.render("Exit", 1,THECOLORS['white']),(178+10,629+5))
       #screen.blit(myfont.render("Exit", 1,THECOLORS['white']),(178+10,640+8+10))
    elif backdrop=="Difficultyselect":
        if buttonactive==True:
            render(renderbutton)
            
        screen.blit(myfont.render("Easy", 1,THECOLORS['white']),(256,251+8))
        screen.blit(myfont.render("Medium", 1,THECOLORS['white']),(256,393+8))
        screen.blit(myfont.render("Difficult", 1,THECOLORS['white']),(256,543+8))          

    else:
        if buttonactive==True:
            render(renderbutton)
        screen.blit(myfont.render("Back", 1,THECOLORS['white']),(39,670))        
    
        
    #If the difficulty has been set, then the game begins   
    if diflevel!=0:
        status=Game.Main(diflevel,1)        
        #Game has finished, status checks if the user has won or lost
        
        #makes ending screen depandant on status

        
        #if status=="lose":
            #screen.blit(Gameover, (0, 0))
            #screen.blit(myfont.render("GAME OVER", 1,THECOLORS['white']),(300,300))  
        #elif status=="win":
            #screen.blit(Gameover, (0, 0))
            #screen.blit(myfont.render("YOU WIN", 1,THECOLORS['white']),(300,300))  
            
            
        ##updates screen and pauses for user to see
        #pygame.display.update()
        #sleep(3)
        
        #Resets all variables as default
        diflevel=0
        menuchoice=""        
        renderbutton=Highlightbutton    
        backdrop="menu"    
        buttonactive=False
        
    pygame.display.update()
    
    #Controls framerate
    clock.tick(60)
    
    

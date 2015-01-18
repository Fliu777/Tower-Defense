#Background Generator
#This draws the map and processes the waypoints
#Frank Liu
#January 27,2012

#from PIL import Image
#import pygame
#import background as tiles
#import math
#import random

### If you get the no available video device error, copy and paste the below code ##
#import platform, os
#if platform.system() == "Windows":
    #os.environ['SDL_VIDEODRIVER'] = 'windib'
#### If you get the no available video device error, copy and paste the above code ###


#pygame.init()
#HEIGHT=512
#WIDTH=768


#screen = pygame.display.set_mode((WIDTH,HEIGHT))
#pygame.display.set_caption('Tiled Background')
#class Sprite:
    #def __init__(self, xpos, ypos, filename):
	#self.x = xpos
	#self.y = ypos
	#self.bitmap = pygame.image.load(filename)
	#self.original=self.bitmap
	#self.startpointx=xpos
	#self.startpointy=ypos
	#self.endpointx=xpos
	#self.endpointy=ypos
	#self.active=False
    #def render(self,xplace,yplace):
	#screen.blit(self.bitmap, (xplace, yplace))
    #def rotate(self,angle):
	#rotate1 = pygame.transform.rotate
	#self.bitmap=rotate1(self.original, angle)

##moves object from a to b given starting and ending points and rate, moves distance by rate each time, getting closer to b,
#def objectmovement(currx,curry,lastx,lasty,rate):
        ##stats[0]=done? True is finished, False is still going
        ##stats[1]= angle
        ##stats[2]= (newx,newy)
    
        #stats=[]
        #angle1=math.atan2(currx-lastx, curry-lasty)
        
        #distleft=((currx-lastx)**2+(curry-lasty)**2)**0.5
        ##distleft=0
        #if distleft<=rate:
            #stats.append(True)
            #stats.append(angle1)
            #stats.append((lastx,lasty))
        #else:
            #stats.append(False)
            #stats.append(angle1)
            #stats.append((currx-rate*math.sin(angle1),curry-rate*math.cos(angle1)))
        #return stats
	

#def Generator():
    #SIZEOFIMAGE=64
	    
    ## Determine the number of rows and columns of tiles
    #size=tiles.size()
    #rows=size[0]
    #columns=size[1]
    
    ##loads tiles
    #dirt = Sprite(0,0,'data/dirt.png')
    #grass= Sprite(0,0,'data/grass.png')
    #im= Image.new('RGB', (WIDTH,HEIGHT))
    
    #crow=ccol=0
    #waypoints=tiles.waypoints()
    #current=-1
    ##diagonalline=Sprite(0,0,'data/dirtline1.bmp')
    ##diagonalline2=Sprite(0,0,'data/dirtline2.bmp')

    ##Drawing the grass
    #while crow<rows:
	#while ccol<columns:
	    ##if canvas[crow][ccol]==".":
		##dirt.render(16*ccol,16*crow)
	    ##else:
	    #grass.render(SIZEOFIMAGE*ccol,SIZEOFIMAGE*crow)
	    ##print crow,ccol
	    #ccol=ccol+1
	#ccol=0
	#crow=crow+1
    
	
	
    ##Drawing the road, could support diagonal roads, but decided not to implement it
    #startx=endx=endy=starty=0
    #for x in range(HEIGHT*WIDTH/64/64):
	    
	#if dirt.active==True and current+1<len(waypoints):
	    
	    ##checks to see if they are the same
	    #if math.fabs(startx-endx)<0.001 or math.fabs(starty-endy)<0.001:
		#stats=objectmovement(startx,starty,endx,endy,64)
		#dirt.rotate(stats[1]*180/math.pi)
		#dirt.x=stats[2][0]
		#dirt.y=stats[2][1]
		#startx=dirt.x
		#starty=dirt.y	    
		#dirt.render(dirt.x, dirt.y)	  	    
	    #else:
		#stats=objectmovement(startx,starty,endx,endy,4)
		#diagonalline.x=stats[2][0]
		#diagonalline.y=stats[2][1]
		#startx=diagonalline.x
		#starty=diagonalline.y
		#choice=random.randint(0,1)
		#if choice==1:
		    #diagonalline2.render(diagonalline.x, diagonalline.y)
		#else:
		    #diagonalline.render(diagonalline.x, diagonalline.y)
	    #if stats[0]==True:
		#dirt.active=False
		
	#if dirt.active==False and current+2<len(waypoints):
	    #current=current+1
	    #startx=waypoints[current][0]	        
	    #starty=waypoints[current][1]
	    #endx=waypoints[current+1][0]
	    #endy=waypoints[current+1][1]
	    #dirt.active=True    
    #pixellist=[]
    
    ##draws image of tiles to a file
    
    #for x in range(WIDTH):
	#for y in range(HEIGHT):
	    #im.putpixel((x,y),screen.get_at((x,y))[:3])  
    #im.save('BACKGROUNDTEMP.png')    
	    
    ####
    
	 
#Generator()

#Map output
#This ouputs the map onto the file
#Frank Liu
#January 27,2012

from PIL import Image
import time

MapNum=1


Mapfile=open("Maps/Map%s.txt"%MapNum,"a")
Pathfile=open("Maps/Path%s.txt"%MapNum,"a")

def WriteMap(Line):
    Mapfile.write(str(Line))

def WritePath(Line):
    Pathfile.write(str(Line)+"\n")

start_time = time.time()
INCREMENT=64 #this is the conversion from it to the tiles


HEIGHT=512
WIDTH=768



turns=[]
for x in range(15):
    turns.append(0)

Mapnumber="2"
    
Backpath=Image.open('data/background'+Mapnumber+'.png')
#gets size of image
width, height= Backpath.size
#print width, height
image=[]
Path=Backpath.load()


#goes through each pixel and creats a 2d array based on the rgb value
for x in range(height):
    image.append([])
    for y in range(width):
        third=Path[y,x][2]
        #print Path[y,x]
        if Path[y,x]==(34,177,76,255):
            image[x].append("#") #no critters here
        elif Path[y,x]==(0,0,0,255):
            image[x].append("A") #Critter Path
        elif Path[y,x]==(255,255,third,255):
            image[x].append(str(255-third))
            turns[255-third]=(y,x)#PATH thatof critter follows
        else:
            image[x].append(" ") #error
newturns=[]

for x in range(len(turns)):  #take out the 0's and nomilization
    if turns[x]!=0:
        newturns.append((int(turns[x][0]/INCREMENT*INCREMENT),int(turns[x][1]/INCREMENT*INCREMENT)))
        #rounds to nearest 64 divisior floor
        #newturns.append((turns[x][0],turns[x][1]))
    else:
        break

#pygame.display.update()


            
road=0
row=col=0
newpath=[[]]

#Making the tiles
#goes through each 64 by 64 block and defines what kind of tile it will be based on a hierachy
#if there is any near white/path dots, then the block is that
#if there is any road, then it is that, provided that it is not a path
#otherwise, it be grass

while row<HEIGHT:
    road=0
    ch="#"
    
    #looking in each tile
    for hi in range(row,row+64):
        for wi in range(col,col+64): 
            if image[hi][wi]=="A":
                road=1
                ch="."
                break 
        if road==1:
            break
    newpath[row/INCREMENT].append(ch)
    col = col + INCREMENT
    if col >= WIDTH:
        col = 0
        newpath.append([])
        row=row+INCREMENT
newpath=newpath[:-1]

#writes to file, that being the entire map path and each waypoint
for x in range(len(newpath)):
    WriteMap("".join(newpath[x]))
for item in newturns:
    WritePath(item)

#returns map
def newimage():
    return newpath

#returns size
def size():
    return (len(newpath),len(newpath[0]))

#returns waypoints
def waypoints():
    return newturns

Mapfile.close()
Pathfile.close()
       
print time.time()-start_time

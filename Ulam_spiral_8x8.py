#code adapted from Daniel Shiffman in his tuto on Ulam Spiral in P5.js - see coding train

from machine import Pin
from neopixel import NeoPixel
from time import sleep

ROWS=8
COLS=8


np = NeoPixel(Pin(28, Pin.OUT),64)

def write_pixel(x, y, a,b,c):
    if y >= 0 and y < ROWS and x >=0 and x < COLS:
        np[int(y*ROWS)+x]=(a,b,c)


x=3
y=4



step=1 				# compteur de pas
direction=0 			# dans quelle direction on va
numSteps=1 			#combien de pas avant de changer d'état ou de direction
turnCounter=1 		# on fait deux sequence avant de changer de direction
totalSteps = 49

def isPrime(value):
    if value==1:
        return False
    for i in range(2,value):
        if value%i==0:
            return False
    return True


for i in range(1,totalSteps+1):
    if isPrime(i):
        write_pixel(x,y,0,150,0)
        np.write()
        print(i)
    else:
        write_pixel(x,y,50,0,0)
        np.write()
        
    if direction==0:
        x+=1

    if direction==1:
        y-=1

    if direction==2:
        x-=1

    if direction==3:
        y+=1

    if step%numSteps==0:
        direction=(direction+1)%4
        turnCounter+=1
        if turnCounter%2==0:
            numSteps+=1
    step+=1
    sleep(0.1)



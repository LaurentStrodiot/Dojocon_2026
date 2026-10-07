from machine import Pin 
from neopixel import NeoPixel 
from time import sleep 

np = NeoPixel(Pin(28), 64) 

ghost1 =[0,0,1,1,1,1,0,0,
          0,1,1,1,1,1,1,0,
          0,1,1,0,1,1,0,1,
          0,1,1,2,1,1,2,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,0,1,1,0,1,1]

ghost2 =[0,0,1,1,1,1,0,0,
          0,1,1,1,1,1,1,0,
          0,1,1,2,1,1,2,1,
          0,1,1,0,1,1,0,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,0,1,1,0,1,1,0]

color=[(0,0,0),(127,127,0),(50,50,50)]

animation=[ghost1,ghost2]


def display(image):
    for i in range(0,64):
        a,b,c=color[image[i]]		 # get the rgb values from the color palette	
        np[i]=(int(a*0.1),int(b*0.1),int(c*0.1)) 	 # the 0.1 parameter decreases light intensity to 10% (to limit the current)
    np.write()


while True:
    for j in range (0,len(animation)):
        display(animation[j])
        sleep(0.5)

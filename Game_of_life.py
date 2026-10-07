#GAME OF LIFE
#Inspiration basée sur les travaux de Daniel Shiffman 


from machine import Pin
from neopixel import NeoPixel
from random import randint

#np = Neopixel(256,0,28, "GRB")
np = NeoPixel(Pin(28, Pin.OUT),256)

grid=[]
newgrid=[]
generation = 0
nombre_cell = 0
tableau_cell = [0,0,0,0,0,0,0,0,0,0]
reste=0

for i in range(16):
    grid.append([])
    newgrid.append([])


for i in range(0,16):
    for j in range(0,16):
        grid[i].append(randint(0,1))
        newgrid[i].append(0)


def copy_tableau():
    for i in range(0,16):
        for j in range(0,16):
            grid[i][j]=newgrid[i][j]



def afficher(tableau):
    for i in range(0,16):
        for j in range(0,16):
            value=tableau[i][j]
            if (i%2 ==0):
                np[(i*16)+(15-j)]=(value*0,value*150,value*0)
            else:
                np[((i*16)+j)]=(value*0,value*150,value*0)
            global nombre_cell
            nombre_cell=nombre_cell+value
    np.write()



while True:
    afficher(grid)
    for i in range(16):
        for j in range(16):
            tot=0
            tot=tot + grid[i-1][j-1]
            tot=tot + grid[i-1][j]
            tot=tot + grid[i][j-1]
            if i<15 and j<15:
                tot=tot + grid[i-1][j+1]
                tot=tot + grid[i][j+1]
                tot=tot + grid[i+1][j-1]
                tot=tot + grid[i+1][j]
                tot=tot + grid[i+1][j+1]
            elif i<15 and j==15: #pour tester le bord droit
                tot=tot + grid[i-1][0]
                tot=tot + grid[i][0]
                tot=tot + grid[i+1][j-1]
                tot=tot + grid[i+1][j]
                tot=tot + grid[i+1][0]
            elif j<15 and i==15: #pour tester le bord inférieur
                tot=tot + grid[i-1][j+1]
                tot=tot + grid[i][j+1]
                tot=tot + grid[0][j-1]
                tot=tot + grid[0][j]
                tot=tot + grid[0][j+1]
            elif j==15 and i==15:
                tot=tot + grid[i-1][0]
                tot=tot + grid[i][0]
                tot=tot + grid[0][j-1]
                tot=tot + grid[0][j]
                tot=tot + grid[0][0]
            
            if tot<2 or tot>3:
                newgrid[i][j]=0
            if tot==3:
                newgrid[i][j]=1
            if tot==2:
                newgrid[i][j]=grid[i][j]
                
    copy_tableau()                
    #print(nombre_cell)
    tableau_cell.append(nombre_cell)
    tableau_cell.pop(0)
    for i in range(0,10):# je calcule la somme des différences entre le nombre de cellules actuel et les nombres précédents
        reste = reste+abs((nombre_cell-tableau_cell[i]))
    if reste == 0: #si pas de différence avec les 10 dernières générations alors on arrête
        machine.reset()
    nombre_cell=0
    reste=0


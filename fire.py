import machine
import neopixel
import time
import random

# 1. Configuration du Raspberry Pi Pico
PIN_DATA = 28      # Broche GP15
NB_LEDS = 64       # Matrice 8x8
PIN_MATRICE = machine.Pin(PIN_DATA, machine.Pin.OUT)
np = neopixel.NeoPixel(PIN_MATRICE, NB_LEDS)

# 2. Création de la grille de "chaleur" (8 colonnes x 8 lignes)
# 0 = froid noir, 255 = chaleur maximale blanche/jaune
chaleur = [0] * NB_LEDS

# Palette de couleurs "Feu" (Chaleur de 0 à 255 -> RGB)
def couleur_feu(degre):
    if degre < 80:
        # Chaleur faible : Rouge sombre à Rouge vif
        return (int(degre * 2), 0, 0)
    elif degre < 180:
        # Chaleur moyenne : Rouge à Orange/Jaune
        return (255, int((degre - 80) * 2.2), 0)
    else:
        # Chaleur forte : Jaune à Blanc
        return (255, 255, int((degre - 180) * 3.4))

# Fonction pour convertir les coordonnées X,Y en index de LED
# Gère le câblage standard en "Zig-Zag" de la plupart des matrices 8x8
def index_led(x, y):
    if y % 2 == 0:
        # Ligne paire : de gauche à droite
        return (y * 8) + x
    else:
        # Ligne impaire : de droite à gauche (reverse)
        return (y * 8) + (7 - x)

# 3. Boucle principale de l'animation
print("Animation Feu lancée... Appuyez sur Ctrl+C dans Thonny pour stopper.")

while True:
    # Étape A : Générer des étincelles/braises aléatoires sur la ligne du bas (y = 7)
    for x in range(8):
        # On injecte une forte chaleur aléatoire à la base du feu
        chaleur[index_led(x, 7)] = random.randint(140, 255)

    # Étape B : Faire monter la chaleur vers le haut (de y = 0 à y = 6)
    for y in range(7):
        for x in range(8):
            # On calcule l'index du pixel actuel et de celui juste en dessous
            idx_actuel = index_led(x, y)
            idx_dessous = index_led(x, y + 1)
            
            # La chaleur du dessous monte, mais se refroidit (on retire de la valeur)
            refroidissement = random.randint(20, 45)
            nouvelle_chaleur = chaleur[idx_dessous] - refroidissement
            
            # On s'assure que la chaleur ne tombe pas en dessous de 0
            if nouvelle_chaleur < 0:
                nouvelle_chaleur = 0
                
            chaleur[idx_actuel] = nouvelle_chaleur

    # Étape C : Traduire la chaleur en couleurs et l'envoyer à la matrice
    for i in range(NB_LEDS):
        np[i] = couleur_feu(chaleur[i])
        
    np.write() # Rafraîchissement physique des LED
    
    # Vitesse de l'animation (plus le temps est court, plus le feu est rapide)
    time.sleep(0.06)

__author__ = 'hadrien'

from math import degrees, radians, cos, sin, asin,pi
from Tkinter import *

# parametres (attention heure en TU)
annee =  2015
mois =  5
jour = 23
heures = 14
minutes = 37
secondes = 0

# coordonnees en degres decimaux
longitude = - 2.21
latitude = 48.5
latitudeRad = radians(latitude)

# calcul du jour julien
JJ = 367 * annee
JJ = JJ - int ( 1.75 * ( int((mois+9)/12) + annee ) )
JJ = JJ - int ( 0.75 * ( 1 + int (( int((mois-9)/7) + annee ) * 0.01 ) ) )
JJ = JJ + int(275 * mois / 9 ) + jour + 1721028.5
# ok, valide. test unitaire: 15/5/2015 : trouver 2457157.5

# calcul du temps en siecle julien 2000.0
T = (JJ - 2451545) / 36525

# approximation du temps sideral greenwich a minuit
TS = 6.69737456 + ( 8640184.812166 * T + 0.093103 * T * T ) / 3600
TS = TS % 24
# ok, valide. test unitaire: trouver 15/5/2015: 15h29m37s (15.4937646929)

def printHMS(s, h):
    heure = int (h)
    min = int ((h - heure) * 60 )
    sec = int((h - heure - float(min) / 60 ) * 3600)
    print (s+"{0}h {1}m {2}s".format(heure,min,sec))

# TS local (heures decimales)
h = heures + float(minutes)/ 60 + float(secondes) / 3600
TSL = TS + h * 1.0027379 - longitude / 15
TSL = TSL % 24
printHMS("TSL=",TSL)

# init screen
master = Tk()
taille = 500
w = Canvas(master, width=taille, height=taille)
w.pack()
w.create_oval(5, 5, taille, taille, fill="black")

#for each star
etoiles = open('stars1500.txt')
count = 0
for line in etoiles:
    count = count + 1
    if (count > 500):
        break
    etoile = line.split()
    # etoile: 0 = id, 1 = alpha, 2 = delta, 4 = magnitude, 5 = color (type)
    alpha = radians(float(etoile[1]))
    delta = radians(float(etoile[2]))
    magnitude = float(etoile[4])
    # calcul de l'angle horaire en degres decimaux
    H = radians((TSL * 15 - float(etoile[1])) % 360)
    # calcul de la hauteur (radians)
    hauteur = sin(latitudeRad) * sin(delta) + cos(latitudeRad) * cos(delta) * cos(H)
    hauteur = asin(hauteur)
    # calcul de l'azimut (radians, origine sud)
    sinazimut = cos(delta) * sin(H) / cos(hauteur)
    cosazimut = - cos(latitudeRad) * sin (delta) + sin(latitudeRad) * cos(delta) * cos(H)
    azimut = asin(sinazimut)
    if (cosazimut < 0 ):
        azimut = pi - azimut
    # peut s'optimiser en gardant sin a et sin h jusque affichage

    if hauteur < 0:
        continue

    # dessiner l'etoile = 0,0: haut gauche ; taille
    rayon = float(taille)/2
    r = rayon * ( 90 - degrees(hauteur) ) / 90
    x = int(rayon + r * sinazimut + .5)
    y = int(rayon + r * cosazimut + .5)

    if (count < 20):
        print ("s.az:{0} c.az:{1} h:{2}m r:{3} x:{4} y:{5} rcosaz:{6} {7}".format(sinazimut,cosazimut, hauteur,r,x,y, r*cosazimut, r*cos(azimut)))

    if (magnitude < 2.01):
        w.create_rectangle(x,y,x+4,y+4, fill="white",  )
    else:
        w.create_rectangle(x,y,x+2,y+2, fill="white",  )

    # recognize polaire
    if etoile[0].startswith("11767"):
        w.create_rectangle(x,y,x+4,y+4, fill="red",  )

    # limit to magnitude 4.15
    if (count > 600):
         break
mainloop()


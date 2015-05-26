__author__ = 'hadrien'

from math import pi

# converts the stars.txt files

compact = True

etoiles = open('stars500.txt')
fout = open('output/stars500o.txt', 'w')
fout.write('[')
for line in etoiles:
    etoile = line.split()
    for i in range(511):
        delta = float(etoile[3*i+1])
        if (delta < - 50): # latitude
            continue
        if ( i != 0):
            fout.write(',\n')

        if compact:
            alpha = int(float(etoile[3*i]) *10)
            delta = int( (float(etoile[3*i+1])+90) *20)
            mag = float(etoile[3*i+2])
            star = int(mag)
            if (mag <0):
                star= 0
            star = star + delta*10
            star = star + alpha *100000
            line = " {0} ".format(star)
            fout.write(line)
        else:
            alphaRad = float(etoile[3*i])/360*2*pi
            deltaRad = delta/360*2*pi
            mag = "false"
            if  float(etoile[3*i+2]) < 2.01:
                mag = "true"
            line = "[ {0}, {1}, {2} ]".format(alphaRad,deltaRad,mag)
            fout.write(line)
fout.write(']')
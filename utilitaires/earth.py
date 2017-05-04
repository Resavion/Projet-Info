import math as ma

# Constantes (ellipsoide WGS84)
R = 6371008.8
A = 6378137.0
F = 1/298.257223563
GM = 3.986005e14
E = ma.sqrt(2. * F - ma.pow(F, 2))

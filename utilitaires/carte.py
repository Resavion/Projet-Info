import numpy as np
import math as ma
import matplotlib.pyplot as plt

import utilitaires.earth as earth


def phi_to_lat_iso(phi, e):
    """
    Convertit latitude phi vers latitude isometrique.
    Les angles sont exprimes en degres decimaux.


    :param phi: latitude en degres decimaux
    :param e: excentricite de l'ellipsoide
    :return: latitude isometrique

    Example:
    >>> phi_to_lat_iso(45,0.08181919104281579)
    50.2274658154
    """

    phi     = np.asarray(phi)
    phi     = phi * ma.pi / 180.

    terme1  = 1. + e * np.sin(phi)
    terme2  = 1. - e * np.sin(phi)
    lat_iso = np.log(np.tan(ma.pi / 4. + phi / 2.)) - e / 2. * np.log(terme1 / terme2)

    return lat_iso


def lat_iso_to_phi(lat, e):
    """
    Convertit latitude isometrique vers latitude phi.
    Les angles sont exprimes en degres decimaux.

    :param lat: latitude isometrique
    :param e: excentricite de l'ellipsoide
    :return: latitude en degres decimaux

    Example:
    >>> lat_iso_to_phi(50.2274658154,0.08181919104281579)
    45.0
    """

    phi  = 2. * np.arctan(np.exp(lat)) - ma.pi / 2.
    phi0 = 999
    while all(np.abs(phi - phi0) > 1e-10):
        phi0   = phi
        terme1 = 1. + e * np.sin(phi0)
        terme2 = 1. - e * np.sin(phi0)
        phi    = 2. * np.arctan((terme1 / terme2) ** (e / 2.) * np.exp(lat)) - ma.pi / 2.

    phi = phi * 180. / ma.pi

    return phi


def lit_fic_coords(fichier):
    """
    Lit un fichier de coordonnees lat, lon. Separateur : espace.
    Les angles sont exprimes en degres decimaux.

    :param fichier: le fichier de coordonnees
    :return: les coordonnees en objet python
    """

    data = np.genfromtxt(fichier, delimiter=" ")

    return data


def mercator(coords, e, x0, y0, n):
    """
    Convertit latitude isometrique vers latitude phi.
    Les angles sont exprimes en degres decimaux.

    :param coords: liste de coordonnees lat, lon (degres decimaux)
    :param e: excentricite de l'ellipsoide
    :param x0: origine des X
    :param y0: origine des Y
    :param n: coefficient
    :return: liste de coordonnees X, Y en projection Mercator
    """

    lon = coords[:, 1]
    lat = coords[:, 0]

    x   = n * lon + x0
    y   = n * phi_to_lat_iso(lat, e) * 1e2 + y0

    return x, y


def dessine_fondcarte():
    # Lecture du trait de cotes
    coords_latlon = np.genfromtxt('utilitaires/coast2.txt')
    # Transfo en Mercator
    x, y = mercator(coords_latlon, earth.E, 0, 0, earth.A)
    # Ajout a la carte
    plt.fill(x, y, 'bisque', edgecolor='sienna', linewidth=0.1)
    return


def parametrage_carte(x_min=-1200000000.0, x_max=1250000000.0,
                      y_min=-1100000000.0, y_max=1800000000.0):
    plt.axis([x_min, x_max, y_min, y_max])
    plt.tick_params(axis='both', which='both', bottom='off', top='off', \
                    right='off', left='off')
    frame1 = plt.gca()
    frame1.axes.xaxis.set_ticklabels([])
    frame1.axes.yaxis.set_ticklabels([])
    frame1.set_facecolor('lightcyan')


def add_arrow(line, position=None, direction='right', size=15, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    position:   x-position of the arrow. If None, mean of xdata is taken
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """

    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = xdata.mean()
    # find closest index
    start_ind = np.argmin(np.absolute(xdata - position))
    if direction == 'right':
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1

    line.axes.annotate(
        '',
        xytext=(xdata[start_ind], ydata[start_ind]),
        xy=(xdata[end_ind], ydata[end_ind]),
        arrowprops=dict(arrowstyle="->", color=color),
        size=size
    )


def waypoint(lat1_deg, lon1_deg, lat2_deg, lon2_deg, frac, dist, radius=6371000):
    """
    Calcule les coordonnees d'un point intermediaire le long d'une geodesique
    
    :param lat1_deg: latitude en degres du point de depart
    :param lon1_deg: longitude en degres du point de depart 
    :param lat2_deg: latitude en degres du point d'arrivee
    :param lon2_deg: longitude en degres du point d'arrivee
    :param frac: position du point intermediaire (entre 0 et 1)
    :param dist: distance entre les deux points
    :param radius: rayon moyen de la Terre
    :return: latitude et longitude en degres du point intermediaire
    """

    delta   = dist/radius
    a       = ma.sin((1. - frac)*delta)/ma.sin(delta)
    b       = ma.sin(frac*delta)/ma.sin(delta)
    lat1    = ma.radians(lat1_deg)
    lat2    = ma.radians(lat2_deg)
    lon1    = ma.radians(lon1_deg)
    lon2    = ma.radians(lon2_deg)
    x       = a * ma.cos(lat1) * ma.cos(lon1) + b * ma.cos(lat2) * ma.cos(lon2)
    y       = a * ma.cos(lat1) * ma.sin(lon1) + b * ma.cos(lat2) * ma.sin(lon2)
    z       = a * ma.sin(lat1) + b * ma.sin(lat2)
    lat     = ma.atan2(z, ma.sqrt(x**2 + y**2))
    lon     = ma.atan2(y, x)
    lat_deg = ma.degrees(lat)
    lon_deg = ma.degrees(lon)
    return lat_deg, lon_deg


def bearing(lat1_deg, lon1_deg, lat2_deg, lon2_deg):
    """
    Methode qui permet de calculer un azimut entre deux points
    
    :param lat1_deg: 
    :param lon1_deg: 
    :param lat2_deg: 
    :param lon2_deg: 
    :return: 
    """

    dlon = ma.radians(lon2_deg - lon1_deg)
    lat1 = ma.radians(lat1_deg)
    lat2 = ma.radians(lat2_deg)
    y    = ma.sin(dlon) * ma.cos(lat2)
    x    = ma.cos(lat1) * ma.sin(lat2) - ma.sin(lat1) * ma.cos(lat2) * ma.cos(dlon)
    return ma.degrees(ma.atan2(y, x))


def distance_haversine(lat1_deg, lon1_deg, lat2_deg, lon2_deg, radius=6371000):
    """
    Methode qui permet de calculer la distance la plus courte (selon la ligne geodesique)
    entre deux points
    
    :param lat1_deg: latitude en degres
    :param lon1_deg: longitude en degres
    :param lat2_deg: latitude en degres
    :param lon2_deg: longitude en degres
    :param radius: rayon moyen de la Terre en metres
    :return: distance selon la geodesique en metres
    """

    dlat = ma.radians(lat2_deg - lat1_deg)
    dlon = ma.radians(lon2_deg - lon1_deg)
    lat1 = ma.radians(lat1_deg)
    lat2 = ma.radians(lat2_deg)
    a    = ma.sin(dlat / 2) * ma.sin(dlat / 2) + ma.sin(dlon / 2) * ma.sin(dlon / 2) * ma.cos(lat1) * ma.cos(lat2)
    c    = 2 * ma.atan2(ma.sqrt(a), ma.sqrt(1 - a))
    return c * radius


def densif_geodesique(list_coords, dist):
    """
    Cree 1 point intermediaire tous les 100 kms environ sur la geodesique
    
    :param list_coords: liste de coordonnees en entree (les 2 extremites)
    :param dist: distance de la route selon la geodesique
    :return: nouvelle liste de coordonnees
    """

    nb_points          = int(ma.floor(dist/2e5))
    lat1_deg, lon1_deg = list_coords[0, :]
    lat2_deg, lon2_deg = list_coords[1, :]
    new_coords         = np.zeros((nb_points+1, 2))
    new_coords[0, :]   = list_coords[0, :]
    for i in range(1, nb_points):
        frac             = i/nb_points
        lat, lon         = waypoint(lat1_deg, lon1_deg, lat2_deg, lon2_deg, frac, dist)
        new_coords[i, :] = lat, lon
    new_coords[nb_points, :] = list_coords[1, :]
    return new_coords


def decoupe_ligne(list_coords):
    """
    Methode qui permet de decouper une route en deux parties au niveau du meridien 180
    
    :param list_coords: liste des coordonnees en entree
    :return: liste de listes de coordonnees (1 seul element si pas decoupe)
    """

    liste1     = []
    liste2     = []
    liste      = liste1
    point_prec = list_coords[0]
    for point in list_coords:
        lon_prec   = point_prec[1]
        lon        = point[1]
        signe_prec = lon_prec/abs(lon_prec)
        signe      = lon/abs(lon)
        saut       = (signe_prec * signe < 0 and abs(lon) > 170)
        if saut:
            lat_prec  = point_prec[0]
            lat       = point[0]
            dlon_prec = 180 - signe_prec*lon_prec
            dlon      = 180 - signe*lon
            dlat      = lat - lat_prec
            lat_mid   = lat_prec + dlat*dlon_prec/(dlon + dlon_prec)
            liste.append([lat_mid, signe_prec*180])
            liste = liste2
            liste.append([lat_mid, signe*180])
        liste.append(point)
        point_prec = point
    liste_return = [np.array(liste1)]
    if liste2:
        liste_return.append(np.array(liste2))
    return liste_return

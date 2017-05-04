import numpy as np
import math as ma


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
    phi = np.asarray(phi)
    phi = phi * ma.pi / 180.

    terme1 = 1. + e * np.sin(phi)
    terme2 = 1. - e * np.sin(phi)
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
    phi = 2. * np.arctan(np.exp(lat)) - ma.pi / 2.
    phi0 = 999
    while all(np.abs(phi - phi0) > 1e-10):
        phi0 = phi
        terme1 = 1. + e * np.sin(phi0)
        terme2 = 1. - e * np.sin(phi0)
        phi = 2. * np.arctan((terme1 / terme2) ** (e / 2.) * np.exp(lat)) - ma.pi / 2.

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

    x = n * lon + x0
    y = n * phi_to_lat_iso(lat, e) * 1e2 + y0

    return x, y


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
    delta = dist/radius
    a = ma.sin((1. - frac)*delta)/ma.sin(delta)
    b = ma.sin(frac*delta)/ma.sin(delta)
    lat1 = ma.radians(lat1_deg)
    lat2 = ma.radians(lat2_deg)
    lon1 = ma.radians(lon1_deg)
    lon2 = ma.radians(lon2_deg)
    x = a * ma.cos(lat1) * ma.cos(lon1) + b * ma.cos(lat2) * ma.cos(lon2)
    y = a * ma.cos(lat1) * ma.sin(lon1) + b * ma.cos(lat2) * ma.sin(lon2)
    z = a * ma.sin(lat1) + b * ma.sin(lat2)
    lat = ma.atan2(z, ma.sqrt(x**2 + y**2))
    lon = ma.atan2(y, x)
    return lat, lon


def bearing(lat1_deg, lon1_deg, lat2_deg, lon2_deg):
    dlon = ma.radians(lon2_deg - lon1_deg)
    lat1 = ma.radians(lat1_deg)
    lat2 = ma.radians(lat2_deg)
    y = ma.sin(dlon) * ma.cos(lat2)
    x = ma.cos(lat1) * ma.sin(lat2) - ma.sin(lat1) * ma.cos(lat2) * ma.cos(dlon)
    return ma.degrees(ma.atan2(y, x))


def distance_haversine(lat1_deg, lon1_deg, lat2_deg, lon2_deg, radius=6371000):
    """ note that the default distance is in meters """
    dlat = ma.radians(lat2_deg - lat1_deg)
    dlon = ma.radians(lon2_deg - lon1_deg)
    lat1 = ma.radians(lat1_deg)
    lat2 = ma.radians(lat2_deg)
    a = ma.sin(dlat / 2) * ma.sin(dlat / 2) + ma.sin(dlon / 2) * ma.sin(dlon / 2) * ma.cos(lat1) * ma.cos(lat2)
    c = 2 * ma.atan2(ma.sqrt(a), ma.sqrt(1 - a))
    return c * radius

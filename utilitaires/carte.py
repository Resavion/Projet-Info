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
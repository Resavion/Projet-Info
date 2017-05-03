import math as ma
# import numpy as np

import ihm.console as ihm
import utilitaires.earth as earth


class Route(object):
    def __init__(self, id_route, compagnie, aeroport_depart, aeroport_arrivee, geom, codeshare,
                 horaires=None):
        """
        Constructeur de la classe route
        
        :param id_route: id de la route
        :param compagnie: compagnie qui propose la route
        :param aeroport_depart: aeroport de depart de la route
        :param aeroport_arrivee: aeroport d'arrivee de la route
        :param geom: linestring entre les deux aeroports en WKT
        :param codeshare: booleen qui permet de savoir si un avion est partage par plusieurs compagnies
        :param horaires: liste des horaires sur cette route
        """
        self._id = id_route
        self._compagnie = compagnie
        self._aeroport_depart = aeroport_depart
        self._aeroport_arrivee = aeroport_arrivee
        self._geom = geom
        self._distance = self.distance_haversine(aeroport_depart, aeroport_arrivee)
        self._codeshare = codeshare
        if horaires is None:
            horaires = []
        self._horaires = horaires

    @property
    def id(self):
        return self._id

    @property
    def compagnie(self):
        return self._compagnie

    @property
    def aeroport_depart(self):
        return self._aeroport_depart

    @property
    def aeroport_arrivee(self):
        return self._aeroport_arrivee

    @property
    def geom(self):
        return self._geom

    @property
    def codeshare(self):
        return self._codeshare

    @property
    def distance(self):
        return self._distance

    @property
    def horaires(self):
        return self._horaires

    def __str__(self):
        return "{} - Id : {} - {} ({},{}) -> {} ({},{}) - {:.0f} km - " \
               "Horaires : {}"\
            .format(self._compagnie.id_code_iata,
                    self._id,
                    self._aeroport_depart.id_code_iata,
                    self._aeroport_depart.municipalite,
                    self._aeroport_depart.code_pays,
                    self._aeroport_arrivee.id_code_iata,
                    self._aeroport_arrivee.municipalite,
                    self._aeroport_arrivee.code_pays,
                    self._distance / 1000,
                    len(self._horaires))

    @staticmethod
    def distance_haversine(dep, arr, radius=6371000):
        """ note that the default distance is in meters """
        dlat = ma.radians(arr.latitude_deg - dep.latitude_deg)
        dlon = ma.radians(arr.longitude_deg - dep.longitude_deg)
        lat1 = ma.radians(dep.latitude_deg)
        lat2 = ma.radians(arr.latitude_deg)
        a = ma.sin(dlat / 2) * ma.sin(dlat / 2) + ma.sin(dlon / 2) * ma.sin(dlon / 2) * ma.cos(lat1) * ma.cos(lat2)
        c = 2 * ma.atan2(ma.sqrt(a), ma.sqrt(1 - a))
        return c * radius

    @staticmethod
    def bearing(self, dep, arr):
        dlon = ma.radians(arr.longitude_deg - dep.longitude_deg)
        lat1 = ma.radians(dep.latitude_deg)
        lat2 = ma.radians(arr.latitude_deg)
        y = ma.sin(dlon) * ma.cos(lat2)
        x = ma.cos(lat1) * ma.sin(lat2) - ma.sin(lat1) * ma.cos(lat2) * ma.cos(dlon)
        return ma.degrees(ma.atan2(y, x))

    def waypoint(self, dep, arr, frac, radius=6371000):
        delta = self._distance/radius
        a = ma.sin((1. - frac)*delta)/ma.sin(delta)
        b = ma.sin(frac*delta)/ma.sin(delta)
        lat1 = ma.radians(dep.latitude_deg)
        lat2 = ma.radians(arr.latitude_deg)
        lon1 = ma.radians(dep.longitude_deg)
        lon2 = ma.radians(arr.longitude_deg)
        x = a * ma.cos(lat1) * ma.cos(lon1) + b * ma.cos(lat2) * ma.cos(lon2)
        y = a * ma.cos(lat1) * ma.sin(lon1) + b * ma.cos(lat2) * ma.sin(lon2)
        z = a * ma.sin(lat1) + b * ma.sin(lat2)
        lat = ma.atan2(z, ma.sqrt(x**2 + y**2))
        lon = ma.atan2(y, x)
        return lat, lon

    def ajouter_horaire(self):
        """
        Methode qui permet d'ajouter un horaire de vol a une route 
        :return: 
        """
        pass

    def supprimer_horaire(self):
        """
        Methode qui permet de supprimer un horaire de vol a une route
        
        :return: 
        """
        pass

    def calculer_plan_vol(self):
        """
        Methode pour calculer le trajet de l'avion en fonction des zones autorisées
        :return: 
        """
        pass

    def afficher_stats(self):
        """
        Methode qui permet d'afficher les statistiques sur le nombre de personnes ayant réellement
        emprunté le chemin par rapport au nombre de places offertes
        :return: 
        """
        pass

    def afficher_horaires(self):
        """
        Methode qui permet d'afficher les horaires ou cette route est empruntée
        :return: 
        """
        for horaire in self._horaires:
            print(horaire)
        ihm.demander("Tapez sur une touche pour revenir au menu")
        return

    def chercher_horaire(self, date):
        pass

    def afficher_plan_vol(self):
        """
        Methode qui permet d'afficher le plan de vol et les différents points de passages (????)
        de l'avion
        :return: 
        """
        pass

    def afficher_carte(self, start=None, show=True, annot=True):
        """
        Methode qui permet d'afficher la route reliant deux aeroports
        :return: 
        """
        ae = earth.A
        fe = earth.F
        mu = earth.GM
        ee = earth.E

        # # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
        # if show:
        #     # Lecture du trait de cotes
        #     coords_latlon = aux.lit_fic_coords('../Data/coast.txt')
        #     # Transfo en Mercator
        #     x, y = aux.mercator(coords_latlon, ee, 0, 0, 6378137.0)
        #     # Ajout a la carte
        #     plt.fill(x, y, 'bisque', linewidth=0.1)
        return


    #
    # # Methode pour faire une carte de la trace au sol du satellite
    # # !!! N'EST PLUS A coder !!!
    # # En entree,
    # # ae       = demi-grand axe de l'ellipsoide (m)
    # # fe       = applatissement de l'ellipsoide
    # # GM       = constante fondamentale x masse terrestre (m^3/s^2)
    # # duration = duree de la trace (MJD)
    # # start    = epoque de debut de la trace (MJD)
    # # show     = affiche la carte ou non (bool)
    # # annot    = affiche le nom du satellite ou non (bool)
    # def plot_track(self, ae, fe, GM, duration=1, start=None, show=True, annot=True):
    #     'Methode pour faire une carte de la trace au sol du satellite'
    #
    #     # Par defaut, debut de la trace a l'epoque de reference
    #     if (start is None):
    #         start = self.ref_epoch
    #
    #     # Calcul de l'excentricite
    #     ee = ma.sqrt(2. * fe - ma.pow(fe, 2))
    #
    #     # Ajout du fond de carte (si la carte ne fait pas partie d'une composition)
    #     if (show):
    #         # Lecture du trait de cotes
    #         coords_latlon = aux.lit_fic_coords('../Data/coast.txt')
    #         # Transfo en Mercator
    #         x, y = aux.mercator(coords_latlon, ee, 0, 0, 6378137.0)
    #         # Ajout a la carte
    #         plt.fill(x, y, 'bisque', linewidth=0.1)
    #
    #     nb_steps = int(ma.floor(duration * 24 * 60))  # 1 step par minute
    #     # Si la duree est 0, un seul pas
    #     if (nb_steps < 1):
    #         nb_steps = 1
    #     list_coords = np.zeros((nb_steps, 2))
    #     i = 0
    #     # Calcul des positions a chaque instant t
    #     for t in np.linspace(start, start + duration, nb_steps):
    #         self.compute_position_keplerian(t)
    #         self.compute_position_cartesian(GM)
    #         self.celestial_to_terrestrial()
    #         lon, lat, h = aux.geocentric_to_geodetic(self.pos_curr_ter, ae, fe)
    #         lat_deg, lon_deg = aux.rad_to_deg(lat), aux.rad_to_deg(lon)
    #         list_coords[i, :] = lat_deg, lon_deg
    #         i += 1
    #     # Transfo en Mercator
    #     xs, ys = aux.mercator(list_coords, ee, 0, 0, 6378137.0)
    #     # Ajout a la carte
    #     if (show):
    #         plt.plot(xs, ys, 'b.')
    #     else:  # symbole plus petit et couleur aleatoire si partie de composition
    #         colors = 'bgrcmy'
    #         color = colors[np.random.randint(len(colors))]
    #         plt.plot(xs, ys, '{},'.format(color))  # pixel pour trace
    #         plt.plot(xs[-1], ys[-1], '{}.'.format(color))  # point pour derniere position
    #
    #     # Parametrage de la carte
    #     plt.axis([-1300000000.0, 1300000000.0, -1500000000.0, 2000000000.0])
    #     plt.tick_params(axis='both', which='both', bottom='off', top='off', \
    #                     right='off', left='off')
    #     frame1 = plt.gca()
    #     frame1.axes.xaxis.set_ticklabels([])
    #     frame1.axes.yaxis.set_ticklabels([])
    #     frame1.set_axis_bgcolor('lightcyan')
    #
    #     # Ajout d'un tag avec le nom sur le dernier point de la trace
    #     if (annot):
    #         fig = plt.gcf()
    #         ax = fig.add_subplot(111)
    #         ax.annotate('{0:s}'.format(self.code), xy=(xs[-1], ys[-1]), xytext=(1.5, 1.5), \
    #                     fontsize=8, textcoords='offset points')
    #
    #     # Affichage
    #     if (show):
    #         if (duration == 0):
    #             plt.title('Trace du satellite {0:s} a l\'epoque {1:.1f}' \
    #                       .format(self.code, start))
    #         else:
    #             plt.title('Trace du satellite {0:s} sur la periode {1:.1f}-{2:.1f}' \
    #                       .format(self.code, start, start + duration))
    #         plt.show()

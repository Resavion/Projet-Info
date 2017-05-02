import math as ma


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

    def afficher_route(self):
        """
        Methode qui permet d'afficher la route reliant deux aeroports
        :return: 
        """
        pass

    def afficher_plan_vol(self):
        """
        Methode qui permet d'afficher le plan de vol et les différents points de passages (????)
        de l'avion
        :return: 
        """
        pass

    